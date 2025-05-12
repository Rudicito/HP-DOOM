import sys
from settings import *

if sys.platform == "HP Prime":
    from hpprime import pixon, dimgrob, eval, fillrect, rect, textout, strblit2, line

    # FOR DEBUG

    # def strblit2(graphic, x, y, width, height, graphic2, sx, sy, swidth, sheight):
    #     print("strblit2 called: \n""\nx={}, y={}, width={}, height={} \nx={}, y={}, width={}, height={}\n".format(
    #             x, y, width, height, sx, sy, swidth, sheight))

else:
    def pixon(*args):
        pass
    
    def dimgrob(*args):
        pass

    def fillrect(*args):
        pass
    def rect(*args):
        pass
    
    def textout(*args):
        pass

    def strblit2(graphic, x, y, width, height, graphic2, sx, sy, swidth, sheight):
        print(
            "strblit2 called: \nx={}, y={}, width={}, height={} \nx={}, y={}, width={}, height={}\n".format(
                x, y, width, height, sx, sy, swidth, sheight))
    
    def line(*args):
        pass




def rgba(rgba):
    """
    Converts a list [R, G, B, (A)] into an ARGB integer.

    :param rgba: A list [R, G, B, (A)] If no A is provided, A defaults to 255.
    :return: An ARGB integer (32 bits).
    """
    if len(rgba) == 4:
        R, G, B, a = map(int, rgba)  # Convert all components to integers
    elif len(rgba) == 3:
        R, G, B = map(int, rgba)  # Convert components to integers
        a = 255  # Default alpha value
    else:
        raise ValueError('rgba must have at least 3 components (without alpha), or 4 components')

    # Check that R, G, B, and a values are within the range of 0 to 255
    if not (0 <= R <= 255 and 0 <= G <= 255 and 0 <= B <= 255 and 0 <= a <= 255):
        raise ValueError("R, G, B, and a values must be between 0 and 255.")

    # Adjust alpha for opacity: 0 = transparent, 255 = opaque
    alpha = 255 - a  # Invert alpha for proper ARGB behavior

    # Combine the values into an ARGB integer
    return (alpha << 24) | (R << 16) | (G << 8) | B

def int_to_rgba(argb):
    """
    Converts an ARGB integer into a list [R, G, B, A].

    :param argb: An ARGB integer (32 bits).
    :return: A list [R, G, B, A].
    """

    argb = int(argb)

    if not (0 <= argb <= 0xFFFFFFFF):
        raise ValueError("The ARGB integer must be between 0 and 0xFFFFFFFF.")

    # Extract each component
    alpha = (argb >> 24) & 0xFF
    R = (argb >> 16) & 0xFF
    G = (argb >> 8) & 0xFF
    B = argb & 0xFF

    # Calculate the actual opacity
    a = 255 - alpha  # Reverse alpha to match transparency

    return [R, G, B, a]

class Graphics:
    def __init__(self):
        self.graphics = {
            "screen": Graphic(0, 320, 240),
            "framebuffer": Graphic(1, DOOM_W, DOOM_H),
            "map_text": Graphic(2, 50000, 400), # 128
            "fl_ce_text": Graphic(3, 50000, 200), # 64
            "patch_text": Graphic(4, 50000, 200), #64
            "sprite_text": Graphic(5, 50000, 200), # 200
            "light" : Graphic(6, 256, DOOM_H),
        }

    def __call__(self, name):
        return self.graphics[name]

