import copy
import sys
import pygame
import random
import numpy as np
from constants import *
import time
from pygame import mixer



# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# --- CLASSES ---


class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares 
        self.marked_sqrs = 0

    def final_state(self, show=False):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]


    def minimax(self, board, maximizing):

        case = board.final_state()
        if case == 1:
            return 1, None  # eval, move

        if case == 2:
            return -1, None

        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)   #in this case self.player=2
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move



    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
            print( f'Random has chosen to mark the square in pos {move} with an eval of: {eval}')            
        else:
            eval, move = self.minimax(main_board, False)
            print( f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move 


class Game:

    def __init__(self,run=True):
        self.board = Board()
        self.ai = AI()
        self.player = 1  
        self.gamemode = 'ai'  
        self.running = run
        self.show_lines()

    def show_lines(self):
    
        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0),(WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE),(WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE),(WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col, p1_object, p2_object):
        if self.player == 1:
            if (p1_object == 1):
                start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
                end_desc = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + SQSIZE - OFFSET)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
         
                start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
                end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            elif(p1_object == 2):    
                rec_x = (col * SQSIZE + OFFSET)
                rec_y = (row * SQSIZE + OFFSET)
                pygame.draw.rect(screen, CROSS_COLOR,pygame.Rect(rec_x, rec_y, 100, 100))
            elif(p1_object == 3):    
                rec_x = (col * SQSIZE + OFFSET)
                rec_y = (row * SQSIZE + OFFSET)
                pygame.draw.ellipse(screen, CROSS_COLOR,[rec_x-30, rec_y, 160, 100],width=10)

        elif self.player == 2:
            if (p2_object == 1):
                center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
            elif(p2_object == 2):    
                rec_x = (col * SQSIZE + OFFSET)
                rec_y = (row * SQSIZE + OFFSET)
                pygame.draw.rect(screen, CIRC_COLOR,pygame.Rect(rec_x-30, rec_y, 160, 100))
            elif (p2_object == 3):
                poly1 = (col * SQSIZE + OFFSET-20, row * SQSIZE + OFFSET)
                poly2 = (col * SQSIZE + SQSIZE -20,row * SQSIZE + SQSIZE - OFFSET)
                poly3 = (col * SQSIZE + SQSIZE - OFFSET-20, row * SQSIZE + OFFSET)
                pygame.draw.polygon(screen, CIRC_COLOR, [poly1, poly3, poly2], width=10)

    def make_move(self, row, col, p1_object, p2_object):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col, p1_object, p2_object)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        # if(self.gamemode == 'pvp'):
        #     self.gamemode = 'ai'
        # else:
        #     self.gamemode = 'pvp'    
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self,run):
        self.__init__(run)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def beep():
    pygame.mixer.init()
    pygame.mixer.music.load('beep.mp3')
    pygame.mixer.music.play()
def win():
    pygame.mixer.init()
    pygame.mixer.music.load('win.mp3')
    pygame.mixer.music.play()
def main_menu(font,TEXT_COL,font1,TEXT_COL1):
    screen.fill((52, 78, 91))
    draw_text("Main Menu", font1, TEXT_COL1, 150, 100)
    draw_text("[s] Start Game", font, TEXT_COL,50 , 150)
    draw_text("[p] Player Vs Player", font, TEXT_COL, 50, 200)
    draw_text("[b] Player Vs Computer Random Base", font, TEXT_COL, 50, 250)
    draw_text("[a] Player Vs Computer AI Base", font, TEXT_COL, 50, 300)
    draw_text("[q] Quit The Game", font, TEXT_COL, 50, 350)
# def fig_select_p1(font,TEXT_COL,font1,TEXT_COL1):
#     screen.fill((52, 78, 91))
#     draw_text("Main Menu", font1, TEXT_COL1, 150, 80)
#     draw_text("[1] Cross", font, TEXT_COL,50 , 130)
#     draw_text("[2] Square", font, TEXT_COL, 50, 160)
#     draw_text("[3] Ellipse", font, TEXT_COL, 50, 190)
#     for event in pygame.event.get():
#         if event.type==pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 return 1
#             if event.key == pygame.K_2:
#                 return 2
#             if event.key == pygame.K_3:
#                 return 3
# def fig_select_p2(font,TEXT_COL,font1,TEXT_COL1):
#     draw_text("Player2 Figure Select", font1, TEXT_COL1, 150, 215)
#     draw_text("[1] Circle", font, TEXT_COL,50 , 250)
#     draw_text("[2] Rectangle", font, TEXT_COL, 50, 280)
#     draw_text("[3] Polygon", font, TEXT_COL, 50, 310)
#     for event in pygame.event.get():
#         if event.type==pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 return 1
#             if event.key == pygame.K_2:
#                 return 2
#             if event.key == pygame.K_3:
#                 return 3

def main():

    game = Game(False)
    board = game.board
    ai = game.ai  

    print('select figure for player 1\n [1]Cross\n [2]Square \n [3]Ellipse')
    p1_object = int(input())
    print('select figure for player 2\n [1]Circle\n [2]Rectangle\n [3]Polygon')
    p2_object = int(input())
    

    #define fonts
    font = pygame.font.SysFont("arialblack", 20)
    #define colours
    TEXT_COL = (17, 17, 18)
    #define fonts
    font1 = pygame.font.SysFont("arialblack", 30)
    #define colours
    TEXT_COL1 = (3, 252, 98)
    TEXT_COL3 = (255, 255, 255)
    font3 = pygame.font.SysFont("arialblack", 40)
    # p1_object=fig_select_p1(font,TEXT_COL,font1,TEXT_COL1)
    # p2_object=fig_select_p2(font,TEXT_COL,font1,TEXT_COL1)
    main_menu(font,TEXT_COL,font1,TEXT_COL1)
  

    while True:

        for event in pygame.event.get():

            if event.type==pygame.KEYDOWN:
                beep()
                if event.key == pygame.K_p:
                    game.reset(True)
                    board = game.board
                    game.change_gamemode()

                if event.key == pygame.K_b:
                    game.reset(True)
                    board = game.board                    
                    ai.level = 0

                if event.key == pygame.K_a:
                    game.reset(True)
                    board = game.board
                    ai.level = 1
                if event.key == pygame.K_r:
                    game.reset(True)
                    board = game.board
                    ai = game.ai
                if event.key == pygame.K_s:
                    game.reset(True)
                    board = game.board
                    ai = game.ai                            
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # print(f"print: {pos}")
                row = pos[1] // SQSIZE
                # print(f"Row: {row}")
                col = pos[0] // SQSIZE
                # print(f"Col: {col}")

                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col, p1_object, p2_object)
                    beep()

                    if game.isover():
                        game.running = False
                        win()
                        draw_text("[r] Restart Game", font3, TEXT_COL3, 50, 250)
                        draw_text("[q] Quit Game", font3, TEXT_COL3, 50, 300)                     

        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            
            pygame.display.update()
            time.sleep(1)  
            # eval
            row, col = ai.eval(board)
            game.make_move(row, col, p1_object, p2_object)
            beep()

            if game.isover():

                game.running = False
                win()
                draw_text("[r] Restart Game", font3, TEXT_COL3, 50, 250)
                draw_text("[q] Quit Game", font3, TEXT_COL3, 50, 300)                 

        pygame.display.update()

main()
