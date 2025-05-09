import umath as math
from vector2 import Vector2 as vec2

##########################################

# Render floor and ceiling?
# Very bad performance compared to walls
RENDER_FLATS = True

# Render walls?
RENDER_WALLS = True

# Load sprites?
# Reduce load time, reduce RAM usage
# Sprites are only used to display the shotgun
LOAD_SPRITES = False

# Screen size, 0 to 8
# 8 draw the game to all the screen; smaller the value is, smaller the screen is
# Better performance when small
SCREEN_SIZE = 0

PLAYER_SPEED = 0.05
PLAYER_ROT_SPEED = 0.2
PLAYER_HEIGHT = 41

##########################################

# COLOR_KEY = (152, 0, 136)

class Settings:
    def __init__(self, render_flats, render_walls, load_sprites, screen_size, player_speed, player_rot_speed, player_height):
        # Render floor and ceiling?
        # Very bad performance compared to walls
        self.RENDER_FLATS = render_flats

        # Render walls?
        self.RENDER_WALLS = render_walls

        # Load sprites?
        # Reduce load time, reduce RAM usage
        # Sprites are only used to display the shotgun
        self.LOAD_SPRITES = load_sprites

        # Screen size, 0 to 8
        # 8 draw the game to all the screen; smaller the value is, smaller the screen is
        # Better performance when small
        self.SCREEN_SIZE = screen_size

        self.PLAYER_SPEED = player_speed
        self.PLAYER_ROT_SPEED = player_rot_speed
        self.PLAYER_HEIGHT = player_height

        self.DOOM_W, self.DOOM_H = 320, 200
        self.DOOM_RES = self.DOOM_W, self.DOOM_H

        self.set_screen_size(self.SCREEN_SIZE)

    def set_screen_size(self, _screen_size):
        if _screen_size < 0:
            self.SCREEN_SIZE = 0
        elif _screen_size > 8:
            self.SCREEN_SIZE = 8
        else:
            self.SCREEN_SIZE = _screen_size

        set_blocks = self.SCREEN_SIZE + 3

        if set_blocks == 11:
            self.WIDTH = self.DOOM_W
            self.HEIGHT = self.DOOM_H
        else:
            self.WIDTH = set_blocks * 32
            self.HEIGHT = int(set_blocks * 168 / 10) & ~7

        self.H_WIDTH = self.WIDTH // 2
        self.H_HEIGHT = self.HEIGHT // 2

        self.FOV = 90.0
        self.H_FOV = self.FOV / 2
        self.SCREEN_DIST = self.H_WIDTH / math.tan(math.radians(self.H_FOV))

# Instance unique que les autres modules peuvent importer
s = Settings(RENDER_FLATS, RENDER_WALLS, LOAD_SPRITES, SCREEN_SIZE, PLAYER_SPEED, PLAYER_ROT_SPEED, PLAYER_HEIGHT)
