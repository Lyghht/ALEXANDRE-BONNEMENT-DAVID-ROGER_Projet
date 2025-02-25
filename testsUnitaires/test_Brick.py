import pygame
import pytest
from unittest.mock import MagicMock
import os, sys
# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from entities.brick import Brick

@pytest.fixture
def mock_config():
    """Fixture pour simuler la configuration du jeu."""
    config = MagicMock()
    config.maxBrickLife = 3 
    config.images = {f"brick{life}": f"../assets/images/brick{life}.png" for life in range(1, config.maxBrickLife + 1)}
    config.sounds = {
        "brickHit": "../assets/sounds/brickHit.wav",
        "brickFall": "../assets/sounds/brickFall.wav"
    }

    config.bonusProbability = 0

    # Simuler le chargement des images et sons
    pygame.image.load = MagicMock(side_effect=lambda path: pygame.Surface((50, 20)))
    pygame.mixer.Sound = MagicMock(return_value=MagicMock())

    return config


@pytest.fixture
def brick(mock_config):
    """Fixture pour créer une brique simulée."""
    return Brick(x=100, y=50, width=50, height=20, life=3, config=mock_config)



def test_DrawBrickActive(brick):
    """Vérifie que la brique est bien dessinée si elle est active."""
    screen = MagicMock()
    brick.draw(screen)
    screen.blit.assert_called_once_with(brick.image, brick.rect)


def test_DrawBrickInactive(brick):
    """Vérifie que la brique n'est pas dessinée si elle est détruite."""
    screen = MagicMock()
    brick.isActive = False
    brick.draw(screen)
    screen.blit.assert_not_called()


def test_HitReducesLife(brick):
    """Test que la méthode hit() réduit la vie de la brique et met à jour l’image."""
    initial_life = brick.life
    brick.hit()
    
    assert brick.life == initial_life - 1
    assert brick.image == brick.brickImages[brick.life]  # Vérifie le changement d'image
    brick.brickHitSound.play.assert_called_once()  # Vérifie que le son de hit est joué


def test_HitDestroysBrick(brick):
    """Test que la brique est désactivée lorsqu'elle est détruite."""
    brick.life = 1  # Met la vie de la brique à 1 avant le test
    brick.hit()
    
    assert brick.isActive is False
    brick.brickFallSound.play.assert_called_once()  # Vérifie que le son de destruction est joué


def test_HitWithCustomDamage(brick):
    """Test que la brique subit des dégâts personnalisés."""
    brick.life = 3
    brick.hit(damage=2)
    
    assert brick.life == 1
    assert brick.isActive is True  # La brique n'est pas encore détruite
    brick.brickHitSound.play.assert_called_once()  # Vérifie que le son de hit est joué


def test_HitExceedsLife(brick):
    """Test que la brique est désactivée si les dégâts sont supérieurs à sa vie restante."""
    brick.life = 3
    brick.hit(damage=5)
    
    assert brick.life <= 0
    assert brick.isActive is False
    brick.brickFallSound.play.assert_called_once()  # Vérifie que le son de destruction est joué
