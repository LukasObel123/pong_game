import time
import curses
import math

## DEFINE SOME IMPORTANT CONSTANTS ##


BIG_TEXT = {
    '3': [
        " █████ ",
        "     █ ",
        " █████ ",
        "     █ ",
        " █████ "
    ],
    '2': [
        " █████ ",
        "     █ ",
        " █████ ",
        " █     ",
        " █████ "
    ],
    '1': [
        "   █   ",
        "  ██   ",
        "   █   ",
        "   █   ",
        " █████ "
    ],
    'GO': [
        " █████   █████ ",
        " █       █   █ ",
        " █   ██  █   █ ",
        " █   █   █   █ ",
        " █████   █████ "
    ],
    'PADDLE':[
        "██",
        "██",
        "██",
        "██",
        "██"  
    ]
    
}

SCORECARD_OFFSET = 10

## IMPORTANT HELPER FUNCTIONS ##


def draw_big_text(stdscr, lines, y, x):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i, x, line)
        except curses.error:
            pass  # Ignore if off-screen

def countdown(stdscr, start=3):
    height, width = stdscr.getmaxyx()
    for n in range(start, 0, -1):
        stdscr.clear()
        num_str = str(n)
        lines = BIG_TEXT[num_str]
        text_width = len(lines[0])
        x = (width - text_width) // 2
        y = (height - len(lines)) // 2
        draw_big_text(stdscr, lines, y, x)
        stdscr.refresh()
        time.sleep(1)

    # Show "GO"
    stdscr.clear()
    lines = BIG_TEXT['GO']
    text_width = len(lines[0])
    x = (width - text_width) // 2
    y = (height - len(lines)) // 2
    draw_big_text(stdscr, lines, y, x)
    stdscr.refresh()
    time.sleep(1)





def draw_scorecard(stdscr,P1,P2):
    height, width = stdscr.getmaxyx()
    title_x = width//2-len("scoreboard")//2
    stdscr.addstr(height - 9,title_x,"SCOREBOARD")
    stdscr.addstr(height - 8,title_x,"__________")
    stdscr.addstr(height - 5, width//8*3,f"{P1.name}: {P1.score}")
    stdscr.addstr(height - 5, width//8*5,f"{P2.name}: {P2.score}")
    

def draw_insructions(stdscr):
    height, width = stdscr.getmaxyx()

    stdscr.addstr(height-9,0,"Instructions")
    stdscr.addstr(height-8,0,"____________")
    stdscr.addstr(height-7,"1. Press space to pause")
    stdscr.addstr(height-6,"2. Press esc to return to menu")











              
def get_input(stdscr, prompt, y, x, max_len=20):
    curses.echo(False)  # We'll draw characters manually
    name = ""
    while True:
        stdscr.erase()
        stdscr.addstr(y, x, prompt)
        stdscr.addstr(y, len(prompt)+1, name)
        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10, 13):  # Enter key
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            name = name[:-1]
        elif 32 <= key <= 126 and len(name) < max_len:  # Printable characters
            name += chr(key)

    return name



    


class PongObject:
    def __init__(self,stdscr,type):
        self.stdscr = stdscr
        self.__type__ = type
        height, width = self.stdscr.getmaxyx()
        self.max_y = height
        self.max_x = width
        

    def update():
        pass 
    
    def draw():
        pass

class Border(PongObject):
    def __init__(self,stdscr):
        super().__init__(stdscr,type="border")
        
    def draw(self):
    # Vertical lines
        for y in range(self.max_y - SCORECARD_OFFSET):  # leave last row alone
            self.stdscr.addch(y+1, 0, '|')
            self.stdscr.addch(y+1, self.max_x - 1, '|')

        # Horizontal lines
        for x in range(1,self.max_x - 1):  # leave last column alone
            self.stdscr.addch(0, x, '-')
            self.stdscr.addch(self.max_y - SCORECARD_OFFSET, x, '-')
        
        


class Ball(PongObject):
    def __init__(self,stdscr):
        super().__init__(stdscr,type="ball")
        self.pos_x = self.max_x // 2
        self.pos_y = (self.max_y- SCORECARD_OFFSET) // 2
        self.vel_x = 20
        self.vel_y = 0

    def update(self,dt,key=""):
        self.pos_x = self.pos_x + self.vel_x*dt
        self.pos_y = self.pos_y + self.vel_y*dt

    def intersect(self,padel_left,padel_right):
        #Check intersection between ball and upper/lower boundary
        if self.pos_y < 1 or self.pos_y > self.max_y-SCORECARD_OFFSET-1:
            self.vel_y *= -1
            
        
        if self.pos_x < 2:
            #Checks for intersect with left padel
            p_min = padel_left.pos_y - padel_left.height // 2
            p_max = padel_left.pos_y + padel_left.height // 2
            if p_min <= self.pos_y <= p_max:
                self.vel_x *= -1
                self.pos_x += 0.5
        elif self.pos_x > self.max_x - 2:
            #Checks for intersect with right padel
            p_min = padel_right.pos_y - padel_right.height // 2
            p_max = padel_right.pos_y + padel_right.height // 2
            if p_min <= self.pos_y <= p_max:
                self.vel_x *= -1
                self.pos_x -= 0.5
        
        
        

        
    def draw(self):
        #x = math.floor(self.pos_x)
        #y = math.floor(self.pos_y)
        x = round(self.pos_x)
        y = round(self.pos_y)
        self.stdscr.addch(y,x, 'O')

class Padel(PongObject):
    def __init__(self,stdscr,type="",height=3):
        super().__init__(stdscr,type)
        self.type = type
        self.height = height
        if self.type == "left":
            self.pos_x = 1
            self.pos_y = (self.max_y-SCORECARD_OFFSET)// 2
        elif self.type == "right":
            self.pos_x = self.max_x-2
            self.pos_y = (self.max_y-SCORECARD_OFFSET)// 2
        else:
            raise Exception("Must declare padel either left or right")

    def update(self,dt="",key=""):
        if self.type == "left":
            if key == ord("w"):
                self.pos_y -= 1
            elif key == ord("s"):
                self.pos_y += 1
        elif self.type == "right":
            if key == curses.KEY_UP:
                self.pos_y -= 1
            elif key == curses.KEY_DOWN:
                self.pos_y += 1
        

    def draw(self):
        half = self.height // 2
        for i in range(-half, self.height - half):
            self.stdscr.addch(self.pos_y + i, self.pos_x, '|')



class Player:
    def __init__(self,name,type = "",score = 0):
        self.name = name
        self.type = type
        self.score = score
        if self.name.lower() == "carly":
            self.type = "wife" 
        elif self.name.lower() == "lukas":
            self.type = "husband"