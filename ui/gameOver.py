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
    font_title : pygame.font.Font
        Police de caractères pour le titre
    modal_rect : pygame.Rect
        Rectangle de la modale
    title : pygame.Surface
        Surface du titre "Game Over"
    score_text : pygame.Surface
        Surface du texte du score
    retry_button : dict
        Informations du bouton "Rejouer"
    menu_button : dict
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
        modal_width = config.screenWidth // 2
        modal_height = config.screenHeight // 2
        self.padding = (20, 10)
        
        # Rectangle de la modale
        self.modal_rect = pygame.Rect(
            (config.screenWidth - modal_width) // 2,
            (config.screenHeight - modal_height) // 2,
            modal_width,
            modal_height
        )
        
        # Titre
        self.title = self.font_title.render("Game Over", True, (255, 0, 0))
        self.title_rect = self.title.get_rect(
            centerx=self.modal_rect.centerx,
            top=self.modal_rect.top + 20
        )
        
        # Boutons
        button_y = self.modal_rect.centery + 50
        self.create_buttons(button_y)

    def create_buttons(self, base_y):
        """
        Crée les boutons de la modale

        Paramètres
        ----------
        base_y : int
            Position verticale de base pour les boutons
        """
        # Bouton Rejouer
        retry_text = self.font.render("Rejouer", True, (100, 100, 100))
        retry_rect = retry_text.get_rect()
        button_rect = pygame.Rect(0, 0,
                                retry_rect.width + self.padding[0] * 2,
                                retry_rect.height + self.padding[1] * 2)
        button_rect.centerx = self.modal_rect.centerx
        button_rect.centery = base_y
        retry_rect.center = button_rect.center
        
        self.retry_button = {
            "text": retry_text,
            "text_rect": retry_rect,
            "rect": button_rect
        }
        
        # Bouton Menu
        menu_text = self.font.render("Menu", True, (100, 100, 100))
        menu_rect = menu_text.get_rect()
        button_rect = pygame.Rect(0, 0,
                                menu_rect.width + self.padding[0] * 2,
                                menu_rect.height + self.padding[1] * 2)
        button_rect.centerx = self.modal_rect.centerx
        button_rect.centery = base_y + 50
        menu_rect.center = button_rect.center
        
        self.menu_button = {
            "text": menu_text,
            "text_rect": menu_rect,
            "rect": button_rect
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
        self.score_text = self.font.render(f"Score:{score}", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(
            centerx=self.modal_rect.centerx,
            centery=self.modal_rect.centery - 20
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
        pygame.draw.rect(screen, (50, 50, 50), self.modal_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), self.modal_rect, 2, border_radius=15)
        
        # Titre
        screen.blit(self.title, self.title_rect)
        
        # Score
        screen.blit(self.score_text, self.score_rect)
        
        # Boutons
        self.drawButton(screen, self.retry_button)
        self.drawButton(screen, self.menu_button)

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
        screen.blit(button["text"], button["text_rect"])

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
            if self.retry_button["rect"].collidepoint(event.pos):
                return "retry"
            elif self.menu_button["rect"].collidepoint(event.pos):
                return "menu"
        if self.visible and event.type == pygame.MOUSEMOTION:
            if self.retry_button["rect"].collidepoint(event.pos):
                self.retry_button["text"] = self.font.render("Rejouer", True, (0, 0, 0))
            else:
                self.retry_button["text"] = self.font.render("Rejouer", True, (100, 100, 100))
            if self.menu_button["rect"].collidepoint(event.pos):
                self.menu_button["text"] = self.font.render("Menu", True, (0, 0, 0))
            else:
                self.menu_button["text"] = self.font.render("Menu", True, (100, 100, 100))
        
        return None