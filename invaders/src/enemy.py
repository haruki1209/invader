import pygame
import random
from bullet import Bullet
from powerup import PowerUp
from sprites import create_enemy_sprite

class Enemy:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 1
        self.width = 40
        self.height = 40
        self.sprite = create_enemy_sprite()
        self.shoot_cooldown = random.randint(180, 300)  # 3-5秒のランダムな発射間隔に変更
        self.bullets = []
        # レベルに応じた攻撃力設定
        self.damage = 5  # 基本攻撃力を5に下方修正

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= 760:
            self.direction *= -1
            self.y += 20

        # 攻撃処理
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = random.randint(180, 300)  # 3-5秒の間隔に変更

        # 弾の更新
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)

    def shoot(self):
        bullet = Bullet(self.x + self.width/2, self.y + self.height, speed=5)
        bullet.damage = self.damage
        self.bullets.append(bullet)

    def drop_item(self):
        if random.random() < 0.3:  # 30%の確率でアイテムドロップ
            item_type = random.choice(['power', 'defense'])
            return PowerUp(self.x + self.width/2, self.y + self.height, item_type)
        return None

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen) 