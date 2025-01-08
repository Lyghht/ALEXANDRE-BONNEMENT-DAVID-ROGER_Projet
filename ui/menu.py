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

    Methodes
    ----------
    draw(screen)
        Dessine le menu sur l'écran
    handle_event(event)
        Gère les événements du menu
    """
    def __init__(self, config):
        """
        Constructeur de la classe Menu
        """
        self.config = config
        self.font = pygame.font.Font(None, 36)
        self.title = self.font.render("Casse Brique", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(config.screenWidth // 2, config.screenHeight // 2 - 50))
        self.play = self.font.render("Jouer", True, (255, 255, 255))
        self.play_rect = self.play.get_rect(center=(config.screenWidth // 2, config.screenHeight // 2 + 50))
        self.quit = self.font.render("Quitter", True, (255, 255, 255))
        self.quit_rect = self.quit.get_rect(center=(config.screenWidth // 2, config.screenHeight // 2 + 100))

    def draw(self, screen):
        """
        Dessine le menu sur l'écran

        Parametres
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner le menu
        """
        screen.blit(self.title, self.title_rect)
        screen.blit(self.play, self.play_rect)
        screen.blit(self.quit, self.quit_rect)

    def handle_event(self, event):
        """
        Gère les événements du menu
        
        Parametres
        ----------
        event : pygame.event.Event
            Evénement à gérer
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                return "play"
            elif self.quit_rect.collidepoint(event.pos):
                return "quit"
        return None