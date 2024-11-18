import math
class Vector2:
    def __init__(self, x, y=None):
        if y is None:
            self.x = self.y = x
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector2 to another Vector2")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        raise TypeError("Can only subtract Vector2 from another Vector2")

    def __iter__(self):
        """Allows unpacking of Vector2 as (x, y)."""
        yield self.x
        yield self.y

    def rotate_ip(self, angle):
        """
        Rotates the vector in place by a given angle (in degrees).
        """
        # Convert the angle to radians
        radians = math.radians(angle)
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)

        # Rotate the vector
        new_x = self.x * cos_theta - self.y * sin_theta
        new_y = self.x * sin_theta + self.y * cos_theta

        # Update the vector's components
        self.x, self.y = new_x, new_y