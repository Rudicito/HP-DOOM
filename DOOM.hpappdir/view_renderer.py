from settings import *
import urandom as random
from urandom import randrange as rnd
from asset_data import get_anim_tex_list


class ViewRenderer:
    def __init__(self, engine):
        self.engine = engine
        self.asset_data = engine.wad_data.asset_data
        self.palette = self.asset_data.palette
        if LOAD_SPRITES:
            self.sprites = self.asset_data.sprites
        # self.wall_textures = self.asset_data.wall_textures
        self.flat_textures = self.asset_data.flat_textures
        self.player = engine.player
        self.screen = engine.screen
        self.framebuffer = engine.framebuffer
        self.x_to_angle = self.engine.seg_handler.x_to_angle
        self.colors = {}
        # sky settings
        self.sky_id = self.asset_data.sky_id
        self.sky_tex = self.asset_data.sky_tex
        self.sky_inv_scale = 160 / s.HEIGHT
        self.sky_tex_alt = 100
        # animated textures
        self.animated_flats = self.asset_data.animated_flats
        self.clock = self.engine.clock

    def draw_sprite(self):
        if LOAD_SPRITES:
            img = self.sprites['SHTGA0']
            pos = (s.H_WIDTH - img.get_width() // 2, s.HEIGHT - img.get_height())
            self.framebuffer.blit_texture(img, pos)

    # def draw_palette(self):
    #     pal, size = self.palette, 10
    #     for ix in range(16):
    #         for iy in range(16):
    #             col = pal[iy * 16 + ix]
    #             gfx.box(self.screen, (ix * size, iy * size, size, size), col)

    def get_color(self, tex, light_level):
        str_light = str(light_level)
        if tex + str_light not in self.colors:
            tex_id = hash(tex)
            random.seed(tex_id)
            color = self.palette[rnd(0, 256)]
            color = color[0] * light_level, color[1] * light_level, color[2] * light_level
            self.colors[tex + str_light] = color
        return self.colors[tex + str_light]

    def draw_vline(self, x, y1, y2, tex, light):
        if y1 < y2:
            color = self.get_color(tex, light)
            self.draw_column(self.framebuffer, x, y1, y2, color)

    @staticmethod
    def draw_column(framebuffer, x, y1, y2, color):
        for iy in range(y1, y2 + 1):
            framebuffer[x, iy] = color

    def draw_flat(self, tex_id, light_level, x, y1, y2, world_z):
        if y1 < y2:
            if tex_id == self.sky_id:
                tex_column = 2.2 * (self.player.angle + self.engine.seg_handler.x_to_angle[x])

                self.draw_wall_col(self.framebuffer, self.sky_tex, tex_column, x, y1, y2,
                                   self.sky_tex_alt, self.sky_inv_scale, light_level=1.0)
            else:
                result = get_anim_tex_list(tex_id, self.animated_flats)
                if result:
                    anim_list, speed = result
                    tex_id = anim_list[self.clock.cycles(speed/35*1000, len(anim_list))]
                
                flat_tex = self.flat_textures[tex_id]

                self.draw_flat_col(self.framebuffer, flat_tex,
                                   x, y1, y2, light_level, world_z,
                                   self.player.angle, self.player.pos.x, self.player.pos.y)

    @staticmethod
    def draw_flat_col(screen, flat_tex, x, y1, y2, light_level, world_z,
                      player_angle, player_x, player_y):
        if not s.RENDER_FLATS:
            screen.line([0,0,0], x, y1, x, y2)
            return
        
        player_dir_x = math.cos(math.radians(player_angle))
        player_dir_y = math.sin(math.radians(player_angle))

        for iy in range(y1, y2 + 1):
            z = s.H_WIDTH * world_z / (s.H_HEIGHT - iy)

            px = player_dir_x * z + player_x
            py = player_dir_y * z + player_y

            left_x = -player_dir_y * z + px
            left_y = player_dir_x * z + py
            right_x = player_dir_y * z + px
            right_y = -player_dir_x * z + py

            dx = (right_x - left_x) / s.WIDTH
            dy = (right_y - left_y) / s.WIDTH

            tx = int(left_x + dx * x) & 63
            ty = int(left_y + dy * x) & 63

            screen.blit_pixel(flat_tex, [x, iy], [tx, ty])

    @staticmethod
    def draw_wall_col(framebuffer, tex, tex_col, x, y1, y2, tex_alt, inv_scale, light_level):
        if not s.RENDER_WALLS:
            framebuffer.line([0,0,0], x, y1, x, y2)
            return
        
        if y1 < y2:
            tex_col = int(tex_col) % tex.width
            tex_y1 = tex_alt + (float(y1) - s.H_HEIGHT) * inv_scale
            tex_y2 = tex_y1 + int(inv_scale * (abs(y2 - y1)))
            framebuffer.blit_column(tex, x, y1, y2, tex_col, tex_y1, tex_y2, inv_scale)