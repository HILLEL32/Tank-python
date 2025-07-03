# logic/enemy.py

import pygame
from logic.entities import GameObject

class AnimatedEnemyHelicopter(GameObject):
    def __init__(self, x, y, frames, speed=3):
        self.frames = frames
        self.current_frame = 0
        self.frame_counter = 0
        image = self.frames[0]
        super().__init__(x, y, image)
        self.speed = speed

    def update(self):
        # תנועה מימין לשמאל
        self.rect.x -= self.speed

        # מעבר פריימים של אנימציה
        self.frame_counter += 1
        if self.frame_counter % 5 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
