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
# ! Shotgun display broken if scale != 1 !
LOAD_SPRITES = False

# Screen size, float: 0 to 1
# smaller the value is, smaller the intern resolution is
# Better performance when small
SCALE = 0.5

# Stretch the game for not having black bar when scale lower than 1
STRETCH = True

FOV = 90

PLAYER_SPEED = 0.125
PLAYER_ROT_SPEED = 0.2
PLAYER_HEIGHT = 41

##########################################

DOOM_W = 320
DOOM_H = 200

SCREEN_W = 320
SCREEN_H = 240

# COLOR_KEY = (152, 0, 136)

class Settings:
    def __init__(self, render_flats, render_walls, load_sprites, scale, stretch, fov, player_speed, player_rot_speed, player_height):
        
        self.RENDER_FLATS = render_flats

        self.RENDER_WALLS = render_walls
        
        self.LOAD_SPRITES = load_sprites

        self.SCALE = scale
        
        self.STRETCH = stretch
        
        self.FOV = fov

        self.PLAYER_SPEED = player_speed
        self.PLAYER_ROT_SPEED = player_rot_speed
        self.PLAYER_HEIGHT = player_height

        self.set_screen_scale(self.SCALE)

    def set_screen_scale(self, scale):
        if scale < 0.1:
            self.SCALE = 0.1
        elif scale > 1:
            self.SCALE = 1
        else:
            self.SCALE = scale

        self.WIDTH = round(DOOM_W * self.SCALE)
        self.HEIGHT = round(DOOM_H * self.SCALE)

        self.H_WIDTH = self.WIDTH // 2
        self.H_HEIGHT = self.HEIGHT // 2

        self.H_FOV = self.FOV / 2
        self.SCREEN_DIST = self.H_WIDTH / math.tan(math.radians(self.H_FOV))

        self.HEIGHT_STRETCH = self.HEIGHT * (240/200)
        
        self.ORIGIN_X_NOT_STRETCHED = (SCREEN_W - self.WIDTH) // 2
        self.ORIGIN_Y_NOT_STRETCHED= (SCREEN_H - self.HEIGHT_STRETCH) // 2
        

# Instance unique que les autres modules peuvent importer
s = Settings(RENDER_FLATS, RENDER_WALLS, LOAD_SPRITES, SCALE, STRETCH, FOV, PLAYER_SPEED, PLAYER_ROT_SPEED, PLAYER_HEIGHT)
