class Config:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 600
        self.bgColor = (0, 0, 0)  # Noir
        self.bgColorMenu = (119, 181, 254) # Bleu clair
        self.fps = 60
        self.paddleSpeed = 5
        self.initialLife = 3
        self.ballSpeed = 4
        self.colors = {
            "brick1": "#F0F465", # Jaune
            "brick2" : "#9CEC5B", # Vert
            "brick3" : "#50C5B7", # Bleu
            "brick4" : "#6184D8", # Bleu
            "brick5" : "#533A71", # Violet
            "paddle": (255, 255, 255),  # Blanc
            "ball": (0, 255, 0),  # Vert
        }