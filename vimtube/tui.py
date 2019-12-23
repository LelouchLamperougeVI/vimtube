import curses
from curses import wrapper
from . import player

params={ # these settings are available to edit in ~/.config/vimtube/
    'greeting_msg': 'Welcome to VimTube! To begin, type :help', # a nice message to show at launch
    'index_gap': 10, # gap for catalogue number indices
    'scrolloff': 3, # leave margin at top/bottom
    'seek_step': 5, # number of seconds for h/l seek
    'big_seek_step': 30, # (/) seek
    'histsize': 100, # number of commands to remember in history
}

class TUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.cbreak()
        curses.noecho()
        self.selection = 0
        self.player = player.player()
        self.start_ui()

    def start_ui(self):
        self.stdscr.clear()
        self.printl(params['greeting_msg'], int(self.rx()/2 - len(params['greeting_msg'])/2), 0, curses.A_BOLD)
        self.stdscr.move(self.ry()-1,0)

    def printl(self, text, pos=0, line=None, attr=curses.A_NORMAL): #print line
        if line is None:
            line = self.ry() -1
        overflow = self.rx() - len(text) - params['index_gap']
        if overflow < 0:
            text = text[:overflow]
        self.stdscr.addstr(line, pos, text, attr)

    def ry(self):
        ry,_ = self.stdscr.getmaxyx()
        return ry

    def rx(self):
        _,rx = self.stdscr.getmaxyx()
        return rx

    def update_selection(self, pos=0):
        self.last_select = self.selection
        self.selection = pos
        r = min(self.ry(), len(self.player.catalogue))

        self.stdscr.clear()
        self.printl('Index', 0, 0, curses.A_REVERSE)
        self.printl('Title', params['index_gap'], 0, curses.A_REVERSE)
        pos = 1
        for item in self.player.catalogue:
            self.printl(str(pos), 0, pos)
            self.printl('-', params['index_gap']-2, pos)
            self.printl(item.title, params['index_gap'], pos)
            if pos-1 == self.selection:
                self.printl(item.title, params['index_gap'], pos, curses.A_STANDOUT)
            pos += 1
        self.printl('index: ' + str(self.selection + 1))

    def interpret(self, key):
        if key == ord('/'):
            token = self.sentence(key)
            self.printl('searching...')
            self.player.search(token)
            self.update_selection()
            self.printl('catalogue updated with search term: ' + token)
        elif key == ord('j'):
            if self.selection < len(self.player.catalogue):
                self.update_selection(self.selection+1)
        elif key == ord('k'):
            if self.selection > 0:
                self.update_selection(self.selection-1)
        elif key in [curses.KEY_ENTER, ord('\n')]:
            self.printl('loading...')
            self.player.load(self.selection)
            self.player.play()
        elif key == ord('p'):
            self.player.pause()
        elif key == ord('q'):
            self.player.player.stop()
        elif key == ord('h'):
            self.player.seek(-1 * params['seek_step'])
        elif key == ord('l'):
            self.player.seek(params['seek_step'])
        elif key == ord('('):
            self.player.seek(-1 * params['big_seek_step'])
        elif key == ord(')'):
            self.player.seek(params['big_seek_step'])

    def sentence(self,key=0):
        token = ''
        pos = 0
        while key not in [curses.KEY_ENTER, ord('\n')]:
            if key == curses.KEY_BACKSPACE:
                if pos > 1:
                    pos = pos - 1
                    self.cl(pos)
                    token = token[:-1]
                key = self.stdscr.getch()
                continue
            self.printl(chr(key), pos)
            key = self.stdscr.getch()
            token += chr(key)
            pos += 1
        self.cl()
        return token[:-1]

    def cl(self, pos=0, line=None): # clear a line; if line==None clear current line
        if line is None:
            line, _ = self.stdscr.getyx()
        self.stdscr.move(line, pos)
        self.stdscr.clrtoeol()

def main(stdscr):
    ui = TUI(stdscr)
    key = stdscr.getch()
    while True:
        ui.cl()
        ui.interpret(key)
        stdscr.move(ui.ry()-1,0)
        key = stdscr.getch()

if __name__ == "__main__":
    wrapper(main)
