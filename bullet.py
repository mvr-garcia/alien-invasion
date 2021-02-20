import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Classe que administra os projeteis disparados"""
    def __init__(self, ai_settings, screen, ship):
        """Cria um projetil para a posição atual da nave"""
        super().__init__()
        self.screen = screen

        # Cria um retangulo para o projetil em (0,0) e define a posição correta
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Armazena a posição do projetil com um valor decimal
        self.y = float(self.rect.y)

        # Caracteristicas do projetil
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move o projétil pra cima na tela"""
        # Atualiza a posição do projétil na tela
        self.y -= self.speed_factor

        # Atualiza a posição do rect
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o projétil na tela"""
        pygame.draw.rect(self.screen, self.color, self.rect)
