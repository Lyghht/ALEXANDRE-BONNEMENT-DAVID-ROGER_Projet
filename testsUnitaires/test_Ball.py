import pytest
from unittest.mock import MagicMock
import sys
import math
import os
import pygame
# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from entities.ball import Ball
from core.collisions import Collisions

@pytest.fixture
def mock_game():
    """Mock de l'objet jeu"""
    game = MagicMock()

    # Simuler la balle
    game.ball.x = 200
    game.ball.y = 300
    game.ball.dx = 5
    game.ball.dy = -5
    game.ball.radius = 10

    # Simuler le paddle
    game.paddle.x = 200
    game.paddle.width = 100

    # Simuler les utils
    game.utils.circleRectCollision = MagicMock(return_value=True)

    # Simuler la configuration
    game.config.bounceAngle = 45
    game.config.screenWidth = 800
    game.config.screenHeight = 600
    game.config.screenHudHeight = 50
    game.config.ballSpeed = 5

    return game

@pytest.fixture
def ball(mock_game, monkeypatch):
    """Fixture pour initialiser une balle avec un mock de pygame.image.load"""
    monkeypatch.setattr(pygame.image, "load", lambda _: pygame.Surface((10, 10)))  # Empêcher le chargement réel de l'image
    return Ball(mock_game.config)


def test_NewSpeedBallLeft(mock_game):
    """Test de newSpeedBall avec la balle frappant le côté gauche du paddle."""
    collisions = Collisions(mock_game)

    mock_game.ball.x = 160  # À gauche du centre du paddle
    dx, dy = collisions.newSpeedBall()

    assert math.isclose(dx, -6.9, abs_tol=0.1)  # La balle doit repartir vers la gauche
    assert dy < 0  # La balle doit continuer à monter

def test_NewSpeedBallRight(mock_game):
    """Test de newSpeedBall avec la balle frappant le côté droit du paddle."""
    collisions = Collisions(mock_game)

    mock_game.ball.x = 280  # À droite du centre du paddle
    dx, dy = collisions.newSpeedBall()

    assert math.isclose(dx, 3.2, abs_tol=0.1)
    assert dy < 0

def test_NewSpeedBallCenter(mock_game):
    """Test de newSpeedBall avec la balle frappant le centre du paddle."""
    collisions = Collisions(mock_game)

    mock_game.ball.x = 251  # Au centre du paddle
    dx, dy = collisions.newSpeedBall()

    assert math.isclose(dx, 0, abs_tol=0.2)  # La balle doit partir droit vers le haut
    assert dy < 0  # La balle doit continuer à monter

def test_initialization(ball, mock_game):
    """Test de l'initialisation de la balle"""
    assert ball.x == mock_game.config.screenWidth // 2
    assert ball.y == mock_game.config.screenHeight - 50
    assert ball.dx == 0
    assert ball.dy == 0
    assert ball.angle == 0

def test_update_no_movement(ball):
    """Test si la balle ne bouge pas quand isPlaying=False"""
    ball.update(isPlaying=False)
    assert ball.dx == 0
    assert ball.dy == 0
    assert ball.angle == 0

def test_update_movement(ball):
    """Test du mouvement de la balle quand isPlaying=True"""
    ball.dx, ball.dy = 5, -5
    ball.update(isPlaying=True)
    assert ball.x == (ball.config.screenWidth // 2) + 5
    assert ball.y == (ball.config.screenHeight - 50) - 5
    assert ball.angle > 0  # Vérifie que l'angle augmente

def test_collision_left(ball):
    """Test du rebond sur le mur gauche"""
    ball.x = 5  # Proche du bord gauche
    ball.dx = -5
    ball.update(isPlaying=True)
    assert ball.dx > 0  # La balle doit rebondir et aller à droite

def test_collision_right(ball):
    """Test du rebond sur le mur droit"""
    ball.x = ball.config.screenWidth - 5
    ball.dx = 5
    ball.update(isPlaying=True)
    assert ball.dx < 0  # La balle doit rebondir et aller à gauche

def test_collision_top(ball):
    """Test du rebond sur le plafond"""
    ball.y = ball.config.screenHudHeight + 5
    ball.dy = -5
    ball.update(isPlaying=True)
    assert ball.dy > 0  # La balle doit rebondir et aller vers le bas

def test_resetPlace(ball, mock_game):
    """Test du reset de la balle"""
    ball.x, ball.y, ball.dx, ball.dy = 100, 100, 5, 5
    ball.resetPlace()
    assert ball.x == mock_game.config.screenWidth // 2
    assert ball.y == mock_game.config.screenHeight - 50
    assert ball.dx == 0
    assert ball.dy == 0

def test_launchBall(ball):
    """Test du lancement de la balle"""
    ball.launchBall()
    assert ball.dx == ball.config.ballSpeed
    assert ball.dy == -ball.config.ballSpeed