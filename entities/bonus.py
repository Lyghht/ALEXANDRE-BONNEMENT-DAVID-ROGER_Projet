import pygame

class Bonus:
    def __init__(self, x, y, width, height, bonus_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.bonus_type = bonus_type
        self.isActive = True
        self.image = pygame.image.load(f'assets/bonuses/{bonus_type}.png')

    def draw(self, screen):
        if self.isActive:
            screen.blit(self.image, self.rect.topleft)

    def apply(self, game):
        if self.bonus_type == "doubleBar":
            game.paddle.doubleBarre()
        elif self.bonus_type == "semiBar":
            game.paddle.semiBarre()
        elif self.bonus_type == "slowBall":
            game.ball.slowBall()
        elif self.bonus_type == "triple_ball":
            game.addBalls(3)
        elif self.bonus_type == "slow_ball":
            game.ball.slowDown()
        elif self.bonus_type == "explosiveBall":
            game.ball.explosiveBall()
        self.isActive = False