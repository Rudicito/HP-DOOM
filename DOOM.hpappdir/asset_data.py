from settings import *
from data_types import PatchHeader
from show_mem import *

class Patch:
    def __init__(self, asset_data, name, graphic,  is_sprite=True):
        self.graphic = graphic
        self.asset_data = asset_data
        self.name = name
        #
        self.palette = asset_data.palette
        self.header, self.patch_columns = self.load_patch_columns(name)
        self.width = self.header.width
        self.height = self.header.height
        #
        self.image = self.get_image()
        # if is_sprite:
        #     self.image = pg.transform.scale(self.image, (
        #         self.width * SCALE, self.height * SCALE)
        #         )

    def load_patch_columns(self, patch_name):
        reader = self.asset_data.reader
        patch_index = self.asset_data.get_lump_index(patch_name)
        patch_offset = reader.directory[patch_index]['lump_offset']
        #
        patch_header = self.asset_data.reader.read_patch_header(patch_offset)
        patch_columns = []

        for i in range(patch_header.width):
            offs = patch_offset + patch_header.column_offset[i]
            while True:
                patch_column, offs = reader.read_patch_column(offs)
                patch_columns.append(patch_column)
                if patch_column.top_delta == 0xFF:
                    break
        return patch_header, patch_columns

    def get_image(self):
        image = self.graphic.create([self.width, self.height])

        ix = 0
        for column in self.patch_columns:
            if column.top_delta == 0xFF:
                ix += 1
                continue

            for iy in range(column.length):
                color_idx = column.data[iy]
                color = self.palette[color_idx]
                image.draw_pixel([ix, iy + column.top_delta], color)

        return image


class Texture:
    def __init__(self, asset_data, tex_map):
        self.graphic = asset_data.graphics("map_text")
        self.asset_data = asset_data
        self.tex_map = tex_map
        self.image = self.get_image()

    def get_image(self):
        image = self.graphic.create([self.tex_map.width, self.tex_map.height])

        for patch_map in self.tex_map.patch_maps:
            patch = self.asset_data.texture_patches[patch_map.p_name_index]
            image.blit(patch.image, (patch_map.x_offset, patch_map.y_offset))

        return image


# ---------------------------------------------------- #
class Flat:
    def __init__(self, asset_data, flat_data):
        self.graphic = asset_data.graphics("fl_ce_text")
        self.flat_data = flat_data
        self.palette = asset_data.palette
        self.image = self.get_image()

    def get_image(self):
        image = self.graphic.create([64, 64])

        #
        for i, color_idx in enumerate(self.flat_data):
            ix = i % 64
            iy = i // 64
            color = self.palette[color_idx]
            image.draw_pixel([ix, iy], color)

        return image
# --------------------------------------------------- #


def get_anim_tex_list(texture_name, anim_tex_list):
    for texture_list, speed in anim_tex_list:
        if texture_name in texture_list:
            return texture_list, speed
    return None


