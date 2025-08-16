#!/usr/bin/env python3

import time
import curses
import pong_utils
import menu
import game




def main(stdscr):

    curses.curs_set(0)            # Hide the blinking cursor
    stdscr.nodelay(True)          # Don't wait for key input
    
    
    state = "menu"

    while state != "exit":
        stdscr.erase()

        if state == "menu":
            state = menu.show_menu(stdscr)
        elif state == "start":
            state,P1,P2 = menu.show_player_setup(stdscr)
        elif state == "playing":
            pong_utils.countdown(stdscr,3)

            while True:
                game.play(stdscr,P1,P2)

        
        stdscr.refresh()



if __name__ == "__main__":
    curses.wrapper(main)








