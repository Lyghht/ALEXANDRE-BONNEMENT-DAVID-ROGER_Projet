import json
from entities.brick import Brick


"""
Fonction permettant de charger un niveau depuis un fichier JSON
@param config: Configuration du jeu
@param level_file: Fichier JSON contenant les informations du niveau
@return: Liste de briques
"""
def loadLevel(config, layout):
    bricks = [] #Permet de créer une liste de bricks vide, c'est elle qui va contenir les briques du niveau
    numColumns = len(layout[0]) #Nombre de colonnes sur la grille
    brickWidth = config.screenWidth // numColumns #Division entière pour obtenir la largeur des briques
    brickHeight = 20

    for rowIndex, row in enumerate(layout): #Parcours de chaque ligne de la grille
        for colIndex, cell in enumerate(row): #Parcours de chaque colonne de la grille
            if cell > 0:  # 1 représente une brique dans la grille (du json)
                x = colIndex * brickWidth
                y = rowIndex * brickHeight + config.screenHudHeight
                color = config.colors["brick" + str(cell)] #Couleur de la brique
                bricks.append(Brick(x, y, brickWidth, brickHeight, color, cell, config)) #Ajout de la brique à la liste de briques

    return bricks