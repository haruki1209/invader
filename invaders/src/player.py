import pygame
from bullet import Bullet
from sprites import create_player_sprite
import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 50
        self.height = 50
        self.bullets = []  # 弾のリストを追加
        self.bullets_remaining = float('inf')  # 通常は無制限、ボス戦では制限あり
        self.sprite = create_player_sprite()
        self.power_effect = None
        self.defense_effect = None
        self.base_damage = 1
        self.moving_left = False   # 左移動フラグを追加
        self.moving_right = False  # 右移動フラグを追加
        self.max_health = 100  # 最大体力
        self.health = self.max_health  # 現在の体力
        self.is_alive = True
        self.invincible_time = 0  # 無敵時間
        self.invincible_duration = 1.5  # ダメージを受けた後の無敵時間（秒）
    
    def handle_event(self, event):
        # キーが押されたとき
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            if event.key == pygame.K_RIGHT:
                self.moving_right = True
            if event.key == pygame.K_SPACE:
                self.shoot()
        
        # キーが離されたとき
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            if event.key == pygame.K_RIGHT:
                self.moving_right = False
    
    def shoot(self):
        if self.bullets_remaining > 0:  # 弾が残っている場合のみ発射可能
            bullet_x = self.x + (self.width // 2) - 2.5
            bullet_y = self.y - 10
            self.bullets.append(Bullet(bullet_x, bullet_y))
            if self.bullets_remaining != float('inf'):
                self.bullets_remaining -= 1
    
    def update(self):
        # 移動フラグに基づいて位置を更新
        if self.moving_left:
            self.x -= self.speed
        if self.moving_right:
            self.x += self.speed
        
        # 画面端での移動制限
        self.x = max(0, min(self.x, 800 - self.width))
        
        # 弾の更新
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # 体力バーの描画
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0),  # 赤色の背景（空の体力バー）
                        (self.x, self.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0),  # 緑色の体力バー
                        (self.x, self.y - 10, health_bar_width * health_ratio, health_bar_height))
        
        # 無敵時間中は点滅効果
        if time.time() < self.invincible_time:
            if int(time.time() * 10) % 2 == 0:  # 高速点滅
                screen.blit(self.sprite, (self.x, self.y))

    def get_current_damage(self):
        if self.power_effect and self.power_effect.is_active():
            return self.base_damage * self.power_effect.multiplier
        return self.base_damage

    def take_damage(self, damage):
        # 無敵時間中はダメージを受けない
        current_time = time.time()
        if current_time < self.invincible_time:
            return

        if self.defense_effect and self.defense_effect.is_active():
            damage /= self.defense_effect.multiplier
        
        self.health -= damage
        self.invincible_time = current_time + self.invincible_duration

        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def draw(self, screen):
        # 既存の描画コードに追加
        screen.blit(self.sprite, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # 体力バーの描画
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0),  # 赤色の背景（空の体力バー）
                        (self.x, self.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0),  # 緑色の体力バー
                        (self.x, self.y - 10, health_bar_width * health_ratio, health_bar_height))
        
        # 無敵時間中は点滅効果
        if time.time() < self.invincible_time:
            if int(time.time() * 10) % 2 == 0:  # 高速点滅
                screen.blit(self.sprite, (self.x, self.y)) 