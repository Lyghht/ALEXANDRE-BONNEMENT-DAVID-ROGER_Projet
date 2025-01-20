# entities/brick.py
import pygame

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
        
    def hit(self):
        """
        Réduit le nombre de coups restants avant destruction de la brique
        """
        self.life -= 1

        self.color = self.config.colors["brick" + str(self.life)]


        if self.life == 0:
            self.isActive = False
    
    def hit(self, damage):
        """
        Réduit le nombre de coups restants avant destruction de la brique

        Paramètres
        ----------
        damage : int
            nombre de coups à retirer à la brique
        """
        self.life -= damage

        self.color = self.config.colors["bricks" + str(self.life)]

        if self.life <= 0:
            self.isActive = False