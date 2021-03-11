from Tetromino import Tetromino as tm
from Game import Game
import pygame as pg
import os

pg.display.set_caption("Tetris")
fps = 30

def main():
    run = True
    game = Game()
    win = pg.display.set_mode((game.WIDTH, game.HEIGHT))

    def update_window():
        win.fill((0, 0, 0))
        game.run_board(win)
        tm.draw(win)
        score_text = game.main_font.render(
                        f"Score = {game.score}", 1, game.WHITE)
        
        win.blit(score_text, (game.WIDTH - score_text.get_width() -5,
                                        score_text.get_height() - 5))

        pg.display.update()
    
    while run:
        update_window()
        current = tm.tetr_list[-1]
        current.fall()

        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    current.move()
                elif event.key == pg.K_LEFT:
                    current.move(operation="left")
                # softdrop
                elif event.key == pg.K_DOWN:
                    current.fall()
                # hardrop
                elif event.key == pg.K_SPACE:
                    current.hardrop()
                elif event.key == pg.K_x:
                    current.rotate()
                elif event.key == pg.K_z:
                    current.rotate(right=False)

        pg.time.Clock().tick(fps)

main()