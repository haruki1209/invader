import pygame

class Bullet:
    def __init__(self, x, y, speed=-10):  # speedのデフォルトを負に設定（上に移動）
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 5
        self.height = 10
        self.active = True
        self.dx = 0  # 横方向の移動を追加

    def update(self):
        self.y += self.speed
        self.x += self.dx  # 横方向の移動を適用
        # 画面外に出たら非アクティブに
        if self.y < 0 or self.y > 600 or self.x < 0 or self.x > 800:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height)) 