import pygame
from core.path import resourcePath

class Menu:
    """
    Représente le menu du jeu

    Attributs
    ----------
    config : Config
        Configuration du jeu
    font : pygame.font.Font
        Police de caractères
    title :
        Titre du jeu
    title_rect : pygame.Rect
        Rectangle contenant le titre
    play :
        Bouton pour lancer le jeu
    play_rect : pygame.Rect
        Rectangle contenant le bouton pour lancer le jeu
    quit :
        Bouton pour quitter le jeu
    quit_rect : pygame.Rect
        Rectangle contenant le bouton pour quitter le jeu
    """
    def __init__(self, config):
        """
        Constructeur de la classe Menu
        """
        self.config = config
        self.font = pygame.font.Font(resourcePath("assets/fonts/PressStart2P-Regular.ttf"), 20)
        self.font_play = pygame.font.Font(resourcePath("assets/fonts/PressStart2P-Regular.ttf"), 30)
        self.font_title = pygame.font.Font(resourcePath("assets/fonts/PressStart2P-Regular.ttf"), 40)
        self.padding = (20, 20)  # (padding_x, padding_y) pour le texte des boutons

        # Titre
        self.title = self.font_title.render("Casse Brique", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(config.screenWidth // 2, 100))

        # Création des boutons avec padding
        self.createButton("Jouer", config.screenHeight // 2)
        self.createButton("Quitter", config.screenHeight - 70, is_quit=True)

    def createButton(self, text, y_pos, is_quit=False):
        """
        Crée un bouton avec le texte centré

        Paramètres
        ----------
        text : str
            Texte du bouton
        y_pos : int
            Position verticale du bouton
        is_quit : bool
            Indique si c'est le bouton quitter
        """
        # Création du texte
        if is_quit:
            rendered_text = self.font.render(text, True, (100, 100, 100))
        else:
            rendered_text = self.font_play.render(text, True, (100, 100, 100))
        text_rect = rendered_text.get_rect()
        
        # Création du rectangle du bouton avec padding
        button_rect = pygame.Rect(0, 0, 
                                text_rect.width + self.padding[0] * 2,
                                text_rect.height + self.padding[1] * 2)
        
        # Centrage du rectangle du bouton
        button_rect.center = (self.config.screenWidth // 2, y_pos)
        
        # Centrage du texte dans le rectangle du bouton
        text_rect.center = button_rect.center

        if is_quit:
            self.quit = rendered_text
            self.quit_rect = button_rect
            self.quit_text_rect = text_rect
        else:
            self.play = rendered_text
            self.play_rect = button_rect
            self.play_text_rect = text_rect

    def draw(self, screen):
        """
        Dessine le menu sur l'écran

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner le menu
        """
        # Dessiner le titre
        screen.blit(self.title, self.title_rect)

        # Dessiner les boutons
        self.drawButton(screen, self.play_rect, self.play, self.play_text_rect)
        self.drawButton(screen, self.quit_rect, self.quit, self.quit_text_rect)

    def drawButton(self, screen, button_rect, text, text_rect):
        """
        Dessine un bouton avec son texte centré

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner
        button_rect : pygame.Rect
            Rectangle du bouton
        text : pygame.Surface
            Surface contenant le texte
        text_rect : pygame.Rect
            Rectangle du texte
        """
        pygame.draw.rect(screen, (255, 255, 255), button_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2, border_radius=10)
        screen.blit(text, text_rect)

    def handleEvent(self, event):
        """
        Gère les événements du menu

        Paramètres
        ----------
        event : pygame.event.Event
            Evénement à gérer
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                return "play"
            elif self.quit_rect.collidepoint(event.pos):
                return "quit"
        if event.type == pygame.MOUSEMOTION:
            if self.play_rect.collidepoint(event.pos):
                self.play = self.font_play.render("Jouer", True, (0, 0, 0))
            else:
                self.play = self.font_play.render("Jouer", True, (100, 100, 100))
            if self.quit_rect.collidepoint(event.pos):
                self.quit = self.font.render("Quitter", True, (0, 0, 0))
            else:
                self.quit = self.font.render("Quitter", True, (100, 100, 100))
        return None