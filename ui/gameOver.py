import pygame
from core.path import resourcePath

class GameOverMenu:
    """
    Représente une modale de Game Over

    Attributs
    ----------
    config : Config
        Configuration du jeu
    font : pygame.font.Font
        Police de caractères pour le texte
    fontTitle : pygame.font.Font
        Police de caractères pour le titre
    modalRect : pygame.Rect
        Rectangle de la modale
    title : pygame.Surface
        Surface du titre "Game Over"
    scoreText : pygame.Surface
        Surface du texte du score
    retryButton : dict
        Informations du bouton "Rejouer"
    menuButton : dict
        Informations du bouton "Menu"
    visible : bool
        État de visibilité de la modale
    """
    
    def __init__(self, config):
        """
        Initialise la modale de Game Over

        Paramètres
        ----------
        config : Config
            Classe de configuration du jeu
        """
        self.config = config
        self.visible = False
        self.score = 0
        
        # Polices
        self.font = pygame.font.Font(resourcePath("assets/fonts/PressStart2P-Regular.ttf"), 20)
        self.font_title = pygame.font.Font(resourcePath("assets/fonts/PressStart2P-Regular.ttf"), 30)
        
        # Dimensions de la modale
        modalWidth = config.screenWidth // 2
        modalHeight = config.screenHeight // 2
        self.padding = (20, 10)
        
        # Rectangle de la modale
        self.modalRect = pygame.Rect(
            (config.screenWidth - modalWidth) // 2,
            (config.screenHeight - modalHeight) // 2,
            modalWidth,
            modalHeight
        )
        
        # Titre
        self.title = self.fontTitle.render("Game Over", True, (255, 0, 0))
        self.titleRect = self.title.get_rect(
            centerx=self.modalRect.centerx,
            top=self.modalRect.top + 20
        )
        
        # Boutons
        buttonY = self.modalRect.centery + 50
        self.create_buttons(buttonY)

    def create_buttons(self, baseY):
        """
        Crée les boutons de la modale

        Paramètres
        ----------
        baseY : int
            Position verticale de base pour les boutons
        """
        # Bouton Rejouer
        retryText = self.font.render("Rejouer", True, (100, 100, 100))
        retryRect = retryText.get_rect()
        buttonRect = pygame.Rect(0, 0,
                                retryRect.width + self.padding[0] * 2,
                                retryRect.height + self.padding[1] * 2)
        buttonRect.centerx = self.modalRect.centerx
        buttonRect.centery = baseY
        retryRect.center = buttonRect.center
        
        self.retryButton = {
            "text": retryText,
            "textRect": retryRect,
            "rect": buttonRect
        }
        
        # Bouton Menu
        menuText = self.font.render("Menu", True, (100, 100, 100))
        menuRect = menuText.get_rect()
        buttonRect = pygame.Rect(0, 0,
                                menuRect.width + self.padding[0] * 2,
                                menuRect.height + self.padding[1] * 2)
        buttonRect.centerx = self.modalRect.centerx
        buttonRect.centery = baseY + 50
        menuRect.center = buttonRect.center
        
        self.menuButton = {
            "text": menuText,
            "textRect": menuRect,
            "rect": buttonRect
        }

    def show(self, score):
        """
        Affiche la modale avec le score

        Paramètres
        ----------
        score : int
            Score du joueur
        """
        self.visible = True
        self.score = score
        self.scoreText = self.font.render(f"Score:{score}", True, (255, 255, 255))
        self.scoreRect = self.scoreText.get_rect(
            centerx=self.modalRect.centerx,
            centery=self.modalRect.centery - 20
        )

    def hide(self):
        """
        Cache la modale
        """
        self.visible = False

    def draw(self, screen):
        """
        Dessine la modale si elle est visible

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner
        """
        if not self.visible:
            return
            
        # Fond semi-transparent
        s = pygame.Surface((self.config.screenWidth, self.config.screenHeight))
        s.fill((0, 0, 0))
        s.set_alpha(128)
        screen.blit(s, (0, 0))
        
        # Fond de la modale
        pygame.draw.rect(screen, (50, 50, 50), self.modalRect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), self.modalRect, 2, border_radius=15)
        
        # Titre
        screen.blit(self.title, self.titleRect)
        
        # Score
        screen.blit(self.scoreText, self.scoreRect)
        
        # Boutons
        self.drawButton(screen, self.retryButton)
        self.drawButton(screen, self.menuButton)

    def drawButton(self, screen, button):
        """
        Dessine un bouton

        Paramètres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner
        button : dict
            Dictionnaire contenant les informations du bouton
        """
        pygame.draw.rect(screen, (255, 255, 255), button["rect"], border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=10)
        screen.blit(button["text"], button["textRect"])

    def handleEvent(self, event):
        """
        Gère les événements de la modale

        Paramètres
        ----------
        event : pygame.event.Event
            Événement à gérer

        Retour
        -------
        str ou None
            'retry' si le bouton rejouer est cliqué
            'menu' si le bouton menu est cliqué
            None sinon
        """
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN:  
            if self.retryButton["rect"].collidepoint(event.pos):
                return "retry"
            elif self.menuButton["rect"].collidepoint(event.pos):
                return "menu"
        if self.visible and event.type == pygame.MOUSEMOTION:
            if self.retryButton["rect"].collidepoint(event.pos):
                self.retryButton["text"] = self.font.render("Rejouer", True, (0, 0, 0))
            else:
                self.retryButton["text"] = self.font.render("Rejouer", True, (100, 100, 100))
            if self.menuButton["rect"].collidepoint(event.pos):
                self.menuButton["text"] = self.font.render("Menu", True, (0, 0, 0))
            else:
                self.menuButton["text"] = self.font.render("Menu", True, (100, 100, 100))
        
        return None