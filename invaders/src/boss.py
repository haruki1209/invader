import pygame
import random
import math
from sprites import create_boss_sprite
from bullet import Bullet

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.speed = 2
        self.direction = 1
        self.health = 50
        self.phase = 1
        self.movement_pattern = 0
        self.pattern_timer = 0
        self.attack_timer = 0
        self.sprite = create_boss_sprite()
        self.damage = 15
        self.bullets = []
        self.shoot_cooldown = 180
        self.vulnerable = True
        self.vulnerable_timer = 0
        self.vulnerable_duration = 180
        self.invulnerable_duration = 120
        self.attack_pattern = 0
        self.bullet_patterns = {
            0: self.single_shot,
            1: self.spread_shot,
            2: self.circle_shot
        }

    def update(self):
        self.pattern_timer += 1
        
        # 体力に応じて行動パターンを変更
        if self.health <= 25 and self.phase == 1:
            self.phase = 2
            self.speed = 3
            self.damage = 20
            self.vulnerable_duration = 240
        
        # 攻撃可能状態の管理
        if self.vulnerable:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0
        else:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.invulnerable_duration:
                self.vulnerable = True
                self.vulnerable_timer = 0
        
        # パターン切り替え
        if self.pattern_timer >= 180:
            self.pattern_timer = 0
            self.movement_pattern = random.randint(0, 2)
        
        # 移動パターン
        if self.movement_pattern == 0:
            # 左右移動（画面中央付近で）
            self.x += self.speed * self.direction
            if self.x <= 200 or self.x >= 600:
                self.direction *= -1
        elif self.movement_pattern == 1:
            # より小さな円運動
            self.x = 400 + math.sin(self.pattern_timer * 0.05) * 100
            self.y = 100 + math.cos(self.pattern_timer * 0.05) * 30
        else:
            # 小さめのジグザグ移動
            self.x += self.speed * self.direction
            self.y = 100 + math.sin(self.pattern_timer * 0.1) * 20
            if self.x <= 200 or self.x >= 600:
                self.direction *= -1
        
        # 攻撃パターンの切り替え
        self.attack_timer += 1
        if self.attack_timer >= 300:  # 5秒ごとに攻撃パターン変更
            self.attack_timer = 0
            self.attack_pattern = random.randint(0, 2)
        
        # 攻撃処理
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.bullet_patterns[self.attack_pattern]()
            self.shoot_cooldown = 120 if self.phase == 2 else 180  # フェーズ2では2秒間隔、それ以外は3秒間隔

    def take_damage(self):
        if self.vulnerable:
            self.health -= 1

    def draw(self, screen):
        # 攻撃可能状態を視覚的に表示
        if self.vulnerable:
            # 攻撃可能時は通常の色で描画
            screen.blit(self.sprite, (self.x, self.y))
        else:
            # 無敵時は半透明の赤色でオーバーレイ
            temp_surface = self.sprite.copy()
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 128))
            temp_surface.blit(overlay, (0, 0))
            screen.blit(temp_surface, (self.x, self.y))

    def single_shot(self):
        # 直線射撃
        bullet = Bullet(self.x + self.width/2, self.y + self.height, speed=6)
        bullet.damage = self.damage
        self.bullets.append(bullet)

    def spread_shot(self):
        # 扇状射撃
        for angle in [-0.3, -0.15, 0, 0.15, 0.3]:
            bullet = Bullet(self.x + self.width/2, self.y + self.height, speed=5)
            bullet.damage = self.damage
            bullet.dx = math.sin(angle) * 5
            self.bullets.append(bullet)

    def circle_shot(self):
        # 円形射撃（フェーズ2でのみ使用）
        if self.phase == 2:
            for i in range(8):
                angle = (math.pi * 2 * i / 8) + (self.pattern_timer * 0.02)
                bullet = Bullet(
                    self.x + self.width/2,
                    self.y + self.height/2,
                    speed=4
                )
                bullet.damage = self.damage
                bullet.dx = math.cos(angle) * 4
                bullet.speed = math.sin(angle) * 4
                self.bullets.append(bullet) 