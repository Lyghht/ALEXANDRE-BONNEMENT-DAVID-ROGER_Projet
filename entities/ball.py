import threading

import pygame
#Classe permettant de générer la balle
class Ball:

    def __init__(self, config):
        """
        Permet de construire une balle
        @param self : Objet de la classe
        @param config : Configuration du jeux
        """
        self.radius = 10 #Taille de la balle
        self.config = config

        self.speedBallCounter = 0

        self.damage = 1 #Dégâts de la balle

        #Chargement de l'image de la balle
        self.imageOriginal = pygame.image.load(config.images["ball"])

        # Pré-calcul des images pour 360 angles
        self.precomputedImages = [
            pygame.transform.rotate(self.imageOriginal, angle) for angle in range(360)
        ]

        # Initialisation pour la rotation
        self.image = self.imageOriginal
        self.angle = 0  # Angle de rotation initial
        self.rotationSpeed = 5  # Vitesse de rotation (en degrés/frame)
        self.slowBallCounter = 0

        self.resetPlace() #Initialisation de la balle

        self.slowBallCounter = 0
        self.speedBallCounter = 0
        
        self.slowBallStopEvent = threading.Event()  # Flag pour stopper les ralentissements
        self.slowBallThreads = []
        self.speedBallThreads = []
        self.explosiveBallThreads = []

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
        self.angle = (self.angle + self.rotationSpeed) % 360
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


    def draw(self, screen):
        """
            Permet de dessiner la balle sur l'écran avec la couleur, la position et la taille définie
            @param self : Objet de la classe
            @param screen : Ecran du jeu
        """
        # Calculer la position pour centrer l'image
        rotated_rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rotated_rect.topleft)


    def resetPlace(self):
        """
            Permet de réinitialiser la position de la balle
            @param self : Objet de la classe
        """
        self.x = self.config.screenWidth // 2 #Position de la balle initial en x
        self.y = self.config.screenHeight - 50 #Position de la balle initial en y
        self.dx = self.dy = 0 #Vitesse de la balle à 0 en début de jeu
        self.angle = 0 #Angle de rotation de la balle à 0
        self.image = self.imageOriginal #Image de la balle
        

    def launchBall(self):
        """
            Permet de lancer la balle
        :return:
        """
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed

    def slowBall(self):
        """
        Active un ralentissement de la balle pendant 15 secondes.
        Chaque appel ajoute un ralentissement supplémentaire (effet cumulatif).
        """
        self.slowBallCounter += 1

        # Appliquer le ralentissement immédiatement
        slowFactor = 1 / 1.2  # Facteur de ralentissement
        self.dx *= slowFactor
        self.dy *= slowFactor
        self.rotationSpeed = max(1, self.rotationSpeed - 1)

        # Créer un thread qui restaurera progressivement la vitesse après 15s
        stopEvent = threading.Event()
        self.slowBallThreads.append(stopEvent)
        threading.Thread(target=self.resetSlow, args=(stopEvent,)).start()

    def resetSlow(self, stopEvent):
        """
        Attend 15 secondes avant d'annuler un ralentissement spécifique.
        """
        for _ in range(150):  # Attendre 15 secondes en vérifiant toutes les 100ms
            if stopEvent.is_set():  # Si on annule tout, on arrête immédiatement
                return
            pygame.time.wait(100)

        # Un ralentissement se termine
        self.slowBallCounter -= 1
        if self.slowBallCounter >= 0:  # S'il reste des ralentissements, ajuster la vitesse
            restoreFactor = 1.2  # Facteur pour retrouver la vitesse normale
            self.dx *= restoreFactor
            self.dy *= restoreFactor
            self.rotationSpeed = min(5, self.rotationSpeed + 1)
    
    def cancelSlowBall(self):
        """
        Annule immédiatement tous les ralentissements en cours.
        """
        print("Cancel slow ball")
        self.slowBallCounter = 0
        for stopEvent in self.slowBallThreads:
            stopEvent.set()  # Arrêter tous les threads actifs
        self.slowBallThreads.clear()

        # Rétablir la vitesse initiale immédiatement
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed
        self.rotationSpeed = 5

    def speedBall(self):
        """Active un boost de vitesse cumulatif pendant 10 secondes."""
        self.speedBallCounter += 1
        speedFactor = 1.2
        self.dx *= speedFactor
        self.dy *= speedFactor
        self.rotationSpeed = min(15, self.rotationSpeed + 2)

        stopEvent = threading.Event()
        self.speedBallThreads.append(stopEvent)
        threading.Thread(target=self.resetSpeed, args=(stopEvent,)).start()

    def resetSpeed(self, stopEvent):
        """Attend 10s avant d'annuler un boost de vitesse spécifique."""
        for _ in range(100):
            if stopEvent.is_set():
                return
            pygame.time.wait(100)

        self.speedBallCounter -= 1
        if self.speedBallCounter >= 0:
            restoreFactor = 1 / 1.2
            self.dx *= restoreFactor
            self.dy *= restoreFactor
            self.rotationSpeed = max(5, self.rotationSpeed - 2)

    def explosiveBall(self):
        """Active un boost de dégâts pendant 10 secondes."""
        self.damage += 10

        stopEvent = threading.Event()
        self.explosiveBallThreads.append(stopEvent)
        threading.Thread(target=self.resetExplosive, args=(stopEvent,)).start()

    def resetExplosive(self, stopEvent):
        """Attend 10s avant de réinitialiser les dégâts."""
        for _ in range(100):
            if stopEvent.is_set():
                return
            pygame.time.wait(100)

        self.damage = max(1, self.damage - 10)

    def cancelAllBonuses(self):
        """Annule immédiatement tous les effets actifs."""
        self.slowBallCounter = 0
        self.speedBallCounter = 0
        self.damage = 1

        # Stopper tous les threads actifs
        for stopEvent in self.slowBallThreads + self.speedBallThreads + self.explosiveBallThreads:
            stopEvent.set()
        
        self.slowBallThreads.clear()
        self.speedBallThreads.clear()
        self.explosiveBallThreads.clear()

        # Réinitialiser la vitesse
        self.dx = self.config.ballSpeed
        self.dy = -self.config.ballSpeed
        self.rotationSpeed = 5
