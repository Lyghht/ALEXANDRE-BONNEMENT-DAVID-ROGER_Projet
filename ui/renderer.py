import pygame
import core.game as gameFile

class Renderer:
    """
    Classe pour gérer le rendu du jeu
    """
    def __init__(self, game):
        self.game = game


    def render(self):
        """
        Affiche les éléments du jeu
        """
        if self.game.state == gameFile.GameState.PLAYING:
            self.renderGame()
        # Ajout des états particuliers (GAME_OVER ou PAUSED)
        elif self.game.state == gameFile.GameState.GAME_OVER:
            self.renderGame() # Affiche les éléments du jeu car GAME_OVER est une modale
            self.renderGameOver()
        elif self.game.state == gameFile.GameState.PAUSED:
            self.renderGame() # Affiche les éléments du jeu car PAUSED est une modale
            self.renderBreakMenu()
        elif self.game.state == gameFile.GameState.MENU:
            self.renderMenu()

        pygame.display.update()


    def renderMenu(self):
        """
        Affiche le menu principal
        """
        self.game.screen.fill(self.game.config.bgColorMenu)
        self.game.menu.draw(self.game.screen)


    def renderGame(self):
        """
        Affiche les éléments du jeu en cours de partie
        """
        self.game.screen.fill(self.game.config.bgColor)
        self.game.paddle.draw(self.game.screen)  # Affiche le paddle
        self.game.ball.draw(self.game.screen)  # Affiche la balle
        self.game.hud.draw(self.game.screen)

        # Affiche les briques
        for brick in self.game.bricks:
            brick.draw(self.game.screen)

        # Affiche les bonus
        for bonus in self.game.bonuses:
            bonus.draw(self.game.screen)


    def renderGameOver(self):
        """
        Affiche l'écran de fin de partie
        """
        self.game.gameOverMenu.show(self.game.score) # Affiche l'écran de fin de partie avec le score
        self.game.gameOverMenu.draw(self.game.screen)
    
    def renderBreakMenu(self):
        """
        Affiche le menu de pause
        """
        self.game.breakMenu.draw(self.game.screen)
        self.game.breakMenu.show()


    def renderCountdownFrame(self, font, remainingTime):
        """
        Affiche le décompte
        @param font: Police du texte
        @param remainingTime: Temps restant
        """
        countdownText = font.render(str(remainingTime), True, (255, 255, 255))
        textRect = countdownText.get_rect(center=(self.game.config.screenWidth // 2, self.game.config.screenHeight // 2))

        # Affiche le décompte avec un rectangle noir pour pas voir les autres éléments en dessous
        pygame.draw.rect(self.game.screen, (0, 0, 0), (textRect.x - 10, textRect.y - 10, textRect.width + 20, textRect.height + 20))
        self.game.screen.blit(countdownText, textRect)

        pygame.display.update()
