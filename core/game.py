import pygame
import math
from entities.paddle import Paddle
from entities.ball import Ball
from levels.levelLoader import loadLevel
from ui.menu import Menu
from core.lifeManager import lifeManager
from ui.gameOver import GameOverMenu
from enum import Enum
from core.utils import Utils
from ui.renderer import Renderer
from levels import levelGenerator

class GameState(Enum):
    """
    Enumération des états du jeu

    Attributs
    ----------
    MENU : int
        Menu principal
    PLAYING : int
        En train de jouer
    PAUSED : int
        En pause
    GAME_OVER : int
        Écran de fin de partie
    """
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


# Classe représentant le jeu
class Game:
    """
    Représente le jeu
    @param self: Objet de la classe
    @param config: Configuration du jeu

    Attributs
    ----------
    config : Config
        Configuration du jeu
    screen : pygame.Surface
        Surface de l'écran
    clock : pygame.time.Clock
        Horloge pour gérer les FPS
    state : GameState
        État du jeu
    running : bool
        État du jeu
    menu : Menu
        Menu principal
    gameOverMenu : GameOverMenu
        Écran de fin de partie
    paddle : Paddle
        Paddle du jeu
    ball : Ball
        Balle du jeu
    bricks : list
        Liste des briques
    gameLife : lifeManager
        Gestionnaire de vies
    estEntrainDeJouer : bool
        Indique si la balle est en mouvement
    score : int
        Score du joueur
    """
    def __init__(self, config):
        # Initialisation de Pygame et des éléments du jeu
        self.config = config
        self.screen = pygame.display.set_mode((config.screenWidth, config.screenHeight))
        pygame.display.set_caption("Casse-Brique")
        self.clock = pygame.time.Clock()

        # État du jeu
        self.state = GameState.MENU
        self.running = True

        # Initialisation des éléments du jeu
        self.menu = Menu(config)
        self.gameOverMenu = GameOverMenu(config)
        self.paddle = Paddle(config)
        self.ball = Ball(config)
        layout = levelGenerator.generateLevels()
        self.bricks = loadLevel(config, layout)
        self.gameLife = lifeManager(config.initialLife)

        # Variables de jeu
        self.estEntrainDeJouer = False
        self.score = 0

        self.utils = Utils(self)

        # Initialisation du renderer
        self.renderer = Renderer(self)

    def run(self):
        """
        Lance la boucle principale du jeu

        @param self: Objet de la classe
        """
        while self.running:
            # Gestion des événements, mise à jour et rendu
            self.handleEvents()
            self.update()
            self.renderer.render()
            self.clock.tick(self.config.fps)

        pygame.quit()

    def update(self):
        """
        Met à jour les éléments du jeu
        """
        if self.state == GameState.PLAYING:
            self.updateGame()

    def updateGame(self):
        """
        Met à jour les éléments du jeu en cours de partie
        """
        keys = pygame.key.get_pressed()
        self.paddle.update(keys) # Met à jour la position du paddle
        if ((keys[pygame.K_LEFT]) or (keys[pygame.K_RIGHT])) and not self.estEntrainDeJouer:
            self.ball.launchBall()
            self.estEntrainDeJouer = True

        self.ball.update() # Met à jour la position de la balle
        self.checkCollisions() # Vérifie les collisions

    def checkCollisions(self):
        """
        Vérifie et gère toutes les collisions du jeu
        @return: True si le jeu continue, False si game over
        """
        if self.checkPaddleCollision() or self.checkBrickCollisions():
            return True

        return self.handleBottomCollision()

    def checkPaddleCollision(self):
        """
        Vérifie la collision entre la balle et le paddle
        @return: True si collision détectée
        """
        if self.utils.circleRectCollision(self.paddle.rect):
            self.ball.dy = -self.ball.dy
            return True
        return False

    def checkBrickCollisions(self):
        """
        Vérifie la collision entre la balle et les briques
        @return: True si collision détectée
        """
        for brick in self.bricks:
            if brick.isActive and self.utils.circleRectCollision(brick.rect):
                brick.hit()
                self.ball.dy = -self.ball.dy
                self.score += 10
                return True
        return False

    def handleEvents(self):
        """
        Gère les événements du jeu
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == GameState.MENU:
                self.handleMenuEvents(event)
            elif self.state == GameState.GAME_OVER:
                self.handleGameOverEvents(event)

    def handleMenuEvents(self, event):
        """
        Gère les événements du menu principal
        @param event: Événement Pygame
        """
        action = self.menu.handleEvent(event)
        if action == "play":
            self.state = GameState.PLAYING
            self.utils.resetGame()
        elif action == "quit":
            self.running = False

    def handleGameOverEvents(self, event):
        """
        Gère les événements de l'écran de fin de partie
        @param event: Événement Pygame
        """
        action = self.gameOverMenu.handleEvent(event)
        if action == "retry":
            self.gameOverMenu.hide() # Cache l'écran de fin de partie
            self.state = GameState.PLAYING
            self.utils.resetGame()
        elif action == "menu":
            self.gameOverMenu.hide() # Cache l'écran de fin de partie
            self.state = GameState.MENU

    def handleBottomCollision(self):
        """
        Gère la collision avec le bord bas de l'écran
        @return: True si le jeu continue, False si game over
        """
        if self.ball.y >= self.config.screenHeight:
            if self.gameLife.loseLife():
                self.utils.resetRound()
                return True
            else:
                self.state = GameState.GAME_OVER
                return False
        return True