from data_structure import Stack, Queue
import tetromino as tm
import pygame as pg

class Game():
    def __init__(self):
        tm.Living.spawn()
        self.score = 0

    s = Stack()
    q = Queue()

    GRAY = (150,150,150)
    DGRAY = (80,80,80)
    WHITE = (255, 255, 255)
    pg.font.init()
    fontSize = 13
    main_font = pg.font.SysFont("arial", fontSize)
    BoardHeight, BoardWidth = 20, 10
    WIDTH, HEIGHT = 600, 800
    PrevXPadd, PrevYPadd = 160, 140
    zoom = 40
    v = 1
    dt = pg.time.Clock().tick(20)
    
    def run_board(self, win):
        for i in range(self.BoardHeight):
            for j in range(self.BoardWidth):
                if tm.Tetromino.board_matrix[i][j] == 0:
                    color = self.GRAY
                    border = 1
                else:
                    color = tm.Tetromino.colors[tm.Tetromino.board_matrix[i][j]]
                    border = 0

                pg.draw.rect(win, color, 
                    [j*self.zoom, i*self.zoom, self.zoom, self.zoom], border)
                
    def clear_board(self): # calculate score
        # If all elements in board_matrix's row are != 0, clear them
        for i in range(self.BoardHeight):
            if all(tm.Tetromino.board_matrix[i]):
                for j in range(self.BoardWidth):
                    tm.Tetromino.board_matrix[i][j] = 0
    
    @classmethod           
    def preview_tetro(cls, win):
        def rect(current, i, j, n):
            pg.draw.rect(win, current.color, 
            [cls.WIDTH - cls.PrevXPadd + (j*cls.zoom), 
            (cls.PrevYPadd*n) + (i*cls.zoom), cls.zoom - 1, cls.zoom - 1])
    
        for m, n in enumerate(range(1,4)):
            current = tm.Tetromino(cls.s.peek(n=n)[m])
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in current.current_shape():
                        rect(current, i, j, n)