import pygame

class HUD:
    """
    Classe représentant l'interface utilisateur du jeu
    """

    def __init__(self, config, score, level):
        """
        Constructeur de la classe HUD

        Paramètres
        ----------
        config : Config
            Configuration du jeu
        """
        self.config = config
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        self.score = score
        self.level = level
        self.lives = config.initialLife

    def draw(self, screen):
        """
        Dessine l'interface utilisateur sur l'écran

        Paramètres
        ----------
        screen : pygame.Surface
            écran sur lequel dessiner l'interface utilisateur
        """
        # Score
        scoreText = self.font.render(f"Score:{self.score}", True, (255, 255, 255))
        screen.blit(scoreText, (10, 10))

        # Niveau
        levelText = self.font.render(f"Niveau:{self.level}", True, (255, 255, 255))
        screen.blit(levelText, (self.config.screenWidth // 2 - levelText.get_width() // 2, 10))

        # Vies
        livesText = self.font.render(f"Vies:{self.lives}", True, (255, 255, 255))
        screen.blit(livesText, (self.config.screenWidth - 10 - livesText.get_width(), 10))

        # Ligne de séparation
        lineWidth = 5
        pygame.draw.line(screen, (255, 255, 255), (0, self.config.screenHudHeight - lineWidth + 1), (self.config.screenWidth, self.config.screenHudHeight - lineWidth + 1), lineWidth)


    def updateScore(self, score):
        """
        Met à jour le score

        Paramètres
        ----------
        score : int
            Score du joueur
        """
        self.score = score

    def updateLives(self, lives):
        """
        Met à jour le nombre de vies

        Paramètres
        ----------
        lives : int
            Nombre de vies restantes
        """
        self.lives = lives

    def updateLevel(self, level):
        """
        Met à jour le niveau

        Paramètres
        ----------
        level : int
            Niveau actuel
        """
        self.level = level

    def reset(self, score=0, level=1):
        """
        Réinitialise l'interface utilisateur
        """
        self.score = score
        self.level = level
        self.lives = self.config.initialLife