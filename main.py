import sys
import os
import pygame
from config.settings import Config
from core.game import Game

# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Charger les configurations
    config = Config()

    # Créer une instance de jeu
    game = Game(config)

    # Lancer la boucle principale du jeu
    game.run()

    # Quitter Pygame
    pygame.quit()

if __name__ == "__main__":
    main()