import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Classe que representa um único alienigena da frota."""
    def __init__(self, ai_settings, screen):
        """Inicializa o alienigena e define sua posição inicial."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem do alienigena e obtém o seu rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Inicia cada alienigena na parte superior esquerda da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição exata do alienigena
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retorna True se os aliens atingiram a borda da tela"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move o alien para a direita ou a esquerda"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Desenha o alienigena em sua posição atual."""
        self.screen.blit(self.image, self.rect)