class AssetData:
    def __init__(self, wad_data, graphics):
        self.wad_data = wad_data
        self.reader = wad_data.reader
        self.graphics = graphics
        self.get_lump_index = wad_data.get_lump_index

        graphics("map_text").init_graphic()
        graphics("fl_ce_text").init_graphic()
        graphics("patch_text").init_graphic()
        graphics("sprite_text").init_graphic()

        # palettes
        self.palettes = self.wad_data.get_lump_data(
            reader_func=self.reader.read_palette,
            lump_index=self.get_lump_index('PLAYPAL'),
            num_bytes=256 * 3
        )
        # current palette
        self.palette_idx = 0
        self.palette = self.palettes[self.palette_idx]

        # sprites
        if LOAD_SPRITES:
            self.sprites = self.get_sprites(start_marker='S_START', end_marker='S_END')
            print("Sprite loaded!")
            # show_mem("sprites")

        # texture patch names
        self.p_names = self.wad_data.get_lump_data(
            self.reader.read_string,
            self.get_lump_index('PNAMES'),
            num_bytes=8,
            header_length=4
        )

        # texture patches
        self.texture_patches = [
            Patch(self, p_name, graphics('patch_text'), is_sprite=False) for p_name in self.p_names
        ]
        print("Texture patches loaded!")
        # show_mem("texture patches")

        # wall textures
        texture_maps = self.load_texture_maps(texture_lump_name='TEXTURE1')
        if self.get_lump_index('TEXTURE2'):
            texture_maps += self.load_texture_maps(texture_lump_name='TEXTURE2')

        self.wall_textures = {
            tex_map.name: Texture(self, tex_map).image for tex_map in texture_maps
        }
        print("Wall textures loaded!")
        # show_mem("wall textures")
        
        # flat textures
        ordered_flats, self.flat_textures = self.get_flats()
        print("Flats textures loaded!")
        # show_mem("flats textures")

        # --------------------------------------------------------------------------- #
        # sky
        self.sky_id = 'F_SKY1'
        self.sky_tex_name = 'SKY1'
        self.sky_tex = self.wall_textures[self.sky_tex_name]
        # --------------------------------------------------------------------------- #

        for key, texture in self.wall_textures.items():
            texture.duplicate(1)
            
        # Animated flats
        self.animated_flats = self.get_animated_texture(ordered_flats, self.animated_flat_ranges)
        
    def get_flats(self, start_marker='F_START', end_marker='F_END'):
        idx1 = self.get_lump_index(start_marker) + 1
        idx2 = self.get_lump_index(end_marker)
        flat_lumps = self.reader.directory[idx1: idx2]

        ordered_flats = []
        flats = {}
        for flat_lump in flat_lumps:
            offset = flat_lump['lump_offset']
            size = flat_lump['lump_size']  # 64 x 64

            flat_data = []
            for i in range(size):
                flat_data.append(self.reader.read_1_byte(offset + i, byte_format='B'))

            flat_name = flat_lump['lump_name']
            ordered_flats.append(flat_name)
            flats[flat_name] = Flat(self, flat_data).image
        return ordered_flats, flats
    # --------------------------------------------------------------------------- #

    def load_texture_maps(self, texture_lump_name):
        tex_idx = self.get_lump_index(texture_lump_name)
        offset = self.reader.directory[tex_idx]['lump_offset']

        texture_header = self.reader.read_texture_header(offset)

        texture_maps = []
        for i in range(texture_header.texture_count):
            tex_map = self.reader.read_texture_map(
                offset + texture_header.texture_data_offset[i]
            )
            texture_maps.append(tex_map)
        return texture_maps

    def get_sprites(self, start_marker='S_START', end_marker='S_END'):
        idx1 = self.get_lump_index(start_marker) + 1
        idx2 = self.get_lump_index(end_marker)
        lumps_info = self.reader.directory[idx1: idx2]
        sprites = {
            lump['lump_name']: Patch(self, lump['lump_name'], self.graphics('sprite_text')).image for lump in lumps_info
        }
        return sprites

    # animated walls and flats are hardcoded: 
    # https://github.com/id-Software/DOOM/blob/a77dfb96cb91780ca334d0d4cfd86957558007e0/linuxdoom-1.10/p_spec.c#L101-L132

    # structure: (endTexture, startTexture, speed)
    animated_flat_ranges = (
        # DOOM 1
        ("NUKAGE3",	"NUKAGE1", 8),
        ("FWATER4",	"FWATER1", 8),
        ("SWATER4",	"SWATER1", 8),
        ("LAVA4",	"LAVA1", 8),
        ("BLOOD3",	"BLOOD1", 8),

        # DOOM 2
        ("RROCK08",	"RROCK05", 8),
        ("SLIME04",	"SLIME01", 8),
        ("SLIME08",	"SLIME05", 8),
        ("SLIME12",	"SLIME09", 8),
    )

    def get_animated_texture(self, texture_names, animated_ranges):

        animated_texture = []

        for end_name, start_name, speed in animated_ranges:
            try:
                start_idx = texture_names.index(start_name)
                end_idx = texture_names.index(end_name)
                animated_texture.append(tuple((texture_names[start_idx:end_idx + 1], speed)))
            except ValueError:
                continue

        return animated_texture

    