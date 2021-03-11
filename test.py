
class Game():
    def __init__(self):
        self.score = 0


    GRAY = (150,150,150)
    fontSize = 13
    BoardHeight, BoardWidth = 40, 10
    WIDTH, HEIGHT = 600, 800
    zoom = 40
    board_matrix = [[0 for _ in range(BoardWidth)] 
                            for _ in range(BoardHeight)]
    