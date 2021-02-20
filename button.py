import pygame.font


class Button:
    """Estabelece um botão de play do jogo"""
    def __init__(self, ai_settings, screen, msg):
        """Inicializa as configurações do botão"""
        self.ai_settings = ai_settings
        self.screen = screen

        self.screen_rect = self.screen.get_rect()

        # Define as dimensões e propriedades dos botões
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Constroi o objeto rect e o centraliza
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # A mensagem do botão deve ser preparada apenas uma vez
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Transforma msg em imagem e renderiza no centro de button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Desenha um botão em branco e , em seguida, desenha o botão com a mensagem"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
