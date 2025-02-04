import pytest
from unittest.mock import MagicMock
import sys
import os
# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.collisions import Collisions


@pytest.fixture
def mock_game():
    """Fixture pour créer un mock du jeu avec les éléments nécessaires."""
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
    game.paddle.rect = MagicMock()

    # Simuler les briques
    brick_mock = MagicMock()
    brick_mock.isActive = True
    brick_mock.rect = MagicMock()
    game.bricks = [brick_mock]

    # Simuler la configuration du jeu
    game.config.bounceAngle = 45
    game.config.screenHeight = 600

    # Simuler les utils
    game.utils.circleRectCollision = MagicMock(return_value=True)  # Simuler une collision

    return game

def test_check_paddle_collision(mock_game):
    """Test de la collision avec le paddle."""
    collisions = Collisions(mock_game)
    
    result = collisions.checkPaddleCollision()
    
    assert result is True  # On s'attend à une collision
    assert mock_game.utils.circleRectCollision.called  # Vérifier que la fonction de collision a été appelée

def test_check_brick_collision(mock_game):
    """Test de la collision avec une brique."""
    collisions = Collisions(mock_game)

    result = collisions.checkBrickCollisions()

    assert result is True  # Collision détectée
    assert mock_game.bricks[0].hit.called  # Vérifier que la brique a été touchée

def test_handle_bottom_collision_game_over(mock_game):
    """Test de la collision avec le bas de l'écran quand il n'y a plus de vies."""
    mock_game.ball.y = 590  # La balle touche le bas
    mock_game.gameLife.loseLife.return_value = False  # Plus de vies

    collisions = Collisions(mock_game)
    result = collisions.handleBottomCollision()

    assert result is False  # Le jeu doit s'arrêter
    assert mock_game.state == "GAME_OVER"  # Vérifier que l'état du jeu est bien mis à jour