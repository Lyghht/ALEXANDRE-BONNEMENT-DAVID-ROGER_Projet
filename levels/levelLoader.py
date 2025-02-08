import json
from entities.brick import Brick

def loadLevel(config, layout):
    """
        Fonction qui permet de charger un niveau
        @param config: Configuration du jeu
        @return: Liste de briques
    """
    bricks = [] #Permet de créer une liste de bricks vide, c'est elle qui va contenir les briques du niveau
    numColumns = len(layout[0]) #Nombre de colonnes sur la grille
    brickWidth = config.screenWidth // numColumns #Division entière pour obtenir la largeur des briques
    brickHeight = 20

    for rowIndex, row in enumerate(layout): #Parcours de chaque ligne de la grille
        for colIndex, cell in enumerate(row): #Parcours de chaque colonne de la grille
            if cell > 0:
                x = colIndex * brickWidth
                y = rowIndex * brickHeight + config.screenHudHeight
                bricks.append(Brick(x, y, brickWidth, brickHeight, cell, config)) #Ajout de la brique à la liste de briques

    return bricks