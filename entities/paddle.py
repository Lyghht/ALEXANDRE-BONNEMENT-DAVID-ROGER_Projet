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
        self.areControlsReversed = False
        self.reset()

        self.image = pygame.transform.scale(pygame.image.load(config.images["paddle"]), (self.width, self.height)) #Chargement de l'image de la barre
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #Création du rectangle de la barre

    def update(self, keys):
        """
        Déplacement de la barre
        @param keys : touches du clavier
        """
        if self.areControlsReversed: #Si les contrôles sont inversés	
            if keys[pygame.K_LEFT] and self.x < self.config.screenWidth - self.width:
                self.x += self.speed
            if keys[pygame.K_RIGHT] and self.x > 0:
                self.x -= self.speed
        else: #Sinon contrôles normaux
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.speed # Déplacement de la barre à gauche
            if keys[pygame.K_RIGHT] and self.x < self.config.screenWidth - self.width:
                self.x += self.speed # Déplacement de la barre à droite
            

    def draw(self, screen):
        """
        Dessin de la barre
        @param screen : écran de jeu
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, self.rect)

    def reset(self):
        """
        Réinitialisation de la barre
        """
        self.x = (self.config.screenWidth - self.width) // 2 #Position de la barre
        self.y = self.config.screenHeight - 40 #Position de la barre

    def doubleBarre(self):
        """
        Double la taille de la barre
        """

        threading.Thread(target=self.resetWidth, args=(2/3,)).start()
        self.width = self.width * 1.5 # Augmentation de la taille de la barre
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))


    def semiBarre(self):
        """
        Réduit la taille de la barre
        """
        threading.Thread(target=self.resetWidth, args=(2,)).start()
        self.width = self.width * 0.5 # Réduction de la taille de la barre
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

    def resetWidth(self, ratio):
        """
        Réinitialisation de la taille de la barre
        """
        pygame.time.wait(15000)
        self.width = self.width * ratio # Réinitialisation de la taille de la barre
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

    def reversedControls(self):
        """
        Inversion des contrôles
        """
        threading.Thread(target=self.resetControls).start()
        self.areControlsReversed = True 

    def resetControls(self):
        """
        Réinitialisation des contrôles
        """
        pygame.time.wait(15000)
        self.areControlsReversed = False
