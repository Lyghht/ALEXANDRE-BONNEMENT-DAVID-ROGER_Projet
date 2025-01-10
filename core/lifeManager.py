#Classe permettant de faire la gestion des vies du joueur
class lifeManager:
    # Constructeur de la classe
    def __init__(self, initialLife):
        self.life = initialLife

    # Méthode permettant de retirer une vie
    #True la partie continue, False la partie est perdue
    def loseLife(self):
        self.life -= 1
        if self.life <= 0:
            return False
        return True

    # Méthode permettant de donner le nombre de vie
    def get_lives(self):
        return self.life

    