from wad_data import WADData
from settings import *
from map_renderer import MapRenderer
from player import Player
from bsp import BSP
from seg_handler import SegHandler
from view_renderer import ViewRenderer
from graphics import *
from clock import Clock
from keys import Keys


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
        self.wad_data = WADData(self, map_name='E1M1')
        #self.map_renderer = MapRenderer(self)
        self.player = Player(self)
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
        self.screen.blit_stretch(self.framebuffer)
        try:
            fps = 1000/self.clock.dt
        except ZeroDivisionError:
            fps = 1000
        self.screen.draw_string("{:.1f} fps".format(fps)) # print fps with 1 digit
        # pg.display.flip()

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
    doom = DoomEngine()
    doom.run()
except KeyboardInterrupt:
    pass
