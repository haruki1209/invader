import pygame
import time
from sprites import create_power_up, create_defense_up

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 20
        self.height = 20
        self.speed = 2
        self.active = True
        self.sprite = create_power_up() if type == 'power' else create_defense_up()

    def update(self):
        self.y += self.speed
        if self.y > 600:
            self.active = False

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

class PowerUpEffect:
    def __init__(self, type):
        self.type = type
        self.start_time = time.time()
        self.duration = 20  # 20秒間
        self.multiplier = 1.25

    def is_active(self):
        return time.time() - self.start_time < self.duration 