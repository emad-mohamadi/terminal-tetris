from play import Game
from display import welcome, format, Screen
from keyboard import press

welcome()
tetris = Game()
# tetris.data_path = <your-directory-path> + "/data.txt"
code = 5
while code:
    code = tetris.do(code)

press("enter")
for _ in range(tetris.n+1):
    input()
scr = Screen()
scr.clear()
scr.show()
print(end=format["from-beginning"])
