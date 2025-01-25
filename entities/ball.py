import pygame
#Classe permettant de générer la balle
class Ball:
    """
    Permet de construire une balle
    @param self : Objet de la classe
    @param config : Configuration du jeux
    """
    def __init__(self, config):
        self.radius = 10 #Taille de la balle

        #Couleur de la balle
        self.color = config.colors["ball"]
        self.config = config
        self.resetPlace() #Initialisation de la balle

    def update(self):
        """
        Méthode permettant de mettre à jour la position de la balle
        @param self : Objet de la classe
        """
        #Déplacement de la balle
        self.x += self.dx
        self.y += self.dy

        # Collision avec les bords de l'écran
        if self.x - self.radius <= 0:  # Collision avec le bord gauche
            self.x = self.radius
            self.dx = -self.dx
        elif self.x + self.radius >= self.config.screenWidth:  # Collision avec le bord droit
            self.x = self.config.screenWidth - self.radius 
            self.dx = -self.dx

        if self.y - self.radius <= self.config.screenHudHeight:  # Collision avec le bord supérieur
            self.y = self.config.screenHudHeight + self.radius
            self.dy = -self.dy

    """
        Permet de dessiner la balle sur l'écran avec la couleur, la position et la taille définie
        @param self : Objet de la classe
        @param screen : Ecran du jeu
    """
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    """
        Permet de réinitialiser la position de la balle
        @param self : Objet de la classe
    """
    def resetPlace(self):
        self.x = self.config.screenWidth // 2 #Position de la balle initial en x
        self.y = self.config.screenHeight - 50 #Position de la balle initial en y
        self.dx = self.dy = 0 #Vitesse de la balle à 0 en début de jeu


    """
        Permet de lancer balle
        @param self : Objet de la classe
    """
    def launchBall(self):
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed