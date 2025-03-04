import pygame
import threading

class Paddle:
    def __init__(self, config):
        self.width = 100
        self.height = 20
        self.speed = config.paddleSpeed
        self.config = config

        self.reversedControlsCounter = 0
        self.sizeMultiplier = 1  # Garde une trace de la taille courante

        self.reset()

        self.image = pygame.transform.scale(pygame.image.load(config.images["paddle"]), (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.reversedControlThreads = []
        self.sizeChangeThreads = []

    def update(self, keys):
        """Déplacement de la barre avec gestion des contrôles inversés."""
        if self.reversedControlsCounter > 0:
            if keys[pygame.K_LEFT] and self.x < self.config.screenWidth - self.width:
                self.x += self.speed
            if keys[pygame.K_RIGHT] and self.x > 0:
                self.x -= self.speed
        else:
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < self.config.screenWidth - self.width:
                self.x += self.speed

    def draw(self, screen):
        """Dessine la barre sur l'écran."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, self.rect)

    def reset(self):
        """Réinitialisation de la barre."""
        self.x = (self.config.screenWidth - self.width) // 2
        self.y = self.config.screenHeight - 40

    def doubleBarre(self):
        """Double la taille de la barre pendant 15 secondes (effet cumulatif)."""
        self.sizeMultiplier *= 1.5
        self.updateSize()

        stopEvent = threading.Event()
        self.sizeChangeThreads.append(stopEvent)
        threading.Thread(target=self.resetSize, args=(stopEvent, 1/1.5)).start()

    def semiBarre(self):
        """Réduit la taille de la barre pendant 15 secondes (effet cumulatif)."""
        self.sizeMultiplier *= 0.5
        self.updateSize()

        stopEvent = threading.Event()
        self.sizeChangeThreads.append(stopEvent)
        threading.Thread(target=self.resetSize, args=(stopEvent, 2)).start()

    def updateSize(self):
        """Met à jour la taille de la barre en fonction du multiplicateur."""
        self.width = int(100 * self.sizeMultiplier)
        self.image = pygame.transform.scale(pygame.image.load(self.config.images["paddle"]), (self.width, self.height))

    def resetSize(self, stopEvent, ratio):
        """Réinitialise la taille après expiration du bonus."""
        for _ in range(150):
            if stopEvent.is_set():
                return
            pygame.time.wait(100)

        self.sizeMultiplier *= ratio
        self.updateSize()

    def reversedControls(self):
        """Inverse les contrôles de la barre pendant 15 secondes."""
        self.reversedControlsCounter += 1

        stopEvent = threading.Event()
        self.reversedControlThreads.append(stopEvent)
        threading.Thread(target=self.resetControls, args=(stopEvent,)).start()

    def resetControls(self, stopEvent):
        """Réinitialise les contrôles après expiration du bonus."""
        for _ in range(100):
            if stopEvent.is_set():
                return
            pygame.time.wait(100)

        self.reversedControlsCounter -= 1

    def cancelAllBonuses(self):
        """Annule immédiatement tous les effets actifs."""
        self.reversedControlsCounter = 0
        self.sizeMultiplier = 1

        # Stopper tous les threads actifs
        for stopEvent in self.reversedControlThreads + self.sizeChangeThreads:
            stopEvent.set()

        self.reversedControlThreads.clear()
        self.sizeChangeThreads.clear()

        self.updateSize()