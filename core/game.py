import pygame
from entities.paddle import Paddle
from entities.ball import Ball
from levels.levelLoader import loadLevel

# Classe représentant le jeu
class Game:
    """
    Représente le jeu
    @param self: Objet de la classe
    @param config: Configuration du jeu
    """
    def __init__(self, config):
        # Initialiser Pygame
        self.config = config
        self.screen = pygame.display.set_mode((config.screenWidth, config.screenHeight))
        pygame.display.set_caption("Casse-Brique")
        self.clock = pygame.time.Clock()

        # Initialise les entités du jeu
        self.paddle = Paddle(config)
        self.ball = Ball(config)
        self.bricks = loadLevel(config, "levels/level1.json")

    """
    Permet de lancer le jeu
    @param self: Objet de la classe
    """
    def run(self):
        # Boucle principale du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Met à jours les éléments du jeu
            self.update()

            # Affiche les éléments du jeu
            self.render()

            # Permet de limiter les FPS
            self.clock.tick(self.config.fps)

        pygame.quit()

    """
    Permet de mettre à jour les éléments du jeu graphiquement
    @param self: Objet de la classe
    """
    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.update(keys) # Met à jour la position du paddle
        self.ball.update() # Met à jour la position de la balle
        self.check_collisions() # Vérifie les collisions

    """
    Permet d'afficher les éléments du jeu
    @param self: Objet de la classe
    """
    def render(self):
        # Affiche les éléments du jeu
        self.screen.fill(self.config.bgColor)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Affiche les briques
        for brick in self.bricks:
            brick.draw(self.screen)

        # Rafraichit l'écran
        pygame.display.flip()

    """
    Permet de vérifier les collisions entre les éléments du jeu
    @param self: Objet de la classe
    """
    def check_collisions(self):
        # Collision balle-paddle
        if self.ball.y + self.ball.radius >= self.paddle.y and self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width:
            self.ball.dy = -self.ball.dy

        # Collision balle-briques
        for brick in self.bricks:
            if brick.isActive and brick.rect.collidepoint(self.ball.x, self.ball.y):
                brick.isActive = False
                self.ball.dy = -self.ball.dy
                break