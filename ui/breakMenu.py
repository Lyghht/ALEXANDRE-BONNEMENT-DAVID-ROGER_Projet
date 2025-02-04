import pygame

class BreakMenu:
    """
    Représente une modale de pause

    Paramètres
    ----------
    config : Config
        Classe de configuration du jeu

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
        Surface du titre "Menu Pause"
    titleRect : pygame.Rect
        Rectangle du titre
    soundButton : dict
        Informations du bouton "Son"
    playButton : dict
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
        
        # Polices
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        self.fontTitle = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
        
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
        self.title = self.fontTitle.render("Menu Pause", True, (255, 0, 0))
        self.titleRect = self.title.get_rect(
            centerx=self.modalRect.centerx,
            top=self.modalRect.top + 20
        )
        
        # Boutons
        self.createButtons()

    def createButtons(self):
        """
        Crée les boutons de la modale
        """
        # Bouton Son
        self.soundImages = [
            pygame.image.load("assets/images/soundOn.png"),
            pygame.image.load("assets/images/soundOff.png")
        ]
        self.soundOn = True
        soundImage = self.soundImages[0]
        soundImage = pygame.transform.scale(soundImage, (30, 30))  # Taille des images du bouton Son
        buttonRect = pygame.Rect(
            self.modalRect.left + 10, # Marge de 10 pixels à gauche de la modale
            self.modalRect.bottom - 60,
            soundImage.get_width() + self.padding[0] * 2,
            soundImage.get_height() + self.padding[1] * 2
        )

        self.soundButton = {
            "image": soundImage,
            "rect": buttonRect
        }

        # Bouton Rejouer
        playImage = pygame.image.load("assets/images/play.png")
        playImage = pygame.transform.scale(playImage, (30, 30))  # Taille agrandie du bouton Play
        buttonRect = pygame.Rect(
            0, 0,
            playImage.get_width() + self.padding[0] * 2,
            playImage.get_height() + self.padding[1] * 2
        )
        buttonRect.center = self.modalRect.center  # Position centré de la modale

        self.playButton = {
            "image": playImage,
            "rect": buttonRect
        }

        # Bouton Menu
        homeImage = pygame.image.load("assets/images/home.png")
        homeImage = pygame.transform.scale(homeImage, (30, 30))  # Taille agrandie du bouton Menu
        buttonRect = pygame.Rect(
            self.modalRect.right - (homeImage.get_width() + self.padding[0] * 2) - 10, # Position à droite de la modale
            self.modalRect.bottom - 60,
            homeImage.get_width() + self.padding[0] * 2,
            homeImage.get_height() + self.padding[1] * 2
        )

        self.menuButton = {
            "image": homeImage,
            "rect": buttonRect
        }



    def show(self):
        """
        Affiche la modale avec le score

        Paramètres
        ----------
        score : int
            Score du joueur
        """
        self.visible = True

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
        
        # Boutons
        self.drawButton(screen, self.soundButton)
        self.drawButton(screen, self.playButton)
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
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), button["rect"], 2, border_radius=10)

        # Positionner le texte au centre du bouton si présent (pas d'image) sinon centrer l'image
        if "image" in button:
            imageRect = button["image"].get_rect(center=button["rect"].center)
            screen.blit(button["image"], imageRect.topleft)
        elif "text" in button:
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
            'play' si le bouton rejouer est cliqué
            'menu' si le bouton menu est cliqué
            None sinon
        """
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN:  
            if self.playButton["rect"].collidepoint(event.pos):
                return "play"
            elif self.menuButton["rect"].collidepoint(event.pos):
                return "menu"
            elif self.soundButton["rect"].collidepoint(event.pos):
                self.toogleSound() # Activer ou désactiver le son (visuel)
        
        return None
    
    def toogleSound(self):
        """
        Active ou désactive le son
        """
        self.soundOn = not self.soundOn
        self.soundButton["image"] = self.soundImages[0] if self.soundOn else self.soundImages[1]
        self.soundButton["image"] = pygame.transform.scale(self.soundButton["image"], (30, 30))