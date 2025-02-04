# entities/paddle.py
import pygame
import threading

class Paddle:
    """
    
    Classe représentant la barre de jeu
    @param config: Configuration du jeu
    @param self : Barre de jeu

    """
    def __init__(self, config): #Initialisation de la barre
        self.width = 100 #Largeur de la barre
        self.height = 20 #Hauteur de la barre
        self.speed = config.paddleSpeed #Vitesse de la barre
        self.config = config #Configuration du jeu
        self.reset()

        self.image = pygame.transform.scale(pygame.image.load(config.images["paddle"]), (self.width, self.height)) #Chargement de l'image de la barre
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #Création du rectangle de la barre

    def update(self, keys): # Deplacement de la barre
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed # Déplacement de la barre à gauche
        if keys[pygame.K_RIGHT] and self.x < self.config.screenWidth - self.width:
            self.x += self.speed # Déplacement de la barre à droite

    def draw(self, screen): # Affichage de la barre
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, self.rect)

    def reset(self):
        self.x = (self.config.screenWidth - self.width) // 2
        self.y = self.config.screenHeight - 40

    def doubleBarre(self):
        def reset_width():
            pygame.time.wait(15000)
            self.width = self.width // 1.5
            self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

        threading.Thread(target=reset_width).start()
        self.width = self.width * 1.5
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

    def semiBarre(self):
        def reset_width():
            pygame.time.wait(15000)
            self.width = self.width // 0.5
            self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

        threading.Thread(target=reset_width).start()
        self.width = self.width * 0.5
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))