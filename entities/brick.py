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

    def __init__(self, x, y, width, height, color, life, config):
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
        color : tuple
            couleur de la brique
        life : int
            nombre de coups restants avant destruction
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.life = life
        self.config = config
        self.isActive = True

    def draw(self, screen):
        """
        Dessine la brique sur l'écran

        Paramètres
        ----------
        screen : pygame.Surface
            écran sur lequel dessiner la brique
        """
        if self.isActive:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)  # Bordure noire
    
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
            self.isActive = False
            self.generateBonus(bonuses)
        else:
            self.color = self.config.colors["brick" + str(self.life)]

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