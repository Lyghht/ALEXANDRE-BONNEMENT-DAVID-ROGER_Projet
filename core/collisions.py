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
            impactRelative = (self.game.ball.x - paddleCenter) / (self.game.paddle.width) # Permet de calculer si l'angle est positif ou négatif
            # Calcul de l'angle de rebond en radians pour la balle
            angle = 90 - (impactRelative * self.game.config.bounceAngle)
            angle = math.radians(angle)
            
            print("angle", angle)
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
            # Si la brique est active et qu'il y a collision
            if brick.isActive and self.game.utils.circleRectCollision(brick.rect):
                brickLeft = brick.rect.x
                brickRight = brick.rect.x + brick.rect.width
                brickTop = brick.rect.y
                brickBottom = brick.rect.y + brick.rect.height

                # Position future de la balle
                ballNextX = self.game.ball.x + self.game.ball.dx
                ballNextY = self.game.ball.y + self.game.ball.dy

                # Vérification de la collision en fonction de la direction de la balle
                if ballNextY - self.game.ball.radius <= brickTop and self.game.ball.dy > 0:
                    # Collision par le haut
                    self.game.ball.dy = -abs(self.game.ball.dy)
                elif ballNextY + self.game.ball.radius >= brickBottom and self.game.ball.dy < 0:
                    # Collision par le bas
                    self.game.ball.dy = abs(self.game.ball.dy)
                elif ballNextX - self.game.ball.radius <= brickLeft and self.game.ball.dx > 0:
                    # Collision par la gauche
                    self.game.ball.dx = -abs(self.game.ball.dx)
                elif ballNextX + self.game.ball.radius >= brickRight and self.game.ball.dx < 0:
                    # Collision par la droite
                    self.game.ball.dx = abs(self.game.ball.dx)
                brick.hit()                
                self.game.score += 10 # Ajout de 10 points au score
                self.game.hud.updateScore(self.game.score)
                return True
        return False
    
    def handleBottomCollision(self):
        """
        Gère la collision avec le bord bas de l'écran
        @return: True si le jeu continue, False si game over
        """
        # Si la balle touche le bas de l'écran
        if self.game.ball.y + 15 >= self.game.config.screenHeight:
            if self.game.gameLife.loseLife(): # Si le joueur a encore des vies	
                self.game.hud.updateLives(self.game.gameLife.getLife())
                self.game.utils.resetRound() # Réinitialisation de la balle et du paddle
                return True
            else: # Si le joueur n'a plus de vie	
                self.game.hud.updateLives(self.game.gameLife.getLife())
                self.game.state = gameFile.GameState.GAME_OVER # Passage à l'état de game over
                return False
        return True