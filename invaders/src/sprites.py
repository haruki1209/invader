import pygame
import math

def create_player_sprite():
    surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    # 宇宙船の本体（三角形）
    pygame.draw.polygon(surface, (0, 255, 0), [(25, 0), (0, 50), (50, 50)])
    # コックピット
    pygame.draw.circle(surface, (100, 255, 100), (25, 30), 10)
    # エンジン炎
    pygame.draw.polygon(surface, (255, 165, 0), [(15, 50), (35, 50), (25, 60)])
    return surface

def create_enemy_sprite():
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    # UFOの本体
    pygame.draw.ellipse(surface, (255, 0, 0), (0, 15, 40, 15))
    # コックピット
    pygame.draw.ellipse(surface, (200, 200, 200), (10, 10, 20, 25))
    # 光
    pygame.draw.circle(surface, (255, 255, 0), (20, 22), 5)
    return surface

def create_boss_sprite():
    surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    
    # 魔王の体（マント）
    pygame.draw.polygon(surface, (100, 0, 0), [
        (20, 40),  # 左肩
        (80, 40),  # 右肩
        (90, 100), # 右下
        (10, 100)  # 左下
    ])
    
    # 頭部
    pygame.draw.circle(surface, (150, 0, 0), (50, 35), 25)
    
    # 角（より大きく、威圧的に）
    pygame.draw.polygon(surface, (50, 0, 0), [
        (30, 20),  # 左角基部
        (15, -5),  # 左角先端
        (35, 25)   # 左角内側
    ])
    pygame.draw.polygon(surface, (50, 0, 0), [
        (70, 20),  # 右角基部
        (85, -5),  # 右角先端
        (65, 25)   # 右角内側
    ])
    
    # 目（より邪悪に）
    # 左目
    pygame.draw.circle(surface, (255, 0, 0), (35, 35), 8)  # 赤い外枠
    pygame.draw.circle(surface, (255, 255, 0), (35, 35), 6)  # 黄色い部分
    pygame.draw.circle(surface, (0, 0, 0), (35, 35), 3)  # 黒い瞳
    
    # 右目
    pygame.draw.circle(surface, (255, 0, 0), (65, 35), 8)  # 赤い外枠
    pygame.draw.circle(surface, (255, 255, 0), (65, 35), 6)  # 黄色い部分
    pygame.draw.circle(surface, (0, 0, 0), (65, 35), 3)  # 黒い瞳
    
    # 口（より邪悪な笑みに）
    pygame.draw.arc(surface, (200, 0, 0), (30, 35, 40, 30), 0, math.pi, 4)
    
    # 装飾（王冠）
    crown_points = [(35, 15), (50, 5), (65, 15), (60, 20), (50, 15), (40, 20)]
    pygame.draw.polygon(surface, (255, 215, 0), crown_points)  # 金色の王冠
    
    # 宝石の装飾
    pygame.draw.circle(surface, (255, 0, 0), (50, 12), 3)  # 中央の赤い宝石
    pygame.draw.circle(surface, (0, 0, 255), (40, 17), 2)  # 左の青い宝石
    pygame.draw.circle(surface, (0, 255, 0), (60, 17), 2)  # 右の緑の宝石
    
    # マントの装飾
    pygame.draw.line(surface, (255, 215, 0), (30, 45), (70, 45), 3)  # 金のライン
    pygame.draw.circle(surface, (255, 215, 0), (50, 60), 5)  # 中央の飾り
    
    return surface

def create_enemy_bullet():
    surface = pygame.Surface((8, 15), pygame.SRCALPHA)
    # 赤い光線
    pygame.draw.polygon(surface, (255, 0, 0), [(4, 0), (0, 15), (8, 15)])
    return surface

def create_power_up():
    surface = pygame.Surface((20, 20), pygame.SRCALPHA)
    # パワーアップアイテム（赤い星）
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2
        radius = 10 if i % 2 == 0 else 5
        points.append((
            10 + radius * math.cos(angle),
            10 + radius * math.sin(angle)
        ))
    pygame.draw.polygon(surface, (255, 0, 0), points)
    return surface

def create_defense_up():
    surface = pygame.Surface((20, 20), pygame.SRCALPHA)
    # 防御アップアイテム（青い盾）
    pygame.draw.polygon(surface, (0, 0, 255), [(10, 0), (20, 5), (20, 15), (10, 20), (0, 15), (0, 5)])
    return surface 