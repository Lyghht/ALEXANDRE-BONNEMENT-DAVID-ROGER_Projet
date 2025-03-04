import pygame

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
    titleRect : pygame.Rect
        Rectangle contenant le titre
    play :
        Bouton pour lancer le jeu
    playRect : pygame.Rect
        Rectangle contenant le bouton pour lancer le jeu
    quit :
        Bouton pour quitter le jeu
    quitRect : pygame.Rect
        Rectangle contenant le bouton pour quitter le jeu
    """
    def __init__(self, config):
        """
        Constructeur de la classe Menu
        """
        self.config = config
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        self.fontPlay = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
        self.fontTitle = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 40)
        self.padding = (20, 20)  # (padding_x, padding_y) pour le texte des boutons

        # Titre
        self.title = self.fontTitle.render("Casse Brique", True, (255, 255, 255))
        self.titleRect = self.title.get_rect(center=(config.screenWidth // 2, 100))

        # Création des boutons avec padding
        self.createButton("Jouer", config.screenHeight // 2)
        self.createButton("Quitter", config.screenHeight - 70, isQuit=True)

    def createButton(self, text, yPos, isQuit=False):
        """
        Crée un bouton avec le texte centré

        Paramètres
        ----------
        text : str
            Texte du bouton
        yPos : int
            Position verticale du bouton
        isQuit : bool
            Indique si c'est le bouton quitter
        """
        # Création du texte
        if isQuit:
            renderedText = self.font.render(text, True, (100, 100, 100))
        else:
            renderedText = self.fontPlay.render(text, True, (100, 100, 100))
        textRect = renderedText.get_rect()
        
        # Création du rectangle du bouton avec padding
        buttonRect = pygame.Rect(0, 0,
                                textRect.width + self.padding[0] * 2,
                                textRect.height + self.padding[1] * 2)
        
        # Centrage du rectangle du bouton
        buttonRect.center = (self.config.screenWidth // 2, yPos)
        
        # Centrage du texte dans le rectangle du bouton
        textRect.center = buttonRect.center

        if isQuit:
            self.quit = renderedText
            self.quitRect = buttonRect
            self.quit_textRect = textRect
        else:
            self.play = renderedText
            self.playRect = buttonRect
            self.play_textRect = textRect

    def draw(self, screen):
        """
        Dessine le menu sur l'écran

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner le menu
        """
        # Dessiner le titre
        screen.blit(self.title, self.titleRect)

        # Dessiner les boutons
        self.drawButton(screen, self.playRect, self.play, self.play_textRect)
        self.drawButton(screen, self.quitRect, self.quit, self.quit_textRect)

    def drawButton(self, screen, buttonRect, text, textRect):
        """
        Dessine un bouton avec son texte centré

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner
        buttonRect : pygame.Rect
            Rectangle du bouton
        text : pygame.Surface
            Surface contenant le texte
        textRect : pygame.Rect
            Rectangle du texte
        """
        pygame.draw.rect(screen, (255, 255, 255), buttonRect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), buttonRect, 2, border_radius=10)
        screen.blit(text, textRect)

    def handleEvent(self, event):
        """
        Gère les événements du menu

        Paramètres
        ----------
        event : pygame.event.Event
            Evénement à gérer
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playRect.collidepoint(event.pos):
                return "play"
            elif self.quitRect.collidepoint(event.pos):
                return "quit"
        if event.type == pygame.MOUSEMOTION:
            if self.playRect.collidepoint(event.pos):
                self.play = self.fontPlay.render("Jouer", True, (0, 0, 0))
            else:
                self.play = self.fontPlay.render("Jouer", True, (100, 100, 100))
            if self.quitRect.collidepoint(event.pos):
                self.quit = self.font.render("Quitter", True, (0, 0, 0))
            else:
                self.quit = self.font.render("Quitter", True, (100, 100, 100))
        return None