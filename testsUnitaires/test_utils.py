import pytest
import pygame
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import Config
from entities.ball import Ball
from entities.paddle import Paddle
from core.utils import Utils


@pytest.fixture
def mock_game():
    game = MagicMock()

    # Initialiser la configuration
    config = Config()
    game.config = config
    
    # Simuler la balle avec des attributs nécessaires
    game.ball = Ball(config)
    game.ball.x = game.ball.x + 5
    game.ball.y = game.ball.y + 5

    # Simuler le paddle
    game.paddle = Paddle(config)
    game.paddle.x = game.paddle.x + 5
    game.paddle.y = game.paddle.y + 5

    game.hud = MagicMock()
    game.level = config.initialLevel
    game.isPlaying = False
    game.score = config.initialScore

    # Simuler les briques
    brick_mock = MagicMock()
    brick_mock.isActive = True
    brick_mock.life = 1
    brick_mock.rect = pygame.Rect(100, 200, 50, 20)

    game.bricks = [brick_mock]

    return game


def test_reset_round(mock_game):
    """
    Test de la méthode resetRound
    """
    config = Config()
    utils = Utils(mock_game)
    utils.showCountdown = MagicMock()
    utils.resetRound()

    assert utils.game.isPlaying is False

    # Vérifier que la balle et le paddle sont réinitialisés
    assert mock_game.ball.x == config.screenWidth // 2
    assert mock_game.ball.y == config.screenHeight - 50
    assert mock_game.paddle.x == (config.screenWidth - mock_game.paddle.width) // 2
    assert mock_game.paddle.y == config.screenHeight - 40


@patch("pygame.mixer.Sound", return_value=MagicMock())  # Empêche le chargement réel des sons
def test_reset_game(mock_sound, mock_game):
    """
    Test de la méthode resetGame
    """
    config = Config()
    mock_game.level += 1 # Permet de tester la réinitialisation du level
    mock_game.score += 100 # Permet de tester la réinitialisation du score
    utils = Utils(mock_game)
    utils.resetGame()

    # Vérifier que les briques sont bien recréées
    assert isinstance(mock_game.bricks, list)

    # Vérifier que les variables de jeu sont réinitialisées
    assert mock_game.isPlaying is False
    assert mock_game.score == config.initialScore
    assert mock_game.level == config.initialLevel

    # Vérifier que la balle et le paddle sont réinitialisés
    assert mock_game.ball.x == config.screenWidth // 2
    assert mock_game.ball.y == config.screenHeight - 50
    assert mock_game.paddle.x == (config.screenWidth - mock_game.paddle.width) // 2
    assert mock_game.paddle.y == config.screenHeight - 40

    # Vérifier que les briques sont rechargées
    for brick in mock_game.bricks:
        assert brick.isActive is True

@patch("pygame.mixer.Sound", return_value=MagicMock())
def test_check_victory_no_bricks_left(mock_sound, mock_game):
    """
    Test de la méthode checkVictory quand toutes les briques sont détruites.
    """
    config = Config()
    utils = Utils(mock_game)
    
    # Simuler un HUD et un Renderer
    mock_game.hud.updateLevel = MagicMock()
    mock_game.hud.updateLives = MagicMock()
    mock_game.renderer.render = MagicMock()
    
    # Simuler le gestionnaire de vie
    mock_game.gameLife.getLife = MagicMock(return_value=config.initialLife - 1)
    mock_game.gameLife.addLife = MagicMock()

    # Simuler des briques toutes détruites
    for brick in mock_game.bricks:
        brick.isActive = False
        brick.life = 0

    utils.showCountdown = MagicMock()
    utils.checkVictory()

    # Vérifier que le niveau a été incrémenté
    assert mock_game.level == config.initialLevel + 1

    # Vérifier que la vie a été augmentée si elle n'était pas au maximum
    mock_game.gameLife.addLife.assert_called_once()

    # Vérifier que l'affichage est mis à jour
    mock_game.hud.updateLevel.assert_called_once_with(mock_game.level)
    mock_game.hud.updateLives.assert_called_once_with(mock_game.gameLife.getLife())

    # Vérifier que le jeu est mis en pause
    assert mock_game.isPlaying == False

    # Vérifier que le compte à rebours est bien affiché
    utils.showCountdown.assert_called_once()

    # Vérifier que le renderer a été appelé pour mettre à jour l'affichage
    mock_game.renderer.render.assert_called_once()


def test_check_victory_bricks_remaining(mock_game):
    """
    Test de la méthode checkVictory quand il reste des briques.
    """
    config = Config()
    utils = Utils(mock_game)
    
    # Simuler des briques restantes
    mock_game.bricks[0].life = 1  # Au moins une brique encore en jeu
    
    utils.checkVictory()

    # Vérifier que le niveau n'a pas changé
    assert mock_game.level == config.initialLevel

    # Vérifier que l'HUD et le renderer ne sont pas appelés
    mock_game.hud.updateLevel.assert_not_called()
    mock_game.hud.updateLives.assert_not_called()
    mock_game.renderer.render.assert_not_called()

@pytest.mark.parametrize("ball_x, ball_y, rect_x, rect_y, rect_w, rect_h, expected",
    [
        (105, 205, 100, 200, 50, 20, True),  # Collision en haut à gauche
        (150, 210, 100, 200, 50, 20, True),  # Collision en haut à droite
        (120, 225, 100, 200, 50, 20, True),  # Collision en bas
        (50, 50, 100, 200, 50, 20, False),   # Pas de collision (hors du rectangle)
    ]
)
def test_circle_rect_collision(mock_game, ball_x, ball_y, rect_x, rect_y, rect_w, rect_h, expected):
    """
    Test de la méthode circleRectCollision avec différents scénarios
    """
    utils = Utils(mock_game)

    # Simuler la position de la balle
    mock_game.ball.x = ball_x
    mock_game.ball.y = ball_y

    # Simuler le rectangle d'un objet (brique)
    rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)

    # Vérifier la collision
    assert utils.circleRectCollision(rect) == expected
