import curses
from curses import wrapper
import player

greeting_msg = 'Welcome to VimTube! To begin, type :help'

class TUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selection = 0
        self.player = player.player()
        self.start_ui()
        
    def start_ui(self):
        self.rx, self.ry = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.stdscr.addstr(0, int(self.ry/2 - len(greeting_msg)/2), greeting_msg, curses.A_STANDOUT)
        self.stdscr.move(self.rx-1,0)
        
    def update_selection(self, pos=0):
        self.selection = pos
        self.stdscr.clear()
        pos = 0
        for item in self.player.catalogue:
            self.stdscr.addstr(pos, 0, str(pos) + '-')
            self.stdscr.addstr(pos, 5, item.title)
            if pos == self.selection:
                self.stdscr.addstr(pos, 5, item.title, curses.A_STANDOUT)
            pos += 1
        self.stdscr.addstr(self.rx-1,0, 'selection: ' + str(self.selection))
        
    def interpret(self, key):
        if key == ord('/'):
            token = self.sentence(key)
            self.stdscr.addstr(self.rx-1,0, 'searching...')
            self.stdscr.refresh()
            self.player.search(token)
            self.update_selection()
            self.stdscr.addstr(self.rx-1,0, 'catalogue updated with search term: ' + token)
        elif key == ord('j'):
            if self.selection < len(self.player.catalogue):
                self.update_selection(self.selection+1)
        elif key == ord('k'):
            if self.selection > 0:
                self.update_selection(self.selection-1)
    
    def sentence(self,key=0):
        token = ''
        pos = 0
        while key not in [curses.KEY_ENTER, ord('\n')]:
            if key == curses.KEY_BACKSPACE:
                pos = pos - 1
                self.stdscr.addstr(self.rx-1,pos, ' ')
                self.stdscr.move(self.rx-1,pos)
                token = token[:-1]
                key = self.stdscr.getch()
                continue
            self.stdscr.addstr(self.rx-1,pos, chr(key))
            key = self.stdscr.getch()
            token += chr(key)
            pos += 1
        return token[:-1]

def main(stdscr):
    ui = TUI(stdscr)

    key = stdscr.getch()
    while key != ord('q'):
        ui.interpret(key)
        stdscr.move(ui.rx-1,0)
        key = stdscr.getch()

wrapper(main)