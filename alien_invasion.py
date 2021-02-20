import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Inicializa o pygame, as configurações e o objeto screen"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Cria o botão Play
    play_button = Button(ai_settings, screen, "Play")

    # Cria uma instância para armanezar os dados do jogo e cria painel de pontuação
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Cria uma espaçonave, um grupo de projeteis e um grupo de alienigenas
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Cria a frota de alienigenas
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Recupera o recorde para aparecer antes do play do jogador
    # Assim o jogador pode se preparar pra um desafio duro ou fácil
    stats.high_score = gf.recover_high_score()
    sb.prep_high_score()

    # Inicia o laço principal do jogo
    while True:
        # Observa eventos de teclado e de mouse
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            # Deixa a tela mais recente visível
            ship.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        # Atualiza a tela do jogo
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
