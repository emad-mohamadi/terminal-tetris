import keyboard
import display
import json
from threading import Thread
from display import format, theme, sizes
from time import sleep


class Game:
    data_path = "data.txt"
    n = 0
    high_score = 0
    best_level = 1
    max_lines = 0
    score = 0
    multiline = 0
    combo = 0
    lines = 0
    level = 1
    experiment = 0
    running = False
    pressed_key = None

    def __init__(self, size=sizes["classic"], mode="classic", fps=20):
        self.size = size
        self.mode = mode
        self.gap = 1 / fps
        return

    def login(self):
        screen = display.Screen()
        win = display.Window(size=[18, 6])
        win.set_header(title="Login")
        win.set_border()

        keyboard.add_hotkey("enter", self.press_key, args=["enter"])
        keyboard.add_hotkey("backspace", self.press_key, args=["backspace"])
        keyboard.add_hotkey("shift+s", self.press_key, args=["S"])
        keyboard.add_hotkey("shift+q", self.press_key, args=["Q"])
        for i in range(97, 123):
            keyboard.add_hotkey(chr(i), self.press_key, args=[chr(i)])

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="Sign up", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 6])
            win.add_text(text="S", pos=["r", 5], format=format["underlined"])
            win.add_text(text="Q", pos=["r", 6], format=format["underlined"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    file = open(self.data_path, "r")
                    data = json.loads(file.read())
                    file.close()
                    if typed in data:
                        self.username = typed
                        display.message(
                            f"welcome {typed}", 1.5, format["fore"]["green"])
                        code = 1
                    else:
                        display.message(
                            f"username '{typed}' not found", 2.5, format["fore"]["red"])
                        code = 5
                    break
                case "S":
                    self.pressed_key = None
                    code = 6
                    break
                case "Q":
                    self.pressed_key = None
                    code = 0
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 10:
                        typed += self.pressed_key
                        self.pressed_key = None

            sleep(self.gap)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Login")
        keyboard.remove_all_hotkeys()
        return code

    def signin(self):
        screen = display.Screen()
        win = display.Window(size=[18, 6])
        win.set_header(title="Sign-up")
        win.set_border()

        keyboard.add_hotkey("enter", self.press_key, args=["enter"])
        keyboard.add_hotkey("backspace", self.press_key, args=["backspace"])
        keyboard.add_hotkey("shift+l", self.press_key, args=["L"])
        keyboard.add_hotkey("shift+q", self.press_key, args=["Q"])
        for i in range(97, 123):
            keyboard.add_hotkey(chr(i), self.press_key, args=[chr(i)])

        typed = ""
        while True:
            win.text = []
            win.add_text(text="username:", pos=["m", 2])
            win.add_text(text=typed+"_", pos=["m", 3])
            win.add_text(text="Login", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 6])
            win.add_text(text="L", pos=["r", 5], format=format["underlined"])
            win.add_text(text="Q", pos=["r", 6], format=format["underlined"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "enter":
                    self.pressed_key = None
                    file = open(self.data_path, "r")
                    data = json.loads(file.read())
                    file.close()
                    if typed not in data:
                        if len(typed) > 3:
                            self.username = typed
                            temp = {
                                "high-score": 0,
                                "best-level": 1,
                                "max-lines": 0,
                                "saved": None
                            }
                            data[self.username] = {
                                "classic": temp,
                                "beta": temp
                            }
                            file = open(self.data_path, "w")
                            file.write(json.dumps(data))
                            file.close()
                            display.message(
                                f"welcome {typed}", 1.5, format["fore"]["green"])
                            code = 1
                        else:
                            display.message(
                                f"username is too short", 2, format["fore"]["red"])
                            code = 6
                    else:
                        display.message(
                            f"username '{typed}' already exists", 2.5, format["fore"]["red"])
                        code = 6
                    break
                case "L":
                    self.pressed_key = None
                    code = 5
                    break
                case "Q":
                    self.pressed_key = None
                    code = 0
                    break
                case "backspace":
                    self.pressed_key = None
                    typed = typed[:-1]
                case _:
                    if self.pressed_key and len(typed) < 10:
                        typed += self.pressed_key
                        self.pressed_key = None

            sleep(self.gap)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Sign-up")
        keyboard.remove_all_hotkeys()
        return code

    def menu(self):
        screen = display.Screen()
        win = display.Window(size=[18, 9])
        win.set_header(title="Menu", format=theme[self.mode])
        win.set_border(format=theme[self.mode])

        file = open(self.data_path, "r")
        data = json.loads(file.read())
        file.close()
        saved = not not data[self.username][self.mode]["saved"]
        del data

        if saved:
            keyboard.add_hotkey("shift+l", self.press_key, args=["l"])
            f1 = format["fore"]["yellow"]
            f2 = format["underlined"]
        else:
            f1 = format["dim"]
            f2 = format["dim"]
        keyboard.add_hotkey("shift+n", self.press_key, args=["n"])
        keyboard.add_hotkey("shift+c", self.press_key, args=["c"])
        keyboard.add_hotkey("shift+o", self.press_key, args=["o"])
        keyboard.add_hotkey("shift+q", self.press_key, args=["q"])
        while True:
            win.text = []
            # if saved:
            win.add_text(text="Load Game", pos=["l", 3], format=f1)
            win.add_text(text="L", pos=["r", 3], format=f2)
            win.add_text(text="New Game", pos=["l", 2])
            win.add_text(text="Change Mode", pos=["l", 5])
            win.add_text(text=f"({self.mode})", pos=[
                "m", 6], format=theme[self.mode])
            win.add_text(text="Logout", pos=["l", 8])
            win.add_text(text="Quit", pos=["l", 9])
            win.add_text(text="N", pos=["r", 2], format=format["underlined"])
            win.add_text(text="C", pos=["r", 5], format=format["underlined"])
            win.add_text(text="O", pos=["r", 8], format=format["underlined"])
            win.add_text(text="Q", pos=["r", 9], format=format["underlined"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "l":
                    self.pressed_key = None
                    code = 3
                    break
                case "n":
                    self.pressed_key = None
                    code = 2
                    break
                case "c":
                    self.pressed_key = None
                    self.mode = "beta" if self.mode == "classic" else "classic"
                    file = open(self.data_path, "r")
                    data = json.loads(file.read())
                    self.high_score = data[self.username][self.mode]["high-score"]
                    self.max_lines = data[self.username][self.mode]["max-lines"]
                    self.best_level = data[self.username][self.mode]["best-level"]
                    code = 1
                    break
                case "o":
                    self.pressed_key = None
                    code = 5
                    self.username = None
                    break
                case "q":
                    self.pressed_key = None
                    code = 0
                    break
            sleep(self.gap)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Menu", format=theme[self.mode])
        keyboard.remove_all_hotkeys()
        return code

    def level_up(self):
        limit = 10 * int(2 ** self.level)
        if self.experiment >= limit:
            self.level += 1
            self.experiment -= limit
            self.best_level = max(self.level, self.best_level)
            return self.experiment / (5 * int(2 ** self.level))
        else:
            return self.experiment / limit

    def calculate_score(self):
        if not self.multiline:
            self.combo = 0
            return
        self.combo += 1
        if self.level == 1:
            self.score += self.multiline * self.combo
            self.experiment += self.multiline * self.combo
        else:
            self.score += int(self.level ** self.multiline) * self.combo
            self.experiment += int(self.level ** self.multiline) * self.combo

        self.high_score = max(self.score, self.high_score)
        self.max_lines = max(self.lines, self.max_lines)
        self.multiline = 0
        return

    def pause(self):
        screen = display.Screen()
        win = display.Window(size=[18, 6])
        win.set_header(title="Paused", format=theme[self.mode])
        win.set_border(format=theme[self.mode])

        keyboard.add_hotkey("shift+r", self.press_key, args=["r"])
        keyboard.add_hotkey("shift+n", self.press_key, args=["n"])
        keyboard.add_hotkey("shift+q", self.press_key, args=["q"])
        keyboard.add_hotkey("shift+m", self.press_key, args=["m"])

        self.save_game()

        while True:
            win.text = []
            win.add_text(text="Resume", pos=["l", 2])
            win.add_text(text="New Game", pos=["l", 3])
            win.add_text(text="Back to Menu", pos=["l", 5])
            win.add_text(text="Quit", pos=["l", 6])
            win.add_text(text="R", pos=["r", 2], format=format["underlined"])
            win.add_text(text="N", pos=["r", 3], format=format["underlined"])
            win.add_text(text="M", pos=["r", 5], format=format["underlined"])
            win.add_text(text="Q", pos=["r", 6], format=format["underlined"])
            screen.add_window(win)
            screen.show()
            match self.pressed_key:
                case "r":
                    self.pressed_key = None
                    code = 3
                    break
                case "n":
                    self.pressed_key = None
                    code = 2
                    break
                case "m":
                    self.pressed_key = None
                    code = 1
                    break
                case "q":
                    self.pressed_key = None
                    code = 0
                    break
            sleep(self.gap)
            screen.clear()
            win.set_pos(("m", "m"))
            win.set_header(title="Paused", format=theme[self.mode])
        keyboard.remove_all_hotkeys()

        return code

    def press_key(self, key):
        self.pressed_key = key
        if key == "enter":
            self.n += 1
        return

    def save_game(self, remove=False):
        file = open(self.data_path, "r")
        data = json.loads(file.read())
        h_s = data[self.username][self.mode]["high-score"]
        m_l = data[self.username][self.mode]["max-lines"]
        b_l = data[self.username][self.mode]["best-level"]
        file.close()
        file = open(self.data_path, "w")
        data[self.username][self.mode] = {
            "high-score": max(self.high_score, h_s),
            "best-level": max(self.best_level, b_l),
            "max-lines": max(self.max_lines, m_l),
            "saved": None
        }
        if not remove:
            data[self.username][self.mode]["saved"] = {
                "score": self.score,
                "level": self.level,
                "experiment": self.experiment,
                "combo": self.combo,
                "lines": self.lines,
                "fixed-blocks": self.main_win.fixed_blocks,
                "shape-pos": self.main_win.shape.pos,
                "shape-blocks": self.main_win.shape.blocks,
                "shape-color": self.main_win.shape.color,
                "next-shape-name": self.next_win.shape.name,
                "next-shape-color": self.next_win.shape.color,
                "matrix": self.main_win.matrix
            }
        file.write(json.dumps(data))
        file.close()
        return

    def leaders(self):
        file = open(self.data_path, "r")
        data = json.loads(file.read())
        all = [(user, data[user][self.mode]["high-score"]) for user in data]
        all.sort(key=lambda a: a[1])
        top = all[-4:]
        if (self.username, self.high_score) not in top:
            top[0] = (self.username, self.high_score)
        return top[::-1]

    def load_game(self):
        file = open(self.data_path, "r")
        data = json.loads(file.read())
        file.close()

        self.save_game(remove=True)

        game = display.Window(size=sizes[self.mode])
        game.set_shape(shape=display.Shape(), pos=("m", "u"))
        game.shape.blocks = data[self.username][self.mode]["saved"]["shape-blocks"]
        game.shape.pos = data[self.username][self.mode]["saved"]["shape-pos"]
        game.shape.color = data[self.username][self.mode]["saved"]["shape-color"]
        game.fixed_blocks = data[self.username][self.mode]["saved"]["fixed-blocks"]
        self.main_win = game

        preview = display.Window(size=[17, 6], pos=(
            game.pos[0]+game.size[0]+4, game.pos[1]))
        preview.set_shape(shape=display.Shape(
            names=(data[self.username][self.mode]["saved"]["next-shape-name"],)), pos=("m", "m"))
        preview.shape.color = data[self.username][self.mode]["saved"]["next-shape-color"]
        self.next_win = preview

        statics = display.Window(
            size=[20, 16], pos=(game.pos[0]-24, game.pos[1]))
        self.stat_win = statics

        self.high_score = data[self.username][self.mode]["high-score"]
        self.best_level = data[self.username][self.mode]["best-level"]
        self.max_lines = data[self.username][self.mode]["max-lines"]
        self.score = data[self.username][self.mode]["saved"]["score"]
        self.combo = data[self.username][self.mode]["saved"]["combo"]
        self.lines = data[self.username][self.mode]["saved"]["lines"]
        self.level = data[self.username][self.mode]["saved"]["level"]
        self.experiment = data[self.username][self.mode]["saved"]["experiment"]
        self.main_win.matrix = data[self.username][self.mode]["saved"]["matrix"]

        return self.run()

    def new_game(self):
        self.save_game(remove=True)
        file = open(self.data_path, "r")
        data = json.loads(file.read())
        file.close()

        self.high_score = data[self.username][self.mode]["high-score"]
        self.best_level = data[self.username][self.mode]["best-level"]
        self.max_lines = data[self.username][self.mode]["max-lines"]
        self.score = 0
        self.multiline = 0
        self.combo = 0
        self.lines = 0
        self.level = 1
        self.experiment = 0

        game = display.Window(size=sizes[self.mode])
        game.set_shape(shape=display.Shape(
            names=display.shape_names[self.mode]), pos=("m", "u"))
        self.main_win = game

        preview = display.Window(size=[17, 6], pos=(
            game.pos[0]+game.size[0]+4, game.pos[1]))
        preview.set_shape(shape=display.Shape(
            names=display.shape_names[self.mode]), pos=("m", "m"))
        self.next_win = preview

        statics = display.Window(
            size=[20, 16], pos=(game.pos[0]-24, game.pos[1]))
        self.stat_win = statics

        return self.run()

    def run(self):
        screen = display.Screen()

        self.main_win.set_fill(fill=" .", format=format["dim"])
        self.main_win.set_header(title="Tetris", format=theme[self.mode])
        self.main_win.set_border(format=theme[self.mode])

        top = self.leaders()
        self.stat_win.set_header(title="Statics", format=theme[self.mode])
        self.stat_win.set_border(format=theme[self.mode])
        self.stat_win.main = False

        self.next_win.set_header(title="Next", format=theme[self.mode])
        self.next_win.set_border(format=theme[self.mode])
        self.next_win.main = False

        help_win = display.Window(size=(17, 7), pos=(
            self.next_win.pos[0], self.next_win.pos[1]+self.next_win.size[1]+3))
        help_win.set_header(title="Help", format=theme[self.mode])
        help_win.set_border(format=theme[self.mode])
        help_win.main = False

        auto_move = Thread(target=self.main_win.auto_move)
        auto_move.daemon = True
        auto_move.start()

        keyboard.add_hotkey("down", self.main_win.move)
        keyboard.add_hotkey("left", self.main_win.move, args=["l"])
        keyboard.add_hotkey("right", self.main_win.move, args=["r"])
        keyboard.add_hotkey("up", self.main_win.rotate)
        keyboard.add_hotkey("space", self.main_win.drop)
        keyboard.add_hotkey("esc", self.press_key, args=["esc"])

        while True:
            if self.pressed_key == "esc":
                self.pressed_key = None
                keyboard.remove_all_hotkeys()
                return 4

            if not self.main_win.can_move():
                self.experiment += self.level
                self.main_win.fix_shape()
                while self.main_win.remove_line():
                    self.lines += 1
                    self.multiline += 1
                self.calculate_score()
                if not self.main_win.game_over():
                    self.main_win.set_shape(shape=display.Shape(
                        names=(self.next_win.shape.name,)), pos=("m", "u"))
                    self.main_win.shape.color = self.next_win.shape.color
                    self.next_win.set_shape(display.Shape(
                        names=display.shape_names[self.mode]), pos=("m", "m"))
                else:
                    break

            help_win.text = []
            self.next_win.text = []
            self.stat_win.text = []
            self.main_win.text = []

            # help_win.add_text(text="Keys for Tetris:", pos=["m", 2])
            help_win.add_text(text="↑", pos=["r", 2])
            help_win.add_text(text="Rotate", pos=["l", 2])
            help_win.add_text(text="←", pos=["r", 3])
            help_win.add_text(text="Move left", pos=["l", 3])
            help_win.add_text(text="→", pos=["r", 4])
            help_win.add_text(text="Move right", pos=["l", 4])
            help_win.add_text(text="↓", pos=["r", 5])
            help_win.add_text(text="Move down", pos=["l", 5])
            help_win.add_text(text="space", pos=["r", 6])
            help_win.add_text(text="Drop", pos=["l", 6])
            help_win.add_text(text="esc", pos=["r", 7])
            help_win.add_text(text="Pause/Exit", pos=["l", 7])
            self.stat_win.set_border(format=theme[self.mode])
            self.stat_win.add_text(text="Score", pos=["l", 2])
            self.stat_win.add_text(text=str(self.score), pos=["r", 2])
            self.stat_win.add_text(text="Lines", pos=["l", 3])
            self.stat_win.add_text(text=str(self.lines), pos=["r", 3])
            self.stat_win.add_text(text=f"Level {self.level}", pos=["m", 5])
            self.stat_win.add_text(
                text="━"*(self.stat_win.size[0]-2), pos=["l", 6])
            self.stat_win.add_text(
                text="━"*int((self.stat_win.size[0]-2)*self.level_up()), pos=["l", 6], format=format["fore"]["red"])
            self.stat_win.add_text(text="├"+"─"*self.stat_win.size[0]+"┤", pos=[
                "m", 8], format=theme[self.mode])
            self.stat_win.add_text(text="├"+"─"*self.stat_win.size[0]+"┤", pos=[
                "m", 14], format=theme[self.mode])
            self.stat_win.add_text(text="Leaderboard", pos=[
                "m", 8], format=theme[self.mode])
            self.stat_win.add_text(
                text="User", pos=["l", 9], format=format["dim"])
            self.stat_win.add_text(text="Best", pos=[
                "r", 9], format=format["dim"])
            self.stat_win.add_text(text="Best", pos=[
                "r", 9], format=format["dim"])
            self.stat_win.add_text(text="MaxLines", pos=["l", 15])
            self.stat_win.add_text(text=str(self.max_lines), pos=["r", 15])
            self.stat_win.add_text(text="BestLevel", pos=["l", 16])
            self.stat_win.add_text(text=str(self.best_level), pos=["r", 16])
            rank = 1
            for user, best in top:
                if user == self.username:
                    f = format["bold"]+format["fore"]["yellow"]
                    top[rank-1] = (user, self.high_score)
                else:
                    f = format["regular"]
                self.stat_win.add_text(
                    text=f"{rank}-{user}", pos=["l", 9+rank], format=f)
                self.stat_win.add_text(text=str(best), pos=[
                                       "r", 9+rank], format=f)
                rank += 1
            top.sort(key=lambda a: 1/(a[1]+1))
            if self.combo:
                self.main_win.add_text(text=f"combo:{self.combo}", pos=[
                                       "m", self.main_win.size[1]+1], format=format["dim"])

            screen.add_window(help_win)
            screen.add_window(self.next_win)
            screen.add_window(self.stat_win)
            screen.add_window(self.main_win)
            screen.show()
            screen.clear()

            sleep(self.gap)
            self.main_win.break_time = 2 ** (-self.level) + 0.5

            self.main_win.set_pos(pos=("m", "m"))
            self.next_win.set_pos(
                pos=(self.main_win.pos[0]+self.main_win.size[0]+4, self.main_win.pos[1]))
            self.stat_win.set_pos(
                pos=(self.main_win.pos[0]-24, self.main_win.pos[1]))
            help_win.set_pos(
                pos=(self.next_win.pos[0], self.next_win.pos[1]+self.next_win.size[1]+3))

        screen.add_window(help_win)
        screen.add_window(self.next_win)
        screen.add_window(self.stat_win)
        screen.add_window(self.main_win)
        screen.show()
        self.save_game(remove=True)
        keyboard.remove_all_hotkeys()
        sleep(5)

        return 1

    def do(self, code):
        match code:
            case 1:
                return self.menu()
            case 2:
                return self.new_game()
            case 3:
                return self.load_game()
            case 4:
                return self.pause()
            case 5:
                return self.login()
            case 6:
                return self.signin()
            case _:
                return 0
