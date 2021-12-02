from dataclasses import dataclass

import pygame
import pytmx
import pyscroll

from src.player import NPC


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # "house" -> Map("house", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house1", target_world="house1",
                   teleport_point="spawn_house1"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2",
                   teleport_point="spawn_house2"),
            Portal(from_world="world", origin_point="enter_house3", target_world="house3",
                   teleport_point="spawn_house3"),
            Portal(from_world="world", origin_point="enter_dungeonroad", target_world="dungeonroad",
                   teleport_point="spawn_dungeonroad")
        ], npcs=[
            NPC("paul", nb_points=4, dialog=["Salut ! Je cherche mon chien, tu ne l'aurais pas vu ?!", "Tant pis ..."])
        ])
        self.register_map("house1", portals=[
            Portal(from_world="house1", origin_point="exit_house1", target_world="world",
                   teleport_point="house1_exit")
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house2", target_world="world",
                   teleport_point="house2_exit")
        ])
        self.register_map("house3", portals=[
            Portal(from_world="house3", origin_point="exit_house3", target_world="world",
                   teleport_point="house3_exit")
        ])
        self.register_map("dungeonroad", portals=[
            Portal(from_world="dungeonroad", origin_point="exit_dungeonroad", target_world="world",
                   teleport_point="dungeonroad_exit"),
            Portal(from_world="dungeonroad", origin_point="enter_dungeon", target_world="dungeon",
                   teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("robin", nb_points=2, dialog=["Tu entends les cris qui viennent de cette grotte ?", "Coureeeez !"])
        ])
        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="dungeonroad",
                   teleport_point="dungeon_exit")
        ])

        self.teleport_player("spawn")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        # Portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # Collisions
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Gérer les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        group.add(self.player)

        # Récupérer tous les NPCs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Enregistrer la nouvelle carte chargée
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()