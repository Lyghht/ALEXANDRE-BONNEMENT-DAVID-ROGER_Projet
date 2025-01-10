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
        self.reset() #Initialisation de la balle

    """
        Méthode permettant de mettre à jour la position de la balle
        @param self : Objet de la classe
    """
    def update(self):
        #Déplacement de la balle
        self.x += self.dx
        self.y += self.dy

        # Collision avec les bords de l'écran
        if self.x <= 0 or self.x >= self.config.screenWidth:
            self.dx = -self.dx
        if self.y <= 0:
            self.dy = -self.dy

    """
        Permet de dessiner la balle sur l'écran avec la couleur, la position et la taille définie
        @param self : Objet de la classe
        @param screen : Ecran du jeu
    """
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.config.screenWidth // 2 #Position de la balle initial en x
        self.y = self.config.screenHeight // 2 #Position de la balle initial en y

        #Vitesse de la balle
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed

