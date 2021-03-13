from data_structure import Stack, Queue
import tetromino as tm
import pygame as pg
import timeit
import db

class Game():
    def __init__(self):
        tm.Living.spawn()
    
    scoring = {0 : 0, 1 : 40, 2 : 100, 3 : 300, 4 : 1200}
    score = 0

    s = Stack()
    q = Queue()
    holding_bag = Queue()

    GRAY = (150,150,150)
    DGRAY = (80,80,80)
    WHITE = (255, 255, 255)
    CYAN = (0,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    ORANGE = (255,165,0)
    YELLOW = (255,255,0)
    PURPLE = (148,0,211)
    
    pg.font.init()
    fontSize = 25
    main_font = pg.font.SysFont("arial", fontSize)
    BoardHeight, BoardWidth = 20, 10
    WIDTH, HEIGHT = 600, 800
    PrevXPadd, PrevYPadd = 160, 140
    zoom = 40
    start = timeit.default_timer()
    times = 0
    run = True
    end = False
    
    @classmethod
    def hold(cls, curr):
        if cls.times == 1:
            if len(cls.holding_bag) != 0:
                curr.x, curr.y, curr.ghost.x = 3, 0, 3
                cls.q.add(cls.holding_bag.current())
                cls.holding_bag.add(curr)
            else: # if empty
                curr.x, curr.y, curr.ghost.x = 3, 0, 3
                cls.holding_bag.add(curr)
                tm.Living.spawn()
    
    @classmethod
    def update_window(cls, win):
        win.fill((0, 0, 0))
        cls.run_board(win)
        current = cls.q.current()
        cls.preview(current, win, active_tetro=True)
        cls.preview(current.ghost, win, active_tetro=True)

        for m, n in enumerate(range(1,4)):
            cls.preview(tm.Tetromino(cls.s.peek(n=n)[m]), win, 
                         cls.WIDTH - cls.PrevXPadd, cls.PrevYPadd*n * (0.3*n))
            
        if len(cls.holding_bag) != 0:
            cls.preview(cls.holding_bag.current(), win, 
                        cls.WIDTH - cls.PrevXPadd, cls.HEIGHT - 200)
        else:
            cls.rect(win, cls.DGRAY, 
                      cls.WIDTH - cls.PrevXPadd, cls.HEIGHT - 200)
            

        score_text = Game.main_font.render(
                        "Score = {}".format(Game.score), 1, Game.WHITE)
        
        win.blit(score_text, ((Game.BoardWidth * Game.zoom),
                                        score_text.get_height()))

        pg.display.update()
                
    @classmethod
    def run_board(cls, win):
        for i in range(cls.BoardHeight):
            for j in range(cls.BoardWidth):
                if tm.Tetromino.board_matrix[i][j] == 0:
                    color = cls.GRAY
                    border = 1
                else:
                    color = tm.Tetromino.colors[tm.Tetromino.board_matrix[i][j]]
                    border = 0

                pg.draw.rect(win, color, 
                    [j*cls.zoom, i*cls.zoom, cls.zoom, cls.zoom], border)
    
    @classmethod
    def clear_board(cls):
        def end():
            # if any letters present at the top
            if any(tm.Tetromino.board_matrix[0]):
                return True
                
        # If all elements in board_matrix's row are != 0, clear them
        update = [tm.Tetromino.board_matrix[i] for i in range(cls.BoardHeight) \
                                    if not all(tm.Tetromino.board_matrix[i])]
        
        before_clean = len(tm.Tetromino.board_matrix)
        after_clean = len(update)
        clear_amount = before_clean - after_clean
        
        cls.score += cls.scoring[clear_amount]
        
        for _ in range(clear_amount):
            update[:0] = [[0 for _ in range(cls.BoardWidth)]]
        
        tm.Tetromino.board_matrix = update
        
        if end() and not cls.end:
            cls.end = True
            db.update_db(cls.score)
            cls.run = False
        
    @classmethod
    def rect(cls, win, color, x=1, y=1, j_mult=1, i_mult=1,):
        pg.draw.rect(win, color, [x+(j_mult*cls.zoom), y+(i_mult*cls.zoom),
                                cls.zoom - 1, cls.zoom - 1])
        
    @staticmethod
    def delta_t():
        x = lambda a : eval("%.{}f".format(1) % a)
        if x(timeit.default_timer() - Game.start) % 1 == 0:
            Game.start -= 0.1
            return True
    
    @staticmethod
    def preview(current, win, x=1, y=1, active_tetro=False):
        for i in range(4):
            for j in range(4):
                temp = i * 4 + j
                if temp in current.current_shape():
                    if not active_tetro:
                        Game.rect(win, current.color, x, y, j, i)
                    else:
                        Game.rect(win, current.color, 
                                  j_mult=current.x + j, i_mult=current.y + i)