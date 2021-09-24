import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):

        # Créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokemon wish")

        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Générer un joueur
        player_position = tmx_data.get_object_by_name("spawn")
        self.player = Player(player_position.x, player_position.y)

        # Gérer les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

        # Définir le rect de collision pour entrer dans les maisons
        enter_house1 = tmx_data.get_object_by_name("enter_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        enter_house2 = tmx_data.get_object_by_name("enter_house2")
        self.enter_house2_rect = pygame.Rect(enter_house2.x, enter_house2.y, enter_house2.width, enter_house2.height)

        # for obj in tmx_data.objects:
        #     name = str(obj.name)
        #     if name.startswith('enter_house'):
        #         enter_house[name[-1]] = tmx_data.get_object_by_name(name)
        #         self.enter_houserect[name[-1]] = pygame.Rect(enter_house[name[-1]].x,
        #                                                      enter_house[name[-1]].y,
        #                                                      enter_house[name[-1]].width,
        #                                                      enter_house[name[-1]].height)



    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house1(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('house1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Gérer les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.group.add(self.player)

        # Définir le rect de collision pour sortir des maisons
        enter_house1 = tmx_data.get_object_by_name('exit_house1')
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        # Récupérer point de spawn dans les maisons
        spawn_house1_point = tmx_data.get_object_by_name("spawn_house1")
        self.player.position[0] = spawn_house1_point.x
        self.player.position[1] = spawn_house1_point.y

    #def switch_house2(self):
    #    # Charger la carte
    #    tmx_data = pytmx.util_pygame.load_pygame('house2.tmx')
    #    map_data = pyscroll.data.TiledMapData(tmx_data)
    #    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    #    map_layer.zoom = 1.5

    #    # Gérer les collisions
    #    self.walls = []

    #    for obj in tmx_data.objects:
    #        if obj.type == 'collision':
    #            self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    #    # Dessiner le groupe de calques
    #    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
    #    self.group.add(self.player)

        # Définir le rect de collision pour sortir des maisons
    #    enter_house = tmx_data.get_object_by_name('exit_house')
    #    self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Récupérer point de spawn dans les maisons
    #    spawn_house_point = tmx_data.get_object_by_name("spawn_house")
    #    self.player.position[0] = spawn_house_point.x
    #    self.player.position[1] = spawn_house_point.y


    def switch_world(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Gérer les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        self.group.add(self.player)

        # Définir le rect de collision pour entrer des maisons
        enter_house1 = tmx_data.get_object_by_name('enter_house1')
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        # Récupérer point de spawn devant la maison
        spawn_house1_point = tmx_data.get_object_by_name('house1_exit')
        self.player.position[0] = spawn_house1_point.x
        self.player.position[1] = spawn_house1_point.y

    def update(self):
        self.group.update()

        self.map = 'world'

        # verifier entrée maison

        if self.map == 'world' and self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_house1()

            self.map = 'house1'

        #if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect2):
        #    self.switch_house2()

        #    self.map = 'house2'

        #if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect3):
        #    self.switch_house3()

        #    self.map = 'house3'

        # verifier sortie maison

        if self.map == 'house1' and self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_world()

            self.map = 'world'

        # Vérification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()