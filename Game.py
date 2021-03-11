from Queue import Queue
import Tetromino as tm
import pygame as pg

class Game():
    def __init__(self):
        tm.Tetromino.spawn()
        self.score = 0

    q = Queue()

    GRAY = (150,150,150)
    DGRAY = (80,80,80)
    WHITE = (255, 255, 255)
    pg.font.init()
    fontSize = 13
    main_font = pg.font.SysFont("arial", fontSize)
    BoardHeight, BoardWidth = 40, 10
    WIDTH, HEIGHT = 600, 800
    zoom = 20
    
    def run_board(self, win):
        for i in range(self.BoardHeight):
            for j in range(self.BoardWidth):
                if tm.Tetromino.board_matrix[i][j] == 0:
                    color = self.GRAY
                    border = 1
                else:
                    color = tm.Tetromino.colors[tm.Tetromino.board_matrix[i][j]] # colorsByIdx()
                    border = 0

                pg.draw.rect(win, color, 
                    [j*self.zoom, i*self.zoom, self.zoom, self.zoom], border)