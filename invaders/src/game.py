import pygame
from player import Player
from enemy import Enemy
from boss import Boss
from powerup import PowerUp, PowerUpEffect

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1
        self.game_state = "menu"
        self.score = 0
        self.powerups = []
        self.reset_level()

    def reset_level(self):
        self.player = Player(400, 550)
        if self.level == 4:
            self.boss = Boss(400, 100)
            self.enemies = []
            self.player.bullets_remaining = float('inf')
        else:
            self.setup_enemies()
            self.player.bullets_remaining = float('inf')

    def setup_enemies(self):
        if self.level == 1:
            self.enemies = [Enemy(x, y, speed=1) 
                           for x in range(100, 700, 100) 
                           for y in range(50, 150, 50)]
            for enemy in self.enemies:
                enemy.damage = 5  # 基本攻撃力

        elif self.level == 2:
            self.enemies = [Enemy(x, y, speed=2) 
                           for x in range(100, 700, 80) 
                           for y in range(50, 200, 50)]
            for enemy in self.enemies:
                enemy.damage = 8  # 攻撃力アップ

        elif self.level == 3:
            self.enemies = [Enemy(x, y, speed=3) 
                           for x in range(100, 700, 60) 
                           for y in range(50, 250, 50)]
            for enemy in self.enemies:
                enemy.damage = 12  # さらに攻撃力アップ

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # 日本語フォントの設定
        try:
            font_path = pygame.font.match_font('yugothic', 'meiryo', 'ms gothic')  # Windowsフォント
            if not font_path:
                font_path = pygame.font.match_font('hiragino maru gothic pron', 'hiragino kaku gothic pron')  # macOSフォント
            
            title_font = pygame.font.Font(font_path, 74)
            menu_font = pygame.font.Font(font_path, 48)
        except:
            # フォールバック：システムにインストールされている日本語フォントを使用
            title_font = pygame.font.SysFont('notosanscjk', 74)
            menu_font = pygame.font.SysFont('notosanscjk', 48)
        
        # タイトル
        title = title_font.render("スペースインベーダー", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 100))
        self.screen.blit(title, title_rect)

        # レベル選択メニュー
        levels = [
            "レベル 1: 初級",
            "レベル 2: 中級",
            "レベル 3: 上級",
            "レベル 4: ボス戦"
        ]
        
        for i, text in enumerate(levels):
            level_text = menu_font.render(text, True, (255, 255, 255))
            text_rect = level_text.get_rect(center=(400, 250 + i * 60))
            self.screen.blit(level_text, text_rect)

        # 操作説明
        instruction = menu_font.render("1-4のキーで難易度を選択", True, (255, 255, 255))
        inst_rect = instruction.get_rect(center=(400, 500))
        self.screen.blit(instruction, inst_rect)

        pygame.display.flip()

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                self.level = int(event.unicode)
                self.game_state = "playing"
                self.reset_level()

    def check_collisions(self):
        # パワーアップアイテムとの衝突判定
        for powerup in self.powerups[:]:
            if (powerup.x < self.player.x + self.player.width and
                powerup.x + powerup.width > self.player.x and
                powerup.y < self.player.y + self.player.height and
                powerup.y + powerup.height > self.player.y):
                if powerup.type == 'power':
                    self.player.power_effect = PowerUpEffect('power')
                else:
                    self.player.defense_effect = PowerUpEffect('defense')
                self.powerups.remove(powerup)

        # 敵の弾との衝突判定
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if (bullet.x < self.player.x + self.player.width and
                    bullet.x + bullet.width > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + bullet.height > self.player.y):
                    self.player.take_damage(bullet.damage)
                    bullet.active = False
                    if not self.player.is_alive:
                        self.game_state = "game_over"

        if self.level == 4:
            # ボスの弾との衝突判定
            for bullet in self.boss.bullets[:]:
                if (bullet.x < self.player.x + self.player.width and
                    bullet.x + bullet.width > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + bullet.height > self.player.y):
                    self.player.take_damage(bullet.damage)
                    bullet.active = False
                    if not self.player.is_alive:
                        self.game_state = "game_over"
            
            # プレイヤーの弾とボスの衝突判定を追加
            for bullet in self.player.bullets[:]:
                if (bullet.x < self.boss.x + self.boss.width and
                    bullet.x + bullet.width > self.boss.x and
                    bullet.y < self.boss.y + self.boss.height and
                    bullet.y + bullet.height > self.boss.y):
                    self.boss.take_damage()
                    bullet.active = False
                    self.score += 200
                    if self.boss.health <= 0:
                        self.game_state = "victory"
        else:
            for bullet in self.player.bullets[:]:
                for enemy in self.enemies[:]:
                    if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        dropped_item = enemy.drop_item()
                        if dropped_item:
                            self.powerups.append(dropped_item)
                        self.enemies.remove(enemy)
                        bullet.active = False
                        self.score += 100

    def draw_hud(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        if self.level == 4:
            bullets_text = font.render(f'残弾数: {self.player.bullets_remaining}', True, (255, 255, 255))
            self.screen.blit(bullets_text, (10, 50))
            health_text = font.render(f'ボスHP: {self.boss.health}', True, (255, 255, 255))
            self.screen.blit(health_text, (10, 90))

    def update(self):
        self.player.update()
        if self.level == 4:
            self.boss.update()
        else:
            for enemy in self.enemies:
                enemy.update()
        
        for powerup in self.powerups[:]:
            powerup.update()
            if not powerup.active:
                self.powerups.remove(powerup)
                
        self.check_collisions()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        if self.level == 4:
            self.boss.draw(self.screen)
        else:
            for enemy in self.enemies:
                enemy.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        self.draw_hud()
        pygame.display.flip()

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('GAME OVER', True, (255, 0, 0))
        self.screen.blit(text, (250, 250))
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (300, 350))
        
        restart_text = font.render('Press R to Restart', True, (255, 255, 255))
        self.screen.blit(restart_text, (300, 400))

    def draw_victory(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('VICTORY!', True, (0, 255, 0))
        self.screen.blit(text, (250, 250))
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (300, 350))
        
        restart_text = font.render('Press R to Restart', True, (255, 255, 255))
        self.screen.blit(restart_text, (300, 400))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.game_state == "menu":
                    self.handle_menu_input(event)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    if self.game_state in ["game_over", "victory"]:
                        self.game_state = "menu"
                        self.level = 1
                        self.score = 0
                        self.reset_level()
                else:
                    self.player.handle_event(event)

            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "playing":
                self.update()
                self.draw()
                
                if len(self.enemies) == 0 and self.level < 4:
                    self.level += 1
                    self.reset_level()
                
                if self.level == 4 and self.player.bullets_remaining <= 0:
                    self.game_state = "game_over"
            elif self.game_state == "game_over":
                self.draw_game_over()
            elif self.game_state == "victory":
                self.draw_victory()

            pygame.display.flip()
            self.clock.tick(60) 