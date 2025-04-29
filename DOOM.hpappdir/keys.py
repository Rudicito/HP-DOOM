from hpprime import keyboard

class Keys:
    def __init__(self):
        self.keyboard_input = keyboard()
        self.left = 7
        self.right = 8
        self.up = 2
        self.down = 12

    def just_pressed(self, key):
        if self.old_keyboard_input & (1 << key) == False and self.keyboard_input & (1 << key) != False:
            return True
        else:
            return False

    def just_released(self, key):
        if self.old_keyboard_input & (1 << key) != False and self.keyboard_input & (1 << key) == False:
            return True
        else:
            return False

    def is_pressed(self, key):
        if self.keyboard_input & (1 << key) != False:
            return True
        else:
            return False

    def get(self):
        self.old_keyboard_input = self.keyboard_input
        self.keyboard_input = keyboard()