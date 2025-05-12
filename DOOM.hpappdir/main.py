from wad_data import WADData
from settings import *
from player import Player
from bsp import BSP
from seg_handler import SegHandler
from view_renderer import ViewRenderer
from graphics import *
from clock import Clock
from keys import Keys
from show_mem import *


class DoomEngine:
    def __init__(self, wad_path='DOOM1.WAD'):
        self.wad_path = wad_path
        self.clock = Clock()
        self.running = True
        self.dt = 1 / 60
        self.on_init()

    def on_init(self):
        self.graphics = Graphics()
        self.screen = self.graphics("screen")
        self.framebuffer = self.graphics("framebuffer")
        self.framebuffer.init_graphic()
        self.keys = Keys()
        self.wad_data = WADData(self, MAP)
        #self.map_renderer = MapRenderer(self)
        self.player = Player(self)
        self.init_draws()
        
    def init_draws(self):
        self.screen.init_graphic()
        self.framebuffer.init_graphic(s.WIDTH, s.HEIGHT)
        self.bsp = BSP(self)
        self.seg_handler = SegHandler(self)
        self.view_renderer = ViewRenderer(self)

    def update(self):
        self.player.update()
        self.seg_handler.update()
        self.bsp.update()
        self.dt = self.clock.tick()

    def draw(self):
        self.view_renderer.draw_sprite()
        if s.STRETCH:
            self.screen.blit_stretch(self.framebuffer)
        else:
            # For refresh the screen when not stretch, only for the fps, stretch display
            self.screen.blit_color((0,0), (319, 17))
            self.screen.blit_not_stretch(self.framebuffer, (s.ORIGIN_X_NOT_STRETCHED, s.ORIGIN_Y_NOT_STRETCHED), (s.WIDTH, s.HEIGHT_STRETCH))
        try:
            fps = 1000/self.clock.dt
        except ZeroDivisionError:
            fps = 1000
        self.screen.draw_string("{:.1f} fps".format(fps)) # print fps with 1 digit
        self.screen.draw_string("Scale = {:.1f}".format(s.SCALE), 263)

    # def check_events(self):
    #     for e in pg.event.get():
    #         if e.type == pg.QUIT:
    #             self.running = False
    #             pg.quit()

    def run(self):
        while self.running:
            # dimgrob(1, 320, 240, rgba([255,0,0]))  # Fill screen with red, to see unset pixel, debug only
            self.update()
            self.draw()



try:
    print("Loading...")
    doom = DoomEngine()
    print("Loading finished!")
    show_mem()
    doom.run()
except KeyboardInterrupt:
    pass
