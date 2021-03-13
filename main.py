from tetromino import Tetromino as tm
from game import Game
import pygame as pg
import os

pg.display.set_caption("Tetris")
fps = 60

def main():
    run = True
    game = Game()
    win = pg.display.set_mode((game.WIDTH, game.HEIGHT))
    
    while run:
        Game.update_window(win)
        current = game.q.current()
        current.fall()

        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    current.move(1)
                    current.ghost.move(current.x)
                elif event.key == pg.K_LEFT:
                    current.move(-1)
                    current.ghost.move(current.x)
                # softdrop
                elif event.key == pg.K_DOWN:
                    current.y += 1
                # hardrop
                elif event.key == pg.K_SPACE:
                    current.hardrop()
                # rotate
                elif event.key == pg.K_z:
                    current.rotate()
                    current.ghost.rotate()
                elif event.key == pg.K_x:
                    current.rotate(right=False)
                    current.ghost.rotate(right=False)
                # hold
                elif event.key == pg.K_LSHIFT:
                    Game.times += 1
                    Game.hold(current)
                    
        pg.time.Clock().tick(fps)

main()