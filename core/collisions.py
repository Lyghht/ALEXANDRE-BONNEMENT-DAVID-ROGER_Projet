import pygame
import math
import core.game as gameFile

"""
Classe qui permet de gérer les collisions
"""

class Collisions:
    """
    Constructeur
    @param self: Objet de la classe
    @param game: Objet de la classe Game
    """
    def __init__(self, game):
        self.game = game

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
        if self.game.utils.circleRectCollision(self.game.paddle.rect):
            paddleCenter = self.game.paddle.x + self.game.paddle.width / 2
            impactRelative = (self.game.ball.x - paddleCenter) / (self.game.paddle.width / 2) # Permet de calculer si l'angle est positif ou négatif
            # Calcul de l'angle de rebond en radians pour la balle
            angle = 90 - (impactRelative * self.game.config.bounceAngle)
            angle = math.radians(angle)
            
            # Calcul de la vitesse de la balle
            speed = math.sqrt(self.game.ball.dx ** 2 + self.game.ball.dy ** 2)

            # Mise à jour de la vitesse de la balle
            self.game.ball.dx = speed * math.cos(angle)
            self.game.ball.dy = -speed * math.sin(angle)

            return True
        return False

    def checkBrickCollisions(self):
        """
        Vérifie la collision entre la balle et les briques
        @return: True si collision détectée
        """
        for brick in self.game.bricks:
            if brick.isActive and self.game.utils.circleRectCollision(brick.rect):
                self.game.ball.dy = -self.game.ball.dy
                brick.hit()                
                self.game.score += 10
                self.game.hud.updateScore(self.game.score)
                return True
        return False
    
    def handleBottomCollision(self):
        """
        Gère la collision avec le bord bas de l'écran
        @return: True si le jeu continue, False si game over
        """
        if self.game.ball.y + 15 >= self.game.config.screenHeight:
            if self.game.gameLife.loseLife():
                self.game.hud.updateLives(self.game.gameLife.getLife())
                self.game.utils.resetRound()
                return True
            else:
                self.game.hud.updateLives(self.game.gameLife.getLife())
                self.game.state = gameFile.GameState.GAME_OVER
                return False
        return True