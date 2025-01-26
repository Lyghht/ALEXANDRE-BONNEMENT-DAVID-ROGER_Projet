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
        self.config = config

        #Couleur de la balle
        self.color = config.colors["ball"]

        #Chargement de l'image de la balle
        self.imageOriginal = pygame.image.load(config.images["ball"])

        # Pré-calcul des images pour 360 angles
        self.precomputedImages = [
            pygame.transform.rotate(self.imageOriginal, angle) for angle in range(360)
        ]

        # Initialisation pour la rotation
        self.image = self.imageOriginal
        self.angle = 0  # Angle de rotation initial
        self.rotation_speed = 100  # Vitesse de rotation (en degrés/frame)

        self.resetPlace() #Initialisation de la balle

    def update(self, isPlaying):
        """
        Méthode permettant de mettre à jour la position de la balle
        @param self : Objet de la classe
        """
        # Si le jeu n'est pas en cours, on ne met pas à jour la balle
        if not isPlaying:
            return
        
        #Déplacement de la balle
        self.x += self.dx
        self.y += self.dy

        # Mise à jour de l'angle
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = self.precomputedImages[self.angle]

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
        # Calculer la position pour centrer l'image
        rotated_rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rotated_rect.topleft)

    """
        Permet de réinitialiser la position de la balle
        @param self : Objet de la classe
    """
    def resetPlace(self):
        self.x = self.config.screenWidth // 2 #Position de la balle initial en x
        self.y = self.config.screenHeight - 50 #Position de la balle initial en y
        self.dx = self.dy = 0 #Vitesse de la balle à 0 en début de jeu
        self.angle = 0 #Angle de rotation de la balle à 0
        self.image = self.imageOriginal #Image de la balle
        

    """
        Permet de lancer balle
        @param self : Objet de la classe
    """
    def launchBall(self):
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed