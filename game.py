from pong_utils import Ball, Border, Padel

import pong_utils
import time
import curses






def play(stdscr,P1,P2):
    stdscr.clear()
    ball = Ball(stdscr) #lets make our ball
    border = Border(stdscr)
    p_left = Padel(stdscr,"left")
    p_right = Padel(stdscr,"right")
    dt = 1/24 #Frame Rate

    Updates = [ball,p_left,p_right]
    #Game Loop
    while True:
        
        stdscr.erase()
        
        #Lets get the key inputs 
        key = stdscr.getch()

        ##Add the score board
        pong_utils.draw_scorecard(stdscr,P1,P2)


        #lets update anything that needs upadting
        for pong_object in Updates:
            pong_object.update(dt,key)
        

        ball.draw()
        border.draw()
        p_left.draw()
        p_right.draw()

        
        
        stdscr.refresh()
        time.sleep(dt)



