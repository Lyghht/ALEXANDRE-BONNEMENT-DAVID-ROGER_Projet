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
        self.config = config
        self.screen = pygame.display.set_mode((config.screenWidth, config.screenHeight))
        pygame.display.set_caption("Casse-Brique")
        self.clock = pygame.time.Clock()

        # Initialiser les entités du jeu
        self.paddle = Paddle(config)
        self.ball = Ball(config)
        self.bricks = loadLevel(config, "levels/level1.json")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mise à jour des éléments du jeu
            self.update()

            # Affichage des éléments du jeu
            self.render()

            # Limiter les FPS
            self.clock.tick(self.config.fps)

        pygame.quit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.update(keys)
        self.ball.update()
        self.check_collisions()

    def render(self):
        self.screen.fill(self.config.bgColor)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        pygame.display.flip()

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