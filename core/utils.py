import pygame
import math
from levels.levelLoader import loadLevel
from core.lifeManager import lifeManager
from levels import levelGenerator

"""
Classe utilitaire pour le jeu
Fonction qu'on utilise un peu partout dans le jeu
En cas de mort ou de victoire
"""
class Utils:
    # Constructeur
    def __init__(self, game):
        self.game = game

    # Fonction pour gérer le reset de la balle et du paddle en cas de mort
    def resetRound(self):
        self.game.ball.cancelAllBonuses()
        self.game.paddle.cancelAllBonuses()
        self.game.ball.resetPlace() 
        self.game.paddle.reset()
        self.game.isPlaying = False
        self.unuseAllBonuses()


        #Affiche le compte à rebours avant de lancer la balle
        self.showCountdown()


    # Fonction pour gérer la remise à zéro du jeu
    def resetGame(self):
        #Reset des bonus
        self.game.ball.cancelAllBonuses()
        self.game.paddle.cancelAllBonuses()

        #Reset des variables de jeu
        self.game.isPlaying = False
        self.game.score = self.game.config.initialScore
        self.game.level = self.game.config.initialLevel


        # On remet la balle et le paddle à leur place initiale
        self.unuseAllBonuses()
        self.game.ball.resetPlace()
        self.game.paddle.reset()

        # On recharge les briques
        layout = levelGenerator.generateLevels(self.game.level)
        self.game.bricks = loadLevel(self.game.config, layout)
        self.game.gameLife = lifeManager(self.game.config.initialLife)
        
        # On recharge l'hud
        self.game.hud.reset(self.game.score, self.game.level)
    
    def checkVictory(self):
        """
        Vérifie si le joueur a gagné
        """
        count = 0
        # On compte le nombre de briques restantes
        for brick in self.game.bricks:
            if brick.life > 0:
                count += 1
        
        # Si il n'y a plus de briques, on passe au niveau suivant
        if count == 0:
            self.unuseAllBonuses()
            # On incrémente le niveau
            self.game.level += 1

            # On met à jour l'hud
            self.game.hud.updateLevel(self.game.level)
            if self.game.gameLife.getLife() < self.game.config.initialLife:
                self.game.gameLife.addLife()
            self.game.hud.updateLives(self.game.gameLife.getLife())
            
            # On recharge les briques
            layout = levelGenerator.generateLevels(self.game.level)
            self.game.bricks = loadLevel(self.game.config, layout)

            # On remet la balle et le paddle à leur place initiale
            self.game.isPlaying = False
            self.game.ball.resetPlace()
            self.game.paddle.reset()

            self.game.renderer.render()
            self.showCountdown()

    def circleRectCollision(self, rectangle):
        """
        Vérifie la collision entre un cercle et un rectangle
        @param circle: Cercle
        @param rectangle: Rectangle
        @return: True si collision détectée
        """
        ball = self.game.ball
        closestX = max(rectangle.left, min(ball.x, rectangle.right))
        closestY = max(rectangle.top, min(ball.y, rectangle.bottom))
        
        #Permet de calculer la distance
        distance = math.sqrt((ball.x - closestX) ** 2 + (ball.y - closestY) ** 2)
        
        return distance < ball.radius + 2 #On ajoute 2 pour corriger un bug de collision

    #Permet d'afficher un compte à rebours
    def showCountdown(self, duration=3):
        """
        Affiche un décompte avant de relancer le jeu
        @param duration: Durée du décompte en secondes
        """
        font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 40)
        startTime = pygame.time.get_ticks()

        while True:
            currentTime = pygame.time.get_ticks()
            elapsedTime = (currentTime - startTime) / 1000 # Temps écoulé en secondes
            remainingTime = duration - int(elapsedTime) # Temps restant arrondi

            # Si le décompte est terminé, on sort de la boucle
            if remainingTime <= 0:
                break

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    return

            # Mise à jour de l'affichage
            self.game.renderer.renderCountdownFrame(font, remainingTime)

    def unuseAllBonuses(self):
        for bonus in self.game.bonuses:
            bonus.isActive = False
            bonus.undraw(self.game.screen)
        self.game.bonuses = []