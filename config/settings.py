class Config:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 600
        self.bgColor = (0, 0, 0)  # Noir
        self.fps = 60
        self.paddleSpeed = 5
        self.ballSpeed = 4
        self.colors = {
            "brick": (255, 0, 0),  # Rouge
            "paddle": (255, 255, 255),  # Blanc
            "ball": (0, 255, 0),  # Vert
        }