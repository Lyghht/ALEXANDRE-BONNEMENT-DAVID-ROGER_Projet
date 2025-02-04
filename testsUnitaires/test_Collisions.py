import pytest
from unittest.mock import MagicMock
import sys
import os
# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.collisions import Collisions


@pytest.fixture
def mock_game():
    game = MagicMock()
    
    # Simuler la balle avec des attributs nécessaires
    game.ball.x = 200
    game.ball.y = 300
    game.ball.dx = 5
    game.ball.dy = -5
    game.ball.radius = 10

    # Simuler le paddle
    game.paddle.x = 180
    game.paddle.width = 40

    # Simuler les briques
    brick_mock = MagicMock()
    brick_mock.isActive = True
    brick_mock.rect = MagicMock()
    brick_mock.rect.x = 100
    brick_mock.rect.y = 200
    brick_mock.rect.width = 50
    brick_mock.rect.height = 20

    game.bricks = [brick_mock]

    # Simuler la configuration du jeu
    game.config.bounceAngle = 45
    game.config.screenHeight = 600

    # Simuler les utils
    game.utils.circleRectCollision = MagicMock(return_value=True)  # Simuler une collision

    return game

def test_CheckPaddleCollision(mock_game):
    """Test de la collision avec le paddle."""
    collisions = Collisions(mock_game)
    
    result = collisions.checkPaddleCollision()
    
    assert result is True  # On attend à une collision
    assert mock_game.utils.circleRectCollision.called  # Vérifie que la fonction de collision a été appelée

def test_CheckBrickCollision(mock_game):
    """Test de la collision avec une brique."""
    collisions = Collisions(mock_game)

    # Simuler une brique avec des valeurs numériques
    mock_game.bricks[0].rect.x = 100
    mock_game.bricks[0].rect.y = 200
    mock_game.bricks[0].rect.width = 50
    mock_game.bricks[0].rect.height = 20

    result = collisions.checkBrickCollisions()

    assert result is True
    assert mock_game.bricks[0].hit.called 

def test_CheckBrickCollisionNoCollision(mock_game):
    """Test quand il n'y a pas de collision avec une brique."""
    collisions = Collisions(mock_game)

    # Déplacer la balle pour qu'elle ne touche pas la brique
    mock_game.ball.x = 500  # Loin de la brique
    mock_game.ball.y = 500
    # Configurer le mock pour renvoyer False dans ce cas
    mock_game.utils.circleRectCollision = MagicMock(return_value=False)

    result = collisions.checkBrickCollisions()

    assert result is False 
    assert not mock_game.bricks[0].hit.called 



def test_CheckBrickCollisionMultipleBricks(mock_game):
    """Test la collision avec plusieurs briques, une seule doit être touchée."""
    collisions = Collisions(mock_game)

    # Ajouter une deuxième brique
    brick2 = MagicMock()
    brick2.isActive = True
    brick2.rect = MagicMock()
    brick2.rect.x = 300  # Cette brique est éloignée, donc pas de collision
    brick2.rect.y = 200
    brick2.rect.width = 50
    brick2.rect.height = 20

    mock_game.bricks.append(brick2)

    # Position de la balle pour toucher uniquement la première brique
    mock_game.ball.x = 110
    mock_game.ball.y = 210

    result = collisions.checkBrickCollisions()

    assert result is True  # Une collision doit être détectée
    assert mock_game.bricks[0].hit.called  # La première brique doit être touchée
    assert not mock_game.bricks[1].hit.called  # La deuxième brique ne doit pas être touchée



def test_HandleBottomCollisionGameOver(mock_game):
    """Test que le jeu passe en GAME OVER si plus de vies."""
    mock_game.ball.y = 590
    mock_game.gameLife.loseLife.return_value = False

    collisions = Collisions(mock_game)
    result = collisions.handleBottomCollision()

    assert result is False 
    from core.game import GameState
    assert mock_game.state == GameState.GAME_OVER
