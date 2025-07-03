# bullet.py
from logic.entities import GameObject

class Bullet(GameObject):
    def __init__(self, x, y, image, speed=10):
        super().__init__(x, y, image)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
