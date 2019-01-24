import itertools
from random import sample

import get_adjacent


class Model:
    """

    This class describes the methods and characteristics of the basic model of the game.
    The basic functions for initializing the game are implemented and allows the controller to manage the view based on
    this model.

    Attributes:
        width               number of column of grid
        height              number of rows of grid
        num_mines           number of mines
        mine                mines' value
        grid                represent the grid of the game
        grid_coords         represent the coordinates of the grid
        cells_revealed      represent the revealed cells
        cells_flagged       represent the flagged cells
        game_state          represent the game state

    """

    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.mine = -1
        self.grid = self.create_grid()
        self.add_mines()
        self.grid_coords = self.grid_coords()
        self.set_adjacent_mine_count()
        self.cells_revealed = set()
        self.cells_flagged = set()
        self._game_state = None

    def mine_value(self):
        return self.mine

    def create_grid(self):
        """method that create a grid of zeroes"""
        return [[0] * self.width for _ in range(self.height)]

    def add_mines(self):
        """method that assign randomly mines to the grid"""
        for x, y in sample(list(itertools.product(range(self.width), range(self.height))), self.num_mines):
            self.grid[y][x] = self.mine

    def grid_coords(self):
        """method that return the grid position"""
        return [(x, y) for y in range(self.height) for x in range(self.width)]

    def is_mine(self, coords):
        """method that identify mine in a cell"""
        try:
            if coords[0] >= 0 and coords[1] >= 0:
                return self.grid[coords[1]][coords[0]] == self.mine
            else:
                return False
        except IndexError:
            return False

    def set_adjacent_mine_count(self):
        """method that calculate the adjacent mine of a cell"""
        for position in self.grid_coords:
            x, y = position
            if self.grid[y][x] >= 0:
                grid_value = sum(map(self.is_mine, get_adjacent.get_adjacent(position)))
                self.grid[y][x] = grid_value

    def get_cell_value(self, index):
        """method that return a cell value"""
        x, y = index
        return self.grid[y][x]

    def get_cells_flagged(self):
        """method that get flag cells"""
        return self.cells_flagged

    def get_cells_revealed(self):
        """method that get revealed cells"""
        return self.cells_revealed

    def set_revealed_cells(self, cells):
        """method that set revealed cells"""
        self.cells_revealed.add(cells)

    def set_flag_cells(self, cells):
        """method that set flag cells"""
        self.cells_flagged.add(cells)

    @property
    def game_state(self):
        """method that return the game state"""
        return self._game_state

    def change_game_state(self, state):
        """method that change the game state"""
        self._game_state = state
