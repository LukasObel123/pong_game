import curses
import pong_utils
import time





def show_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Pong!")
    stdscr.addstr(1, 0, "Press S to Start")
    stdscr.addstr(2, 0, "Press Q to Quit")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('s') or key == ord('S'):
            return "start"
        elif key == ord('q') or key == ord('Q'):
            return "exit"
        
def show_player_setup(stdscr):
    stdscr.clear()
    p1 = pong_utils.get_input(stdscr,"Enter Player 1 Name: ",0,0) #get p1 name as input
    p2 = pong_utils.get_input(stdscr,"Enter Player 2 Name: ",0,0) #get p2 name is input


    P1 = pong_utils.Player(p1) #Setting up Player 1 class
    P2 = pong_utils.Player(p2) #Setting up Player 2 class
    stdscr.clear()
    
    ##This checks to see if either player recieves any special bonuses and applies them
    if P1.type == "wife": 
        txt_to_print = f"Congratualtions {P1.name}!!! You recieve a +3 point wife start bonus"         
        P1.score = 3
    elif P2.type == "wife":
        txt_to_print = f"Congratualtions {P2.name}!!! You recieve a +3 point wife start bonus"
        P2.score = 3         
    else:
        txt_to_print = ""      
    stdscr.addstr(0,0,txt_to_print)
    stdscr.refresh() 

    ## Adding a loading display
    #time.sleep(1)
    stdscr.addstr(2,0,"LOADING......")
    stdscr.refresh() 
    #time.sleep(3)
    stdscr.addstr(2,0,"Done Loading :)             ")
    stdscr.refresh() 



    ## Asks if ready to play. Either returns back to the menu or starts the game
    stdscr.addstr(4,0,f"{P1.name} and {P2.name} are you read to play PONG?  \nPress enter if ready or Q to return to the menu")
    while True:
        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13):  # Enter key
            return "playing" , P1, P2
        elif key == ord('q') or key == ord('Q'):
            return "menu" , None , None


    
    