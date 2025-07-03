# tank.py
import pygame
from logic.entities import GameObject
from logic.bullet import Bullet

class Tank(GameObject):
    def __init__(self, x, y, image, speed=5):
        super().__init__(x, y, image)
        self.speed = speed
        self.bullets = []

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def shoot(self, bullet_image):
        bullet = Bullet(self.rect.centerx, self.rect.top, bullet_image)
        self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.bottom > 0]

    def draw(self, screen):
        super().draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