class Graphic: # The graphics variable, G1, G2 for example on hp prime
    def __init__(self, graphic_var, width = None, height = None):
        self.graphic_var = graphic_var
        self.width = width
        self.height = height
        # x offset where the next texture going to start
        self.offset = 0

    def init_graphic(self, width=None, height=None):
        if self.graphic_var == 0:
            # raise ValueError('G0 can not be re-dimensioned')
            fillrect(0, 0, 0, 320, 240, rgba([0,0,0]), rgba([0,0,0]))

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        # The python version of dimgrob seems to have issue to initialize the graphics var, (issue to fill with transparency color)
        # Use the hpppl one instead
        # dimgrob(self.graphic_var, self.width, self.height, rgba([255,255,255,0]))
        eval("DIMGROB_P(G"+ str(self.graphic_var)+ ", "+ str(self.width)+ ", "+ str(self.height)+ " ,"+ str(rgba([255,255,255,0]))+ ")")

    def blit(self, graph, x_y=None):
        if x_y is None:
            x = 0
            y = 0
        else:
            x = x_y[0]
            y = x_y[1]

        strblit2(self.graphic_var, x, y, graph.width, graph.height, graph.graphic_var, 0, 0, graph.width, graph.height)

    def blit_stretch(self, graph):
        strblit2(self.graphic_var, 0, 0, self.width, self.height, graph.graphic_var, 0, 0, graph.width, graph.height)
        
    def blit_not_stretch(self, graph, x_y, w_h):
        strblit2(self.graphic_var, x_y[0], x_y[1], w_h[0], w_h[1], graph.graphic_var, 0, 0, graph.width, graph.height)
        
    def blit_color(self, x_y, x_h, color=rgba([0,0,0])):
        fillrect(self.graphic_var, x_y[0], x_y[1], x_h[0], x_h[1], color, color)
        


    def blit_texture(self, texture, x_y=None):
        if x_y is None:
            x = 0
            y = 0
        else:
            x = x_y[0]
            y = x_y[1]

        strblit2(self.graphic_var, x, y, texture.width, texture.height, texture.graphic_var, texture.offset, 0, texture.width, texture.height)

    def blit_column(self, texture, x, y1, y2, text_x, text_y1, text_y2, scale):
        # # DEBUG
        # # if x < 0 or y1 < 0 or y2 < 0 or text_x < 0 or text_y1 < 0 or text_y2 < 0 or scale < 0:
        # #     print(x, y1, y2, text_x, text_y1, text_y2, scale)

        text_y1 = int(text_y1)
        text_y2 = int(text_y2)

        # print(texture.height, x, y1, y2, text_x, text_y1, text_y2, scale)

        if text_y1 > text_y2:
            print(text_y1, text_y2)

        y2 += 1

        height_g = y2 - y1
        height_t = abs(text_y2 - text_y1)

        # Put the text_y1 on a good coords (not negative or higher than the total_height of the texture,
        # Change text_y2 to keep the same distance between text_y1 and text_y2
        if text_y1 < 0 or text_y1 >= texture.total_height:
            factor = text_y1 // texture.total_height
            text_y1 = text_y1 - texture.total_height * factor
            text_y2 = text_y2 - texture.total_height * factor

        # if debug:
        #     print("after : ", text_y1, text_y2)


        if text_y2 < texture.total_height:
            strblit2(self.graphic_var, x, y1, 1, height_g,
                     texture.graphic_var, texture.offset+text_x, text_y1, 1, height_t)

        else:  # Texture need to repeat
            # First iteration
            segment_t = abs(texture.total_height - text_y1)
            segment_g = max(1, int(segment_t / scale))

            strblit2(self.graphic_var, x, y1, 1, segment_g,
                     texture.graphic_var, texture.offset+text_x, text_y1, 1, segment_t)

            # Multiple iteration
            y1 += segment_g

            segment_t = texture.total_height
            segment_g = max(1, int(segment_t / scale))

            while y1 + segment_g < y2:
                strblit2(self.graphic_var, x, y1, 1, segment_g,
                         texture.graphic_var, texture.offset+text_x, 0, 1, segment_t)
                y1 += segment_g

            # Final iteration
            # print("y1 = ", y1, "y2 = ", y2)
            segment_g = y2 - y1
            segment_t = int(segment_g * scale)

            strblit2(self.graphic_var, x, y1, 1, segment_g,
                     texture.graphic_var, texture.offset+text_x, 0, 1, segment_t)

    def line(self, color, x1, y1, x2, y2):
        line(self.graphic_var, x1, y1, x2, y2, rgba(color))

    # FOR DEBUG
    # def blit_column(self, texture, x, y1, y2, text_x, text_y1, text_y2, scale, color):
    #     y2 += 1
    #     fillrect(self.graphic_var, x, y1, 1, y2-y1, rgba(color), rgba(color))

    def blit_pixel(self, texture, g_x_y, t_x_y):
        strblit2(self.graphic_var, g_x_y[0], g_x_y[1], 1, 1,
                 texture.graphic_var, t_x_y[0]+texture.offset, t_x_y[1], 1, 1)

    def create(self, width_height):

        # print("offset", self.offset)
        # print("width_height", width_height[0],width_height[1])

        texture = TextureArray(self.graphic_var, self.offset, width_height)
        self.offset += width_height[0]
        return texture

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Key must be a tuple of two integers (x, y).")
        x, y = key
        self.draw_pixel((x, y), value)

    def __getitem__(self, key):
        x, y = key
        return self.get_pixel([x, y])

    def draw_pixel(self, x_y, color):
        x = x_y[0]
        y = x_y[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError('Try to add pixel to a graphic outside his limits :', x, y, self.width, self.height)
        else:
            pixon(self.graphic_var, x, y, rgba(color))

    # SUPER SLOW
    def get_pixel(self, x_y):
        x = x_y[0]
        y = x_y[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError('Try to get pixel to a graphic outside his limits :', x, y, self.width, self.height)
        else:
            return int_to_rgba(int(eval("get_pixel(G" + str(self.graphic_var) + "," + str(x) + "," + str(y) + ")")))

    def draw_string(self, string, x=0, y=0, color=rgba([255,255,255])):
        string = str(string)
        textout(self.graphic_var, x, y, string, color)


class TextureArray:
    def __init__(self, graphic_var, offset, shape):
        self.graphic_var = graphic_var
        # Offset is up left of the texture, value is about the x value
        self.offset = offset
        self.shape = shape
        self.width = shape[0]
        self.height = shape[1]

        self.duplicate_number = 1


        # total_height is the height with all duplicate texture
        self.total_height = self.height

    def draw_pixel(self, x_y, color):
        x = x_y[0]
        y = x_y[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError('Try to add pixel to a texture outside his limits :', x, y, self.width, self.height)
        else:
            pixon(self.graphic_var, x+self.offset, y, rgba(color))

    def get_pixel(self, x_y):
        x = x_y[0]
        y = x_y[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            # raise ValueError('Try to get pixel to a texture outside his limits : ', x, y, self.width, self.height)
            # print('Try to get pixel to a texture outside his limits')
            # print(x, y, self.width, self.height)

            return [255,0,0,255]
        else:
            return int_to_rgba(int(eval("get_pixel(G" + str(self.graphic_var) + "," + str(x+self.offset) + "," + str(y) + ")")))

    def blit(self, t_arr, x_y):

        text_offset_x_left = 0
        text_offset_x_right = 0
        text_offset_y_up = 0
        text_offset_y_down = 0

        x = x_y[0]
        if x < 0:
            text_offset_x_left = abs(x)
            x = 0
        if x + t_arr.width >= self.width:
            text_offset_x_right = abs(x + t_arr.width - self.width)

        if x >= self.width:
            return

        y = x_y[1]
        if y < 0:
            text_offset_y_up = abs(y)
            y = 0
        if y + t_arr.height >= self.height:
            text_offset_y_down = abs(y + t_arr.height - self.height)

        if y >= self.height:
            return

        # if x < 0 or x >= self.width or y < 0 or y >= self.height:
        #     raise ValueError('Try to add pixel to a texture outside his limits : ', x, y, self.width, self.height)

        visualised_width = t_arr.width - text_offset_x_left - text_offset_x_right
        visualised_height = t_arr.height - text_offset_y_up - text_offset_y_down

        # # DEBUG
        #
        # print(self.graphic_var, self.offset+x, y, visualised_width, visualised_height,
        #          t_arr.graphic_var, t_arr.offset+text_offset_x_left, 0+text_offset_y_up, visualised_width, visualised_height)
        #
        strblit2(self.graphic_var, self.offset+x, y, visualised_width, visualised_height,
                 t_arr.graphic_var, t_arr.offset+text_offset_x_left, 0+text_offset_y_up, visualised_width, visualised_height)

    def duplicate(self, duplicate_number):
        for i in range(duplicate_number):
            strblit2(self.graphic_var, self.offset, self.total_height + self.height * i, self.width, self.height,
                     self.graphic_var, self.offset, 0, self.width, self.height)

        self.duplicate_number += duplicate_number

        self.total_height = self.height * self.duplicate_number

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __len__(self):
        # Return width for len(tex)
        return self.width

    def __getitem__(self, key):
        if isinstance(key, tuple):  # Accessing specific pixel
            return self.get_pixel(key)
        elif isinstance(key, int):  # Accessing a row (still can work as a list)
            if key < 0 or key >= self.height:
                raise ValueError("Row index out of bounds.")
            return [self.get_pixel((x, key)) for x in range(self.width)]  # List of pixels in the row
        else:
            raise TypeError("Invalid key type. Must be a tuple (x, y) or int (row).")

    def __setitem__(self, key, value):
        if isinstance(key, tuple):  # Specific pixel
            x, y = key
            self.draw_pixel((x, y), value)
        elif isinstance(key, int):  # Row
            if key < 0 or key >= self.height:
                raise ValueError("Row index out of bounds.")
            for x in range(self.width):
                self.draw_pixel((x, key), value)
        else:
            raise TypeError("Invalid key type. Must be a tuple (x, y) or int (row).")



