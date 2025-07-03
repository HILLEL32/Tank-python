# logic/boom.py

import pygame
from logic.entities import GameObject

class Boom(GameObject):
    def __init__(self, x, y, frames, speed=5):
        self.frames = frames
        self.frame_index = 0
        self.frame_counter = 0
        self.done = False
        image = self.frames[0]
        super().__init__(x, y, image)
        self.speed = speed

    def update(self):
        self.frame_counter += 1
        if self.frame_counter % self.speed == 0:
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.done = True  # סיים את האנימציה
