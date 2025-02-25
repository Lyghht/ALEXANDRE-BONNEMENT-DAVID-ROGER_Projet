### Projects2024
Projets des étudiants en BUT Info Alternant 2024-2025  
Groupe : ALEXANDRE Clément - BONNEMENT léo - DAVID Émile - ROGER Simon

# Projet de Développement d'un casse brique
Langage de programmation : python  
Dépendances : pygame, pytest, unittest

## Comment lancer le jeu :
Pour lancer le jeu, il faudra exécuter le main qui permet de lancer les différentes classes du projet et ne pas oublier d'installer les dépendances nécessaires (tels que pygame, etc.).

## Comment lancer les tests :
Pour exécuter les tests, il faut exécuter ```pytest``` avec l'option ```-v``` (plus de détails) ou simplement ```pytest```, ce qui est possible à la racine du projet.

## Installer les dépendances :
Pour installer les dépendances, il suffit d'exécuter ```pip install -r requirements.txt```

## Arborescence du projet :

```
ALEXANDRE-BONNEMENT-DAVID-ROGER_PROJET/
├── main.py               # Point d'entrée du jeu
├── config/
│   └── settings.py       # Configuration globale (dimensions de l'écran, couleurs, vitesse, etc.)
├── assets/
│   ├── images/           # Images des briques, de la balle, du paddle, etc.
│   ├── sounds/           # Effets sonores pour collisions et musique de fond
│   └── fonts/            # Polices pour le texte
├── core/
│   ├── game.py           # Classe principale pour gérer la boucle de jeu et les événements
│   ├── utils.py          # Fonctions utilitaires
│   ├── collisions.py     # Classe pour la gestion des collisions
│   ├── lifeManager.py    # Classe pour la gestion des vies
├── entities/
│   ├── bonus.py          # Classe pour les bonus
│   ├── paddle.py         # Classe pour le paddle
│   ├── ball.py           # Classe pour la balle
│   └── brick.py          # Classe pour les briques
├── levels/
│   ├── levelGenerator.py # générateur de niveau
│   └── levelLoader.py    # Chargeur de niveau
├── testsUnitaires/
│   ├── test_Ball.py      # tests unitaires pour la classe Ball
│   ├── test_Brick.py     # tests unitaires pour la classe Brick
│   ├── test_Collisions.py # tests unitaires pour la classe Collisions
│   ├── test_LifeManager.py # tests unitaires pour la classe LifeManager
│   ├── test_Paddle.py    # tests unitaires pour la classe Paddle
│   ├── test_Utils.py     # tests unitaires pour la classe Utils
├── ui/
│   ├── renderer.py       # Gère le render des différents éléments du jeu
│   ├── menu.py           # Menu principal (start, quit)
│   ├── hud.py            # Interface utilisateur en jeu (score, vies restantes)
│   ├── breakMenu.py      # Affichage de l'écran de pause
│   └── gameOver.py       # Affichage de l'écran de fin de partie
└── README.md             # Documentation pour le projet
└── requirement.txt       # Fichier des dépendances python
```

## Tâches à Réaliser :

#### 1.	Code et Commentaire :
-	Développez le jeu en respectant les normes de codage.
-	Commentez le code de manière claire et explicative.
#### 2.	Cahier des charges :
-	Rédigez un cahier des charges décrivant les fonctionnalités, les règles du jeu, les objectifs et les spécifications techniques.
#### 3.	Plan de Test :
-	Élaborez un plan de test détaillé, y compris les scénarios de test, les données de test et les critères d'acceptation. (Plan de test simplifié, sans analyses des risques, juste l’ensemble de vos tests, les critère d’acceptations, et la validation du test)
#### 4.	Documentation Technique :
-	Créez une documentation technique complète expliquant l'architecture du jeu et la structure du code.
#### 5.	Tests Unitaires :
-	Implémentez des tests unitaires pour valider le bon fonctionnement du code du jeu.
#### 6.	GitHub :
-	Créez un répertoire sur GitHub : https://github.com/TMareIUT/Projects2024/  
[Vos Noms de Famille]_Projet
Faites en un fork et poussez régulièrement le code source, la documentation, le plan de test et les tests unitaires. N’hésitez pas à faire de multiples Pull-Request.
#### 7.	Revue de Code :
-	Effectuez une revue de code en utilisant les pull-request sur GitHub pour examiner le code de vos collègues et fournir des commentaires constructifs.
-	lien : https://github.com/Nattends/projet-snake/pull/3
