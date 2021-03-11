import pygame as pg
from game import Game

CYAN = (0,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
PURPLE = (148,0,211)

class Tetromino():
    def __init__(self, typ): # typ is a string in IJLOSTZ
        self.type = typ
        self.color = Tetromino.colors[typ]
        self.shape = Tetromino.shape[typ]
        self.x, self.y, self.rot = 3, 0, 0
        
    board_matrix = [[0 for _ in range(Game.BoardWidth)] 
                            for _ in range(Game.BoardHeight)]

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
        def rect(current, i, j):
            pg.draw.rect(win, current.color, 
            [(j + current.x)*Game.zoom, (i + current.y)*Game.zoom, 
                                        Game.zoom - 1, Game.zoom - 1])
    
        current = Game.q.current()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in current.current_shape():
                    rect(current, i, j)
                    rect(current.ghost, i, j)

    def hardrop(self):
        setattr(self, "y", self.ghost.y)

    def collides(self):
        # Checks collision on every block returns True if at least one collides
        for i in range(4):
            for j in range(4):
                temp = i * 4 + j
                if temp in self.current_shape():
                    if i + self.y > Game.BoardHeight - 1 or i + self.y < 0 or \
                    Tetromino.board_matrix[i + self.y][j + self.x] != 0:
                        return True
        return False
    
    def fall(self): # rename this
        self.ghost.fall()
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

    def move(self, dx):
        def edge():
            for i in range(4):
                for j in range(4):
                    temp = i * 4 + j
                    if temp in self.current_shape():
                        if j + self.x + dx > Game.BoardWidth - 1 or \
                            0 > j + self.x + dx:
                                return True
            return False
        
        if not edge():
            self.x += dx

class Ghost(Tetromino):
    def __init__(self, typ):
        super().__init__(typ)
        self.color = Game.DGRAY

    def fall(self):
        while not self.collides():
            self.y += 1
        self.y -=1

class Living(Tetromino):
    def __init__(self, typ):
        super().__init__(typ)
        self.ghost = Ghost(self.type)
        
    @classmethod
    def spawn(cls):
        Game.q.add(cls(Game.s.peek(n=1)[0]))
        return cls(Game.s.pop())
        
    def freeze(self):
        for i in range(4):
            for j in range(4):
                temp = i * 4 + j
                if temp in self.current_shape():
                    Tetromino.board_matrix[i + self.y][j + self.x] = self.type
        self.spawn()