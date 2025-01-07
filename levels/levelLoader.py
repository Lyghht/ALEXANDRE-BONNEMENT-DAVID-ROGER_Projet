import json
from entities.brick import Brick


"""
Fonction permettant de charger un niveau depuis un fichier JSON
@param config: Configuration du jeu
@param level_file: Fichier JSON contenant les informations du niveau
@return: Liste de briques
"""
def loadLevel(config, level_file):
    bricks = [] #Permet de créer une liste de bricks vide, c'est elle qui va contenir les briques du niveau

    with open(level_file, "r") as file: #Ouverture du fichier JSON
        data = json.load(file) #Chargement du fichier JSON dans data

    # Calculer la largeur des briques en fonction du nombre de colonnes sur la grille
    numColumns = len(data["layout"][0])
    brickWidth = config.screenWidth // numColumns #Division entière pour obtenir la largeur des briques
    brickHeight = 20

    for rowIndex, row in enumerate(data["layout"]): #Parcours de chaque ligne de la grille
        for colIndex, cell in enumerate(row): #Parcours de chaque colonne de la grille
            if cell == 1:  # 1 représente une brique dans la grille (du json)
                x = colIndex * brickWidth
                y = rowIndex * brickHeight
                color = config.colors["brick"] #Couleur des briques (à voir si on change en fonction de la dureté plus tard)
                bricks.append(Brick(x, y, brickWidth, brickHeight, color, 1)) #Ajout de la brique à la liste de briques

    return bricks