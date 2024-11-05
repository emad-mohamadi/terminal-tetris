## Terminal Tetris


Before you run the game
- Enter directory path in `main.py` (and uncomment the line)
- Changed script must be like this
  
  ```Python
  def main():
      from tetris.play import Game
      from tetris.display import welcome, format, Screen
      from keyboard import press

      welcome()
      tetris = Game()
      #  Changed line:  #
      tetris.data_path = "C:/Users/Emad" + "/data.txt"
      # # # # # # # # # #
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

- Then open the project directory in terminal and use this command:
  ```console
  pip install . # Make sure pip is already installed.
  ```
- Now you can play the game anywhere in terminal with `tetris` command:
  ```console
  tetris
  ```

or
- Open your directory in terminal
- Run the game:

      python tetris.py
----

Requirements:
- Python `keyboard` package must be installed
- If not, you can install it using `pip`:

      pip install keyboard
----

Enjoy it 🍵
----

~ emad-mohamadi & danial-fazel\
The Biotet team

----
Contact:\
semadmhmdi@gmail.com \
t.me/emad_mohammadi

----
       
