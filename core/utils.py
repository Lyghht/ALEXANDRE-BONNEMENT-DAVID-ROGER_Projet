import pygame
from levels.levelLoader import loadLevel
from core.lifeManager import lifeManager

"""
Classe utilitaire pour le jeu
Fonction qu'on utilise un peu partout dans le jeu
En cas de mort ou de victoire
"""
class Utils:
    # Constructeur
    def __init__(self, game):
        self.game = game

    # Fonction pour gérer le reset de la balle et du paddle en cas de mort
    def resetRound(self):
        self.game.ball.resetPlace() 
        self.game.paddle.reset()
        self.game.estEntrainDeJouer = False

        #Affiche le compte à rebours avant de lancer la balle
        self.showCountdown()


    # Fonction pour gérer la remise à zéro du jeu
    def resetGame(self):
        #Reset des variables de jeu
        self.game.estEntrainDeJouer = False
        self.game.score = 0

        # On remet la balle et le paddle à leur place initiale
        self.game.ball.resetPlace()
        self.game.paddle.reset()

        # On recharge les briques
        self.game.bricks = loadLevel(self.game.config, "levels/level1.json")
        self.game.gameLife = lifeManager(self.game.config.initialLife)



    #Permet d'afficher un compte à rebours
    def showCountdown(self, duration=3):
        """
        Affiche un décompte avant de relancer le jeu
        @param duration: Durée du décompte en secondes
        """
        font = pygame.font.Font(None, 100) # Police et taille du texte
        startTime = pygame.time.get_ticks()

        while True:
            currentTime = pygame.time.get_ticks()
            elapsedTime = (currentTime - startTime) / 1000 # Temps écoulé en secondes
            remainingTime = duration - int(elapsedTime) # Temps restant arrondi

            # Si le décompte est terminé, on sort de la boucle
            if remainingTime <= 0:
                break

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    return

            # Mise à jour de l'affichage
            self.game.renderer.renderCountdownFrame(font, remainingTime)