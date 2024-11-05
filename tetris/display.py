from os import get_terminal_size as console_size
from math import ceil
from random import choice, randint
from time import sleep

sizes = {
    "classic": (20, 20),
    "beta": (24, 20)
}

shapes = {
    "L": ((-1, 1), (1, 0), (-1, 0)),
    "J": ((1, 1), (1, 0), (-1, 0)),
    "O": ((-1, 1), (0, 1), (-1, 0)),
    "I": ((1, 0), (-2, 0), (-1, 0)),
    "S": ((0, 1), (-1, 1), (1, 0)),
    "Z": ((-1, 0), (0, 1), (1, 1)),
    "T": ((-1, 0), (1, 0), (0, 1)),
    "L5": ((-1, 1), (1, 0), (-1, 0), (2, 0)),
    "J5": ((1, 1), (1, 0), (-1, 0), (-2, 0)),
    "HT15": ((0, 1), (1, 0), (-1, 0), (-2, 0)),
    "HT25": ((0, -1), (1, 0), (-1, 0), (-2, 0)),
    "I5": ((1, 0), (-2, 0), (-1, 0), (2, 0)),
    "S5": ((0, 1), (-1, 1), (1, 0), (2, 0)),
    "Z5": ((-1, 0), (0, 1), (1, 1), (-2, 0)),
    "ST5": ((-1, 0), (1, 0), (0, 1), (0, -1)),
    "P5": ((0, 1), (1, 1), (1, 0), (0, -1)),
    "Q5": ((0, 1), (1, 1), (1, 0), (-1, 0)),
    "C5": ((1, 0), (-1, 0), (1, -1), (-1, -1)),
    "BT5": ((0, 2), (-1, 0), (1, 0), (0, 1)),
    "E5": ((-1, 0), (-1, 1), (0, -1), (1, -1)),
    "SL5": ((0, 1), (0, 2), (1, 0), (2, 0)),
    "BL5": ((0, 1), (0, 2), (-1, 0), (-2, 0))
}


shapes_4blocks = ("L", "J", "O", "O", "I", "I", "S", "Z", "T", "T")
shapes_5blocks = ("L5", "J5", "HT15", "HT25", "I5", "I5", "S5",
                  "Z5", "ST5", "BT5", "P5", "Q5", "C5", "E5", "BT5", "SL5", "BL5")
shape_names = {
    "classic": shapes_4blocks,
    "beta": shapes_5blocks*2 + shapes_4blocks,
}

palette = ("red", "green", "yellow", "blue", "purple")

