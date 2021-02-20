import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza as posições dos projeteis e elimina os antigos."""
    # Atualiza as posições dos projeteis
    bullets.update()

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Livra-se dos projeteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum projétil atingiu o alienigena, caso positivo ele elimina o projetil e o alien"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Atualiza o score a cada colisão
    for alien in collisions.values():
        if collisions:
            stats.score += ai_settings.alien_points
    sb.prep_score()

    check_high_score(stats, sb)

    # Se o grupo aliens zerar é criado um novo nível com uma nova grade de aliens e sem projeteis
    if len(aliens) == 0:
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Cria uma nova grade de aliens, limpa os projeteis da tela e inicia um novo nível"""
    bullets.empty()
    ai_settings.increase_speed()
    create_fleet(ai_settings, screen, ship, aliens)
    # Aumenta o nível
    stats.level += 1
    sb.prep_level()


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde a eventos de pressionamento de tecla e mouse."""
    if event.key == pygame.K_RIGHT:
        # Move a espaçonave para a direita
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move a espaçonave para a esquerda
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Dispara o projetil
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        # Salva o High_score em um arquivo externo
        quit_game(stats)
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """"Dispara um projétil se o limite ainda não foi alcançado."""""
    # Cria um novo projétil e o adiciona ao grupo
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)


def check_keyup_events(event, ship):
    """Responde a soltura de teclas."""
    if event.key == pygame.K_RIGHT:
        # Interrompe o moving_right quando solta a tecla
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Interrompe o moving_left quando solta a tecla
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a eventos de pressionamento de tecla e mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Salva o High_score em um arquivo externo
            quit_game(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def quit_game(stats):
    """Salva a pontuação máxima e sai do jogo"""
    filename = "high_score.txt"

    with open(filename, "w") as file_object:
        file_object.write(str(stats.high_score))

    # Sai do jogo
    sys.exit()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Checa se o usuário clicou na área do botão play"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Inicia um novo jogo quando o usuário clica em play"""
    # Recupera a pontuação máxima
    stats.high_score = recover_high_score()
    # Reseta as configurações de velocidade do jogo
    ai_settings.initialize_dynamic_settings()
    # Oculta o cursor do Mouse
    pygame.mouse.set_visible(False)
    # Reseta os dados estatísticos do jogo
    stats.reset_stats()
    stats.game_active = True
    # Prepara as imagens de pontuação
    sb.prep_scoreboard_images()
    # Esvazia as listas de aliens e bullets
    aliens.empty()
    bullets.empty()
    # Cria uma nova frota e centraliza a espaçonave
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def recover_high_score():
    """Recupera a pontuação máxima do jogo ao ser inicializado"""
    # Recupera o high_score do arquivo txt
    filename = "high_score.txt"
    try:
        with open(filename, "r") as file_object:
            lista = file_object.read()
            return int(lista)
    except IOError:
        return 0


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem
    screen.fill(ai_settings.bg_color)

    # Redesenha os projeteis atras das espaçonaves e dos alienigenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Desenha a espaçonave
    ship.blitme()
    # Desenha o alienigena
    aliens.draw(screen)

    # Mostra a pontuação do jogo
    sb.show_score()
    # Desenha o botão Play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente visível
    pygame.display.flip()


def check_high_score(stats, sb):
    """Verifica se há um novo recorde."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    sb.prep_high_score()


def get_number_alien_x(ai_settings, alien_width):
    """Calcula o numero de alienigenas em um linha na tela"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calcula o numero de linhas com alienigenas que cabem na tela"""
    available_space_y = ai_settings.screen_height - ((3 * alien_height) - ship_height)
    number_rows = available_space_y // (2 * alien_height)
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Cria um alienigena e o posiciona na linha."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de alienigenas"""
    # Cria um alienigena e calcula o numero de alienigenas em uma linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_alien_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Cria a primeira linha de alienigenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alien atinge a borda"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Faz a frota descer e muda a sua direção"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Atualiza as posições dos aliens."""
    # Checa e altera caso a frota de aliens atinja a borda
    check_fleet_edges(ai_settings, aliens)
    # Verifica se um alien atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # Verifica se um alien atingiu a nave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # Mostra a ultima posição dos aliens
    aliens.update()


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Verifica se algum alien atingiu a parte inferior da tela"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Então faremos o mesmo quando a nave é atingida, chamamos ship_hit
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Responde ao fato de a nave ter sido atingido por um alien"""
    if stats.ships_left > 0:
        # Decrementa ships_left
        stats.ships_left -= 1

        # Atualiza o painel de pontuações
        sb.prep_ships()

        # Esvazia a lista de bullets e alien
        bullets.empty()
        aliens.empty()

        # Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa
        sleep(0.5)
    else:
        stats.game_active = False
        # Retorna a exibição do cursor do Mouse
        pygame.mouse.set_visible(True)
