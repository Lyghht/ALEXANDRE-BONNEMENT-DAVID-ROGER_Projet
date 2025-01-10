import pygame
from entities.paddle import Paddle
from entities.ball import Ball
from levels.levelLoader import loadLevel
from ui.menu import Menu
from core.lifeManager import lifeManager

# Classe représentant le jeu
class Game:
    #Permet de savoir si le joueur est en train de jouer ou pas
    estEntrainDeJouer = False

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

        # Initialise le menu
        self.menu = Menu(config)

        # Initialise les entités du jeu
        self.paddle = Paddle(config)
        self.ball = Ball(config)
        self.bricks = loadLevel(config, "levels/level1.json")
        self.gameLife = lifeManager(config.initialLife)

    """
    Permet de lancer le jeu
    @param self: Objet de la classe
    """
    def run(self):
        """
        Permet de lancer le jeu
        """
        # Affiche d'abord le menu
        if not self.show_menu():
            pygame.quit()
            return  # Quitte si l'utilisateur sélectionne "Quitter"

        # Boucle principale du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Met à jour les éléments du jeu
            self.update()

            # Affiche les éléments du jeu
            self.render()

            # Permet de limiter les FPS
            self.clock.tick(self.config.fps)

        pygame.quit()
    
    def show_menu(self):
        """
        Affiche le menu principal
        @return: True si le joueur veut jouer, False s'il veut quitter
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Quitter le jeu

                # Gère les interactions avec le menu
                action = self.menu.handle_event(event)
                if action == "play":
                    return True  # Lancer le jeu
                elif action == "quit":
                    return False  # Quitter le jeu

            # Dessine le menu
            self.screen.fill(self.config.bgColorMenu) # Couleur de fond
            self.menu.draw(self.screen)
            pygame.display.flip()  # Rafraîchit l'écran

    """
    Permet de mettre à jour les éléments du jeu graphiquement
    @param self: Objet de la classe
    """
    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.update(keys) # Met à jour la position du paddle
        if ((keys[pygame.K_LEFT]) or (keys[pygame.K_RIGHT])) and not self.estEntrainDeJouer:
            self.ball.launchBall()
            self.estEntrainDeJouer = True
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
        
        #Regarde la collision avec le bord bas de l'écran
        if self.ball.y >= self.config.screenHeight:
            if self.gameLife.loseLife(): #Si le joueur a encore des vies
                self.ball.resetPlace()
                self.paddle.reset()
                self.estEntrainDeJouer = False
            else: #Sinon la partie est perdue
                self.show_menu() #A revoir après