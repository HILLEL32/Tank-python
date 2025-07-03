# entities.py
import pygame

class GameObject:
    """מחלקת בסיס לכל אובייקט במשחק"""
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass  # כדי שמחלקות יורשות יוכלו להגדיר update משלהן
