import random

def generateRandomLayout(rows, cols, difficulty, minGroupSize=2, maxGroupSize=5, symmetrical=False, geometric=False):
    layout = [[0 for _ in range(cols)] for _ in range(rows)]

    # Déterminer les niveaux de vie possibles en fonction de la difficulté
    if difficulty <= 0.3:
        lifeRange = [1, 2]  # Niveaux de 1 à 3
    elif 0.3 < difficulty <= 0.5:
        lifeRange = [1, 2, 3, 4]  # Niveaux de 4 à 5
    else:
        lifeRange = [1, 2, 3, 4, 5, 6]  # Niveaux au-dessus de 7

    # Générer des groupes aléatoires
    for _ in range(int(rows * cols * difficulty)):
        life = random.choice(lifeRange)  # Vie de la brique choisie dans la plage appropriée
        groupSize = random.randint(minGroupSize, maxGroupSize)  # Taille du groupe
        startRow = random.randint(0, rows - 1)
        startCol = random.randint(0, cols - 1)

        # Essayer de placer un groupe de briques
        for _ in range(groupSize):
            if 0 <= startRow < rows and 0 <= startCol < cols and layout[startRow][startCol] == 0:
                layout[startRow][startCol] = life

                # Déplacer aléatoirement pour continuer le groupe
                startRow += random.choice([-1, 0, 1])
                startCol += random.choice([-1, 0, 1])

    # Appliquer la symétrie si nécessaire
    if symmetrical:
        for r in range(rows):
            for c in range(cols // 2):
                layout[r][cols - c - 1] = layout[r][c]

    # Appliquer des formes géométriques
    if geometric:
        # Exemple de génération d'un carré de briques
        shapeSize = random.randint(2, min(rows, cols) // 3)
        topLeftRow = random.randint(0, rows - shapeSize)
        topLeftCol = random.randint(0, cols - shapeSize)
        for r in range(topLeftRow, topLeftRow + shapeSize):
            for c in range(topLeftCol, topLeftCol + shapeSize):
                layout[r][c] = random.choice(lifeRange)

        # Exemple de génération d'un triangle
        triangleSize = random.randint(2, min(rows, cols) // 3)
        startRow = random.randint(0, rows - triangleSize)
        startCol = random.randint(0, cols - triangleSize)
        for i in range(triangleSize):
            for j in range(i + 1):
                layout[startRow + i][startCol + j] = random.choice(lifeRange)

    return layout

def generateLevels(level):
    difficulty = level * 0.1

    # Déterminer la taille de la grille en fonction du niveau
    match level:
        case 1 | 2 | 3:
            rows = 10
            cols = 10
        case 4 | 5:
            rows = 12
            cols = 15
        case _ if level > 5:
            rows = 15
            cols = 20
        case _:
            rows = 10
            cols = 10
    symmetrical = True
    geometric = True
    return generateRandomLayout(rows, cols, difficulty, symmetrical=symmetrical, geometric=geometric)
