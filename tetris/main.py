def main():
    from tetris.play import Game
    from tetris.display import welcome, format, Screen
    from keyboard import press
    from os import path

    welcome()

    tetris = Game()
    tetris.data_path = path.dirname(path.abspath(__file__)) + r"\data.txt"

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


if __name__ == '__main__':
    main()
