from core.path import resourcePath

class Config:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 600
        self.screenHudHeight = 50
        self.bgColor = (0, 0, 0)  # Noir
        self.bgColorMenu = (119, 181, 254) # Bleu clair
        self.fps = 60
        self.paddleSpeed = 12
        self.bounceAngle = 55 # Angle de rebond 90 - bounceAngle = angle de rebond max côté droite
        self.initialLife = 3
        self.initialLevel = 1
        self.initialScore = 0
        self.ballSpeed = 5
        self.maxBrickLife = 6
        self.sounds = {
            "brickHit": resourcePath("assets/sounds/brickHit.wav"),
            "brickFall": resourcePath("assets/sounds/brickFall.wav"),
        }
        self.images = {
            "ball": resourcePath("assets/images/superball.png"),
            "brick1": resourcePath("assets/images/brick1.png"),
            "brick2": resourcePath("assets/images/brick2.png"),
            "brick3": resourcePath("assets/images/brick3.png"),
            "brick4": resourcePath("assets/images/brick4.png"),
            "brick5": resourcePath("assets/images/brick5.png"),
            "brick6": resourcePath("assets/images/brick6.png"),
            "paddle": resourcePath("assets/images/paddle.png"),
            "heart": resourcePath("assets/images/heart.png"),
            "heartBroken": resourcePath("assets/images/heartBroken.png"),
        }
        self.bonusProbability = 0.2
        self.bonusSpeed = 2