import pytest
import sys
import os

# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.lifeManager import lifeManager


def test_lose_life_test():
    """
    Test de la méthode loseLife
    """
    # Création de l'objet life
    life = lifeManager(3)
    # Test de la méthode
    assert life.loseLife() == True
    assert life.loseLife() == True
    assert life.loseLife() == False
    assert life.loseLife() == False

def test_add_life_test():
    """
    Test de la méthode addLife
    """
    # Création de l'objet life
    life = lifeManager(3)
    # Test de la méthode
    life.addLife(0)
    assert life.getLife() == 3
    life.addLife(1)
    assert life.getLife() == 4
    life.addLife(2)
    assert life.getLife() == 6

def test_get_life_test():
    """
    Test de la méthode getLife
    """
    # Création de l'objet life
    life = lifeManager(3)
    # Test de la méthode
    assert life.getLife() == 3
    life.loseLife()
    assert life.getLife() == 2
    life.addLife(1)
    assert life.getLife() == 3
    life.addLife(2)
    assert life.getLife() == 5