format = {
    "regular": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underlined": "\033[4m",
    "fore": {"black": "\033[30m",
             "red": "\033[31m",
             "green": "\033[32m",
             "yellow": "\033[33m",
             "blue": "\033[34m",
             "purple": "\033[35m",
             "teal": "\033[36m",
             "gray": "\033[37m"},
    "back": {"black": "\033[40m",
             "red": "\033[41m",
             "green": "\033[42m",
             "yellow": "\033[43m",
             "blue": "\033[44m",
             "purple": "\033[45m",
             "teal": "\033[46m",
             "gray": "\033[47m"},
    "from-beginning": "\033[1;1H"
}


theme = {
    "classic": format["regular"],
    "beta": format["fore"]["blue"]
}


class Screen:
    def __init__(self, format=format["regular"]):
        self.default = format
        self.clear()
        return

    def clear(self, fill=" "):
        self.matrix = [[fill]*console_size()[0]
                       for i in range(console_size()[1])]
        return

    def __repr__(self):
        stdout = format["from-beginning"] + self.default
        stdout += "\n".join(["".join(row) for row in self.matrix])
        return stdout

    def show(self):
        print(self, end="")
        return

    def add_window(self, window):
        window.paused = False
        x_begin = window.pos[0]
        y_begin = window.pos[1]
        x_end = window.pos[0] + window.size[0] + 1
        y_end = window.pos[1] + window.size[1] + 1
        # Borders & Fill
        try:
            char_size = len(window.fill)
            for i in range(x_begin, x_end+1):
                if i < 1:
                    raise IndexError
                for j in range(y_begin, y_end+1):
                    if j < 1:
                        raise IndexError
                    if (x_begin < i < x_end) and (y_begin < j < y_end):
                        self.matrix[j-1][i-1] = window.fill_format + \
                            window.fill[i % char_size] + self.default
                    elif x_begin < i < x_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.horizontal + self.default
                    elif y_begin < j < y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.vertical + self.default
                    elif i == x_begin and j == y_begin:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[0] + self.default
                    elif i == x_end and j == y_begin:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[1] + self.default
                    elif i == x_begin and j == y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[2] + self.default
                    elif i == x_end and j == y_end:
                        self.matrix[j-1][i-1] = window.border_format + \
                            window.corners[3] + self.default
            # Header
            pos = window.pos[0] + (window.size[0] - len(window.header)) // 2
            for char in window.header:
                self.matrix[y_begin-1][pos] = window.header_format + \
                    char + self.default
                pos += 1
            # Text
            for text, pos, size, format in window.text:
                for i in range(size):
                    self.matrix[y_begin+pos[1]-1][x_begin+pos[0] +
                                                  i-1] = format + text[i] + self.default

            # Shape
            if window.shape:
                if window.main:
                    pos = window.land_pos()
                    for block in window.shape.blocks:
                        if (x_begin < window.pos[0]+(pos[0]+block[0])*2 < x_end) and (y_begin < window.pos[1]+pos[1]+block[1] < y_end):
                            self.matrix[window.pos[1]+pos[1]+block[1]-1][window.pos[0]+(
                                pos[0]+block[0])*2-2] = window.shape.color + "░" + self.default
                            self.matrix[window.pos[1]+pos[1]+block[1]-1][window.pos[0]+(
                                pos[0]+block[0])*2-1] = window.shape.color + "░" + self.default

                pos = window.shape.pos
                for block in window.shape.blocks:
                    if (x_begin < window.pos[0]+(pos[0]+block[0])*2 < x_end) and (y_begin < window.pos[1]+pos[1]+block[1] < y_end):
                        self.matrix[window.pos[1]+pos[1]+block[1]-1][window.pos[0] +
                                                                     (pos[0]+block[0])*2-2] = window.shape.color + "█" + self.default
                        self.matrix[window.pos[1]+pos[1]+block[1]-1][window.pos[0] +
                                                                     (pos[0]+block[0])*2-1] = window.shape.color + "█" + self.default
            # Fixed Blocks
            for block in window.fixed_blocks:
                if (x_begin < window.pos[0]+block[0]*2 < x_end) and (y_begin < window.pos[1]+block[1] < y_end):
                    self.matrix[window.pos[1]+block[1]-1][window.pos[0] +
                                                          block[0]*2-2] = block[2] + "█" + self.default
                    self.matrix[window.pos[1]+block[1]-1][window.pos[0] +
                                                          block[0]*2-1] = block[2] + "█" + self.default
        except IndexError:
            if window.main:
                window.paused = True
                pause = Window(size=(console_size()[0]-2, console_size()[1]-2))
                pause.text = []
                pause.add_text(text="PAUSED", pos=[
                               "m", ceil(console_size()[1]/2)-1])
                self.clear()
                self.add_window(pause)
            else:
                self.clear()
        return


class Window:
    break_time = 1
    paused = False
    main = True
    text = []

    def __init__(self,  size, pos=("m", "m")):
        self.size = size
        self.set_pos(pos)
        self.set_border()
        self.set_fill()
        self.set_header(title="")
        self.shape = None
        self.matrix = [[-1]+[0]*(self.size[0]//2)+[-1]
                       for _ in range(self.size[1]+1)] + [[-1]*(self.size[0]//2+2)]
        self.fixed_blocks = []
        return

    def land_pos(self):
        x_pos, y_pos = self.shape.pos
        while y_pos < len(self.matrix):
            if not self.can_move(pos=(x_pos, y_pos)):
                return (x_pos, y_pos)
            y_pos += 1
        return

    def set_pos(self, pos):
        pair = list(pos)
        if pair[0] == "m":
            pair[0] = (console_size()[0] - self.size[0]) // 2
        if pair[1] == "m":
            pair[1] = (console_size()[1] - self.size[1]) // 2
        self.pos = tuple(pair)
        return

    def set_shape(self, shape, pos=("m", "u")):
        self.shape = shape
        shape.name = choice(shape.names)
        pairs = shapes[shape.name]
        self.shape.blocks = [[0, 0]] + [list(pair) for pair in pairs]
        self.shape.set_pos(pos, self.size)
        shape.color_name = choice(shape.palette)
        shape.color = format["fore"][shape.color_name]
        return

    def add_text(self, text, pos, format=format["regular"]):
        if pos[0] == "l":
            pos[0] = 2
        elif pos[0] == "r":
            pos[0] = self.size[0] - len(text)
        elif pos[0] == "m":
            pos[0] = (self.size[0] - len(text)) // 2 + 1
        self.text.append((text, pos, len(text), format))
        return

    def can_move(self, direction="d", pos=None):
        if not pos:
            pos = self.shape.pos
        try:
            if direction == "d":
                for block in self.shape.blocks:
                    if pos[1]+block[1]+1 >= 0 and self.matrix[pos[1]+block[1]+1][pos[0]+block[0]] in [-1, 1]:
                        return False
            elif direction == "r":
                for block in self.shape.blocks:
                    if pos[1]+block[1] >= 0 and self.matrix[pos[1]+block[1]][pos[0]+block[0]+1] in [-1, 1]:
                        return False
            elif direction == "l":
                for block in self.shape.blocks:
                    if pos[1]+block[1] >= 0 and self.matrix[pos[1]+block[1]][pos[0]+block[0]-1] in [-1, 1]:
                        return False
        except IndexError:
            return False
        return True

    def can_rotate(self, direction="c"):
        # if self.shape.name == "O":
        #     return False
        new_positions = []
        if direction == "c":
            for block in self.shape.blocks:
                new_positions.append((-block[1], block[0]))
        elif direction == "a":
            for block in self.shape.blocks:
                new_positions.append((block[1], -block[0]))
        try:
            for position in new_positions:
                if self.shape.pos[1]+position[1] >= 0 and self.matrix[self.shape.pos[1]+position[1]][self.shape.pos[0]+position[0]] in [-1, 1]:
                    return False
        except:
            return False
        return True

    def fix_shape(self):
        for block in self.shape.blocks:
            self.fixed_blocks.append(
                (self.shape.pos[0]+block[0], self.shape.pos[1]+block[1], self.shape.color))
            self.matrix[self.shape.pos[1]+block[1]
                        ][self.shape.pos[0]+block[0]] = 1
        return

    def set_border(self, vertical="│", horizontal="─", corners=("╭", "╮", "╰", "╯"), format=format["regular"]):
        self.vertical = vertical
        self.horizontal = horizontal
        self.corners = corners
        self.border_format = format
        return

    def set_header(self, title, format=format["regular"]):
        self.header = title
        self.header_format = format
        return

    def set_fill(self, fill=" ", format=format["regular"]):
        self.fill = fill
        self.fill_format = format
        return

    def move(self, direction="d", distance=1):
        if self.paused or not self.can_move(direction=direction):
            return False
        if direction == "d":
            self.shape.set_pos((self.shape.pos[0], self.shape.pos[1]+distance))
        elif direction == "r":
            self.shape.set_pos((self.shape.pos[0]+distance, self.shape.pos[1]))
        elif direction == "l":
            self.shape.set_pos((self.shape.pos[0]-distance, self.shape.pos[1]))
        return

    def rotate(self, direction="c"):
        if self.paused or not self.can_rotate():
            return False
        new_positions = []
        if direction == "c":
            for block in self.shape.blocks:
                new_positions.append((-block[1], block[0]))
        elif direction == "a":
            for block in self.shape.blocks:
                new_positions.append((block[1], -block[0]))
        self.shape.blocks = new_positions
        return

    def game_over(self):
        if 1 in self.matrix[1]:
            self.set_header(
                "GAME-OVER", format=format["fore"]["red"]+format["bold"])
            self.set_border(format=format["fore"]["red"])
            return True
        return False

    def remove_line(self):
        for i in range(len(self.matrix)-2, 1, -1):
            if all(self.matrix[i][1:-1]) == 1:
                print("\a", end="")
                del self.matrix[i]
                self.matrix.insert(0, [-1]+[0]*(self.size[0]//2)+[-1])
                temp = []
                for j in range(len(self.fixed_blocks)):
                    if self.fixed_blocks[j][1] != i:
                        temp.append(list(self.fixed_blocks[j]))
                for j in range(len(temp)):
                    if temp[j][1] < i:
                        temp[j][1] += 1
                self.fixed_blocks = [tuple(block) for block in temp]
                return True
        return False

    def auto_move(self):
        while True:
            if not self.paused and self.can_move():
                self.move()
            sleep(self.break_time)
        return

    def drop(self):
        if self.paused:
            return False
        self.shape.pos = self.land_pos()
        return


class Shape:

    def __init__(self, names=shape_names["classic"], palette=palette):
        self.names = names
        self.palette = palette
        return

    def set_pos(self, pos, window_size=None):
        pair = list(pos)
        if pair[0] == "m":
            pair[0] = ceil(window_size[0] / 4)
        if pair[1] == "u":
            pair[1] = 0
        elif pair[1] == "m":
            pair[1] = ceil(window_size[1] / 2)
        self.pos = tuple(pair)
        return


def welcome():
    scr = Screen()
    welcome = Window(size=(16, 2), pos=("m", "m"))
    welcome.set_border(horizontal=" ", vertical=" ",
                       corners=(" ", " ", " ", " "))
    goal = "tetris"
    new = [""] * 6
    remaining = 6
    progress = 0.0
    while progress < 10 or remaining > 0:
        if remaining > 0:
            remaining = 0
            for i in range(6):
                if new[i] != goal[i]:
                    remaining += 1
                    new[i] = chr(randint(97, 122))
        if progress < 10:
            progress += 0.2
        welcome.text = []
        welcome.add_text(text="  ".join(new), pos=["m", 1],
                         format=format["fore"]["blue"])
        welcome.add_text(text="━"*16, pos=[1, 2])
        welcome.add_text(text="━"*(6-remaining+int(progress)),
                         pos=[1, 2], format=format["fore"]["red"])
        welcome.set_pos(pos=("m", "m"))
        scr.clear()
        scr.add_window(welcome)
        scr.show()
        sleep(0.05)
    sleep(0.5)


def message(message, time, format):
    scr = Screen()
    popup = Window(size=(16, 2), pos=("m", "m"))
    popup.set_border(horizontal=" ", vertical=" ",
                     corners=(" ", " ", " ", " "))

    while time > 0:
        popup.text = []
        popup.add_text(text=message, pos=["m", 1],
                       format=format)
        popup.set_pos(pos=("m", "m"))
        scr.clear()
        scr.add_window(popup)
        scr.show()
        sleep(0.05)
        time -= 0.05
