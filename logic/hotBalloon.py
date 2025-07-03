import pygame
from logic.entities import GameObject

class AnimatedHotBalloon(GameObject):
    def __init__(self, x, y, frames, speed=2):
        self.frames = frames
        self.current_frame = 0
        self.frame_counter = 0
        self.speed = speed
        image = self.frames[0]
        super().__init__(x, y, image)

    def update(self):
        self.rect.y += self.speed
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
