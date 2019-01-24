# Minesweeper
An implementation of Minesweeper game.
# Game
Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular
board containing hidden "mines" or bombs without detonating any of them, with help from clues about
the number of neighboring mines in each field. The game originates from the 1960s, and has been
written for many computing platforms in use today.
The player is initially presented with a grid of undifferentiated squares. Some randomly selected
squares, unknown to the player, are designated to contain mines. Typically, the size of the grid and
the number of mines are set in advance by the user, either by entering the numbers or selecting from
defined skill levels, depending on the implementations.The game is played by revealing squares of the grid by clicking or otherwise indicating each square. If a square containing a mine is revealed, the player loses the game. If no mine is revealed,
a digit is instead displayed in the square, indicating how many adjacent squares contain mines; if no
mines are adjacent, the square becomes blank, and all adjacent squares will be recursively revealed.
The player uses this information to deduce the contents of other squares, and may either safely
reveal each square or mark the square as containing a mine. The game is won when all mine-free
squares are revealed, because all mines have been located.

# Rules of the Game

The rules of Minesweeper are fairly simple:

* You are presented with a board of squares. Some squares contain mines (bombs), others don’t.
* If you click on a square containing a bomb, you lose. If you manage to click all the squares
(without clicking on any bombs) you win.
* Clicking a square which doesn’t have a bomb reveals the number of neighbouring squares
containing bombs. Use this information plus some guess work to avoid the bombs.
* To open a square, point at the square and left click on it.
* To mark a square you think is a bomb, point and right-click.
* If you mark a bomb incorrectly, you will have to correct the mistake before you can win. Incorrect
bomb marking doesn’t kill you, but it can lead to mistakes which do.
* You don’t have to mark all the bombs to win; you just need to open all non-bomb squares.

# Implementation

The game is implemented in Python language, and the GUI framework chosen is PyQt5. The implementation is based on the MVC pattern (Model view controller).

# Model

The Model class provides the basis of 'Minesweeper'.This class allows to inizialize and manage the board.In this class the grid is created, the mines are assigned and the cell values ​​are calculated according to the position of the bombs.
Attributes:

* width=number of column of grid
* height=number of rows of grid
* num_mines=number of mines
* mine=mines value
* grid=represent the grid of the game
* grid_coords=represent the coordinates of the grid
* cells_revealed=represent the revealed cells
* cells_flagged=epresent the flagged cells
* game_state=represent the game state

# Controller

This class provides the methods to allow the dialog between view and model.This class implements the rules of detection and management of the grid, reveals the decisions, detects the state of the game and manages the user's view through the model grid. It also manages the reset of the game and the loading of a saved model.
Attributes:

* width=number of column of grid
* height=number of rows of grid
* num_mines=number of mines
* difficulty=represent the game difficulty
* model=represent the model
* view=represent the view

# View

This class provides to display the current state of game and to setting the application GUI. The interaction with users is manage by this class. The section of GUI code is was created with use of Qt Designer.This class allows the display of the game and the current status together with the time elapsed and the best result.It also provides the functions to save the model and to read the best results obtained up to that moment.
Attributes:

* width=number of column of grid
* height=number of rows of grid
* num_mines=number of mines
* n_secs_start=number of second that start the timer
* n_secs=number of second runtime
* controller=reference to controller(MVC)
* _timer=timer used to manage the time

# Features

   * Play
   * Restart
   * Time Elapsed
   * History Best Result
   * Save/Not save Game
   * Load Game
   * Choose Difficulty

# Requirements
    
| Software  | Version | Required |
| ------------- | ------------- | ------------- |
| Python  | >= 3.5  | Yes
| Pyqt5  | >= 5.1  | Yes
| itertools  |
| functools  |
| time  |
| random  |

# How to play?
The game can be launched from the minesweeper.py script:

      $ python3 minesweeper.py
To play you will have to follow the rules written above. The game starts with easy mode but with the menu on the top left you can choose the difficulty you prefer and then start playing. In the top menu by clicking on exit you can decide whether to close the application by saving the data and then being able to restart the game in the state in which it was left or not, otherwise clicking on closing the window does not save the data.During the game it will be possible to start from scratch by clicking on the central icon with the smile.The state of the game is represented by the smile, if it smiles it means that the game is in progress, if it cries it means that you have lost, finally if it says you win ... you have won!
In the interface are shown the playing time and the best result obtained in the difficulty you are playing up to that point.
Seen the development in linux environment I thought to use the top menu to streamline the application without putting a new menu within the interface. This is because the use of the top menu in the linux environment is expanded to any application.

# Game View
![Game User View](https://github.com/WolBig/MinesWeeper/blob/master/icons/shotGame.png)
