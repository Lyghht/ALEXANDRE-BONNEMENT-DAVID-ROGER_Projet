import pygame
#Classe permettant de générer la balle
class Ball:
    #Constructeur de la classe
    def __init__(self, config):
        self.radius = 10 #Taille de la balle
        self.x = config.screenWidth // 2 #Position de la balle initial en x
        self.y = config.screenHeight // 2 #Position de la balle initial en y

        #Vitesse de la balle
        self.dx = config.ballSpeed
        self.dy = -config.ballSpeed

        #Couleur de la balle
        self.color = config.colors["ball"]
        self.config = config

    #Méthode permettant de mettre à jour la position de la balle
    def update(self):
        #Déplacement de la balle
        self.x += self.dx
        self.y += self.dy

        # Collision avec les bords de l'écran
        if self.x <= 0 or self.x >= self.config.screenWidth:
            self.dx = -self.dx
        if self.y <= 0:
            self.dy = -self.dy

    #Permet de dessiner la balle sur l'écran avec la couleur, la position et la taille définie
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)