# entities/brick.py
import pygame
import random
from entities.Bonus import Bonus

class Brick:
    """
    Classe représentant une brique

    ...

    Attributs
    ----------
    rect : pygame.Rect
        rectangle représentant la brique
    color : tuple
        couleur de la brique
    life : int
        nombre de coups restants avant destruction
    isActive : bool
        indique si la brique est active ou non

    Méthodes
    -------
    draw(screen)
        Dessine la brique sur l'écran
    hit()
        Réduit le nombre de coups restants avant destruction de la brique
    hit(damage)
        Réduit le nombre de coups restants avant destruction de la brique en fonction des dégâts infligés
    """

    def __init__(self, x, y, width, height, life, config):
        """
        Constructeur de la classe Brick

        Paramètres
        ----------
        x : int
            position x de la brique
        y : int
            position y de la brique
        width : int
            largeur de la brique
        height : int
            hauteur de la brique
        life : int
            nombre de coups restants avant destruction
        """
        # Initialisation des attributs
        self.life = life
        self.config = config
        self.isActive = True

        # Création du rectangle représentant la brique
        self.rect = pygame.Rect(x, y, width, height)

        # Chargement des images des briques
        self.brickImages = {
            life: pygame.transform.scale(pygame.image.load(config.images[f"brick{life}"]), (width, height))
            for life in range(1, self.config.maxBrickLife + 1)
        }
        self.image = self.brickImages[self.life]

        # Sons de collision avec une brique
        self.brickHitSound = pygame.mixer.Sound(self.config.sounds["brickHit"])
        self.brickFallSound = pygame.mixer.Sound(self.config.sounds["brickFall"])

    def draw(self, screen):
        """
        Dessine la brique sur l'écran

        Paramètres
        ----------
        screen : pygame.Surface
            écran sur lequel dessiner la brique
        """
        if self.isActive:
            # Dessin de la brique
            screen.blit(self.image, self.rect)

    
    def hit(self, bonuses, damage=1):
        """
        Réduit le nombre de coups restants avant destruction de la brique

        Paramètres
        ----------
        bonuses : list
        damage : int
            nombre de coups à retirer à la brique
        """
        self.life -= damage

        if self.life <= 0:
            self.brickFallSound.play() # Son de destruction de la brique
            self.isActive = False
            self.generateBonus(bonuses)
        else:
            # Mise à jour de l'image de la brique
            self.image = self.brickImages[self.life]
            self.brickHitSound.play()

    def generateBonus(self, bonuses):
        """
        Génère un bonus aléatoire lorsque la brique est détruite

        Paramètres
        ----------
        bonuses : list
            liste des bonus
        """
        if random.random() < self.config.bonusProbability:
            bonus_type = random.choice(["doubleBar"])
            bonus = Bonus(self.rect.x, self.rect.y, 20, 20, bonus_type)
            bonuses.append(bonus)