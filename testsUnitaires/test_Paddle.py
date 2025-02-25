import pygame
import pytest
import sys, os
# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import MagicMock
from entities.paddle import Paddle

@pytest.fixture
def mock_config():
    config = MagicMock()
    config.paddleSpeed = 5
    config.screenWidth = 800
    config.screenHeight = 600
    config.images = {"paddle": "assets/paddle.png"}
    return config

@pytest.fixture
def paddle(mock_config):
    return Paddle(mock_config)

def test_paddle_moves_left(paddle):
    """Test du déplacement du paddle vers la gauche."""
    paddle.x = 400  # Position de départ
    keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
    
    paddle.update(keys)

    assert paddle.x == 395  # Doit avoir reculé de paddleSpeed

def test_paddle_moves_right(paddle):
    """Test du déplacement du paddle vers la droite."""
    paddle.x = 400  # Position de départ
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}

    paddle.update(keys)

    assert paddle.x == 405  # Doit avoir avancé de paddleSpeed

def test_paddle_does_not_exit_left(paddle):
    """Test que le paddle ne sort pas de l'écran par la gauche."""
    paddle.x = 0
    keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}

    paddle.update(keys)

    assert paddle.x == 0  # Doit rester à 0

def test_paddle_does_not_exit_right(paddle):
    """Test que le paddle ne sort pas de l'écran par la droite."""
    paddle.x = paddle.config.screenWidth - paddle.width
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}

    paddle.update(keys)

    assert paddle.x == paddle.config.screenWidth - paddle.width  # Doit rester au max à droite

def test_paddle_reset(paddle):
    """Test de la réinitialisation du paddle."""
    paddle.x = 300  # Modifier la position
    paddle.y = 200

    paddle.reset()

    assert paddle.x == (paddle.config.screenWidth - paddle.width) // 2
    assert paddle.y == paddle.config.screenHeight - 40