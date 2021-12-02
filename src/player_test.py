import pygame
import unittest
from player import Player


class TestPlayer(unittest.TestCase):

    def test_player_spawn(self):
        player = Player()
