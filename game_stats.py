class GameStats:
    """Armazena dados estatísticos da Alian Invasion"""
    def __init__(self, ai_settings):
        """Inicialia os dados estatísticos"""
        self.ai_settings = ai_settings

        # Inicia a Alian Invasion em um estado inativo
        self.game_active = False

        self.reset_stats()

        # A pontuação máxima jamais deverá ser reiniciada
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Inicializa os dados estatisticos que podem mudar durante o jogo."""
        self.ships_left = self.ai_settings.ships_limit
        self.score = 0
        self.level = 1
