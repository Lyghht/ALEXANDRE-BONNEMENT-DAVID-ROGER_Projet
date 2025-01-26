class Config:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 600
        self.screenHudHeight = 50
        self.bgColor = (0, 0, 0)  # Noir
        self.bgColorMenu = (119, 181, 254) # Bleu clair
        self.fps = 60
        self.paddleSpeed = 8
        self.bounceAngle = 55 # Angle de rebond 90 - bounceAngle = angle de rebond max côté droite
        self.initialLife = 3
        self.initialLevel = 1
        self.initialScore = 0
        self.ballSpeed = 5
        self.maxBrickLife = 5
        self.sounds = {
            "brickHit": "assets/sounds/brickHit.wav",
            "brickFall": "assets/sounds/brickFall.wav",
        }
        self.images = {
            "ball": "assets/images/superball.png",
            "brick1": "assets/images/brick1.png",
            "brick2": "assets/images/brick2.png",
            "brick3": "assets/images/brick3.png",
            "brick4": "assets/images/brick4.png",
            "brick5": "assets/images/brick5.png",
            "brick6": "assets/images/brick6.png",
            "paddle": "assets/images/paddle.png",
        }