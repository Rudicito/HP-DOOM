from settings import *
from vector2 import Vector2 as vec2


class Player:
    def __init__(self, engine):
        self.engine = engine
        self.keys = self.engine.keys
        # Player 1 start thing has a type equal to 1
        self.thing = next((thing for thing in engine.wad_data.things if thing.type == 1), None)
        self.pos = self.thing.pos
        self.angle = self.thing.angle
        self.DIAG_MOVE_CORR = 1 / math.sqrt(2)
        self.height = PLAYER_HEIGHT
        self.floor_height = 0
        self.z_vel = 0

    def update(self):
        self.get_height()
        self.control()

    def get_height(self):
        # self.height = self.engine.bsp.get_sub_sector_height() + PLAYER_HEIGHT
        self.floor_height = self.engine.bsp.get_sub_sector_height()

        if self.height < self.floor_height + PLAYER_HEIGHT:
            self.height += 0.4 * (self.floor_height + PLAYER_HEIGHT - self.height)
            self.z_vel = 0
        else:
            self.z_vel -= 0.9
            self.height += max(-15.0, self.z_vel)

    def control(self):
        speed = PLAYER_SPEED * self.engine.dt
        rot_speed = PLAYER_ROT_SPEED * self.engine.dt

        self.keys.get()
        if self.keys.is_pressed(self.keys.left):
            self.angle += rot_speed
        if self.keys.is_pressed(self.keys.right):
            self.angle -= rot_speed

        inc = vec2(0)
        # if key_state[pg.K_a]:
        #     inc += vec2(0, speed)
        # if key_state[pg.K_d]:
        #     inc += vec2(0, -speed)
        if self.keys.is_pressed(self.keys.up):
            inc += vec2(speed, 0)
        if self.keys.is_pressed(self.keys.down):
            inc += vec2(-speed, 0)

        if inc.x and inc.y:
            inc *= self.DIAG_MOVE_CORR

        inc.rotate_ip(self.angle)
        self.pos += inc
