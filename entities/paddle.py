# entities/paddle.py
import pygame

class Paddle:
    """
    
    Classe représentant la barre de jeu
    @param config: Configuration du jeu
    @param self : Barre de jeu

    """
    def __init__(self, config): #Initialisation de la barre
        self.width = 100 #Largeur de la barre
        self.height = 20 #Hauteur de la barre
        self.color = config.colors["paddle"] #Couleur de la barre
        self.speed = config.paddleSpeed #Vitesse de la barre
        self.config = config #Configuration du jeu
        self.reset()

    def update(self, keys): # Deplacement de la barre
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed # Déplacement de la barre à gauche
        if keys[pygame.K_RIGHT] and self.x < self.config.screenWidth - self.width:
            self.x += self.speed # Déplacement de la barre à droite

    def draw(self, screen): # Affichage de la barre
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = (self.config.screenWidth - self.width) // 2
        self.y = self.config.screenHeight - 40