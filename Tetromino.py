import pygame as pg
from Game import Game

CYAN = (0,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
PURPLE = (148,0,211)


class Tetromino():
    def __init__(self, typ): # typ is a string in IJLOSTZ
        Tetromino.tetr_list.append(self)
        self.type = typ
        self.color = Tetromino.colors[typ]
        self.shape = Tetromino.shape[typ]
        self.x, self.y, self.rot = 3, 0, 0

    board_matrix = [[0 for _ in range(Game.BoardWidth)] 
                            for _ in range(Game.BoardHeight)]
    tetr_list = []

    # numbers represent index of a 4x4 matrix where a block should be
    shape = {
        "I" : [[1,5,9,13], [4,5,6,7]],
        "J" : [[1,2,5,9], [0,4,5,6], [1,5,8,9],[4,5,6,10]],
        "L" : [[1,2,6,10], [5,6,7,9], [2,6,10,11], [3,5,6,7]],
        "O" : [[1,2,5,6]],
        "S" : [[6,7,9,10], [1,5,6,10]],
        "T" : [[1,4,5,6],[1,4,5,9], [4,5,6,9], [1,5,6,9]],
        "Z" : [[4,5,9,10], [2,5,6,9]],
    }
    colors = {
        "I" : CYAN, 
        "J" : BLUE, 
        "L" : ORANGE, 
        "O" : YELLOW, 
        "S" : GREEN, 
        "T" : PURPLE, 
        "Z" : RED, 
    }

    @classmethod
    def draw(cls, win):
        """
        Draws little squares on the board

        This method uses 4x4 matrix and p determines which squares to fill
        by traversing tetrinoes shapes
        """
        current = cls.tetr_list[-1]
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in current.current_shape():
                    pg.draw.rect(win, current.color, 
                    [(j + current.x)*Game.zoom, (i + current.y)*Game.zoom, 
                                                Game.zoom - 1, Game.zoom - 1])

    @classmethod
    def spawn(cls):
        return cls(Game.q.pop())

    def __eq__(self, other):
        pass

    def ghost(self):
        if self.collides():
            self.y -= 1

    def hardrop(self):
        pass
        

    def collides(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.current_shape():
                    if i + self.y > Game.BoardHeight - 1 or i + self.y < 0 or \
                    Tetromino.board_matrix[i + self.y][j + self.x] != 0:
                        return True
        return False

    def fall(self):
        self.y += 1
        if self.collides():
            self.y -= 1
            self.freeze()

    def current_shape(self):
        return self.shape[self.rot]

    def rotate(self, right=True):
        if right:
            self.rot = (self.rot + 1) % len(self.shape)
        else:
            self.rot = (self.rot - 1) % len(self.shape)

    def move(self, operation="right"):
        if operation == "right":
            self.x += 1
        else:
            self.x -= 1

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.current_shape():
                    Tetromino.board_matrix[i + self.y][j + self.x] = self.type
        self.spawn()

class Ghost(Tetromino):
    def __init__(self, typ):
        super().__init__(typ)
        self.color = Game.DGRAY

    def logic(self):
        if self.collides()[0]:
            self.y -= 1
            Tetromino.tetr_list[-1] = self