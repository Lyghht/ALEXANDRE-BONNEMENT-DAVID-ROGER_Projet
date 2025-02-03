import random

def generateRandomLayout(rows, cols, difficulty, min_group_size=2, max_group_size=5, symmetrical=False, geometric=False):
    layout = [[0 for _ in range(cols)] for _ in range(rows)]

    # Déterminer les niveaux de vie possibles en fonction de la difficulté
    if difficulty <= 0.3:
        life_range = [1, 2]  # Niveaux de 1 à 3
    elif 0.3 < difficulty <= 0.5:
        life_range = [1, 2, 3, 4]  # Niveaux de 4 à 5
    else:
        life_range = [1, 2, 3, 4, 5, 6]  # Niveaux au-dessus de 7

    # Générer des groupes aléatoires
    for _ in range(int(rows * cols * difficulty)):
        life = random.choice(life_range)  # Vie de la brique choisie dans la plage appropriée
        group_size = random.randint(min_group_size, max_group_size)  # Taille du groupe
        start_row = random.randint(0, rows - 1)
        start_col = random.randint(0, cols - 1)

        # Essayer de placer un groupe de briques
        for _ in range(group_size):
            if 0 <= start_row < rows and 0 <= start_col < cols and layout[start_row][start_col] == 0:
                layout[start_row][start_col] = life

                # Déplacer aléatoirement pour continuer le groupe
                start_row += random.choice([-1, 0, 1])
                start_col += random.choice([-1, 0, 1])

    # Appliquer la symétrie si nécessaire
    if symmetrical:
        for r in range(rows):
            for c in range(cols // 2):
                layout[r][cols - c - 1] = layout[r][c]

    # Appliquer des formes géométriques
    if geometric:
        # Exemple de génération d'un carré de briques
        shape_size = random.randint(2, min(rows, cols) // 3)
        top_left_row = random.randint(0, rows - shape_size)
        top_left_col = random.randint(0, cols - shape_size)
        for r in range(top_left_row, top_left_row + shape_size):
            for c in range(top_left_col, top_left_col + shape_size):
                layout[r][c] = random.choice(life_range)

        # Exemple de génération d'un triangle
        triangle_size = random.randint(2, min(rows, cols) // 3)
        start_row = random.randint(0, rows - triangle_size)
        start_col = random.randint(0, cols - triangle_size)
        for i in range(triangle_size):
            for j in range(i + 1):
                layout[start_row + i][start_col + j] = random.choice(life_range)

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
