import pygame as pg, sys, time
from pygame.locals import *
from ai import com


# Global variables
win = 0
lose = 0
tie = 0
XO = False
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)
TTT = [[None]*3, [None]*3, [None]*3]    #Board


# Initializing game window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100), 0, 32)
pg.display.set_caption("TicTacToe")
time.sleep(1)


# Loading the image
opening = pg.image.load('tictac.png')
x_img = pg.image.load('x.jpeg')
o_img = pg.image.load('o.jpeg')


# Resizing the image
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height+100))


def game_opening():
    screen.fill(white)

    #Drawing vertical line
    pg.draw.line(screen, line_color, (width/3, 0), (width/3, height), 7)
    pg.draw.line(screen, line_color, (width/3*2, 0), (width/3*2, height), 7)
    #Drawing horizontal line
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, height/3*2), (width, height/3*2), 7)
    draw_status()


def draw_status():
    global draw, win, lose, tie

    score =  "You(X):   Win {}   Lose {}   Tie {}".format(win, lose, tie)
    if winner is None:
        turn = "Your" if not XO else "Computer"
        message = turn + "'s Turn"
    else:
        turn = "You" if not winner else "Computer"
        message = turn + " Won!"
    if draw:
        message = "Game Draw!"

    font  = pg.font.Font(None, 30)
    text = font.render(message, 1, white)
    score = font.render(score, 1, white)

    #copy the rendered message onto board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-80))
    score_rect = score.get_rect(center=(width/2, 500-40))
    screen.blit(score, score_rect)
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global TTT, winner, draw, tie, win, lose

    for i in range(0,3):
        # Check for winning rows
        if ((TTT[i][0]==TTT[i][1]==TTT[i][2]) and (TTT[i][0] is not None)):
            winner = TTT[i][0]
            if winner:
                lose += 1
            else:
                win += 1
            pg.draw.line(screen, (250,0,0), (0, (i+1)*height/3-height/6), (width,(i+1)*height/3-height/6),4)
            break
        # Check for winning columns
        if ((TTT[0][i]==TTT[1][i]==TTT[2][i]) and (TTT[0][i] is not None)):
            winner = TTT[0][i]
            if winner:
                lose += 1
            else:
                win += 1
            pg.draw.line(screen, (250,0,0), ((i+1)*width/3-width/6, 0), ((i+1)*width/3-width/6, height),4)
            break

    # Check for diagonal winners
    if (TTT[0][0]==TTT[1][1]==TTT[2][2]) and (TTT[1][1] is not None):
        winner =  TTT[1][1]
        if winner:
            lose += 1
        else:
            win += 1
        pg.draw.line(screen, (250,70,70), (50,50), (350,350), 4)
    
    if (TTT[0][2]==TTT[1][1]==TTT[2][0]) and (TTT[1][1] is not None):
        winner =  TTT[1][1]
        if winner:
            lose += 1
        else:
            win += 1
        pg.draw.line(screen, (250,70,70), (350,50), (50,350), 4)

    if (not any(None in sub for sub in TTT) and winner is None):
        draw = True
        tie += 1
    draw_status()


def drawXO(row, col):
    global TTT, XO
    if row==0:
        posx = 30
    if row==1:
        posx = width/3 + 30
    if row==2:
        posx = width/3*2 + 30
    
    if col==0:
        posy = 30
    if col==1:
        posy = height/3 + 30
    if col==2:
        posy = height/3*2 + 30

    TTT[row][col] = XO
    if not XO:
        screen.blit(x_img, (posy,posx))
        XO = True
        # AI's Turn
        val, move = com(TTT, True, 0, -1e7, 1e7)
        if move is not None:
            drawXO(move[0], move[1])
    else:
        screen.blit(o_img, (posy, posx))
        XO = False
    pg.display.update()


def user_click():
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()

    #get column of mouse click (1-3)
    if(x<width/3):
        col=0
    elif(x<width/3*2):
        col=1
    elif(x<width):
        col=2
    else:
        return

    #get row of mouse click (1-3)
    if(y<height/3):
        row=0
    elif(y<height/3*2):
        row=1
    elif(y<height):
        row=2
    else:
        return

    if TTT[row][col] is None:
        drawXO(row, col)
        check_win()


def reset_game():
    global TTT, winner, XO, draw, tie, win , lose
    time.sleep(1)
    XO = False
    draw = False
    winner = None
    TTT = [[None]*3, [None]*3, [None]*3]
    game_opening()


if __name__ == '__main__':
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    game_opening()
    #run the game loop forever
    while(True):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                user_click()
                if(winner is not None or draw):
                    reset_game()
        pg.display.update()
        CLOCK.tick(fps)