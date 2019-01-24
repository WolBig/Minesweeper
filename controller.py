import get_adjacent
from model import Model
import viewPyqt5


class Controller:

    """

    This class describes the methods and characteristics that allow to manage model and view.
    Allows to manage all the operations of the game on the model and then bring them back to the view, keeping the
    information related to the game on the model.

    Attributes:
        width               number of column of grid
        height              number of rows of grid
        num_mines           number of mines
        difficulty          represent the game difficulty
        model               represent the model
        view                represent the view

    """

    def __init__(self, width, height, num_mines, difficulty):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.difficulty = difficulty
        self.model = Model(self.width, self.height, self.num_mines)
        self.view = viewPyqt5.View(self.width, self.height, self.num_mines, self)

    def load_all(self, grid, reveal, flag, n_secs):
        """method that load saved games"""
        self.reset_mod(self.difficulty)
        self.model.grid = []
        for i in grid:
            self.model.grid.append(eval(i))
        flag = eval(flag)
        for fla in flag:
            self.model.set_flag_cells(fla)
            self.view.flag_cell(fla)
            self.update_flagged_cell_saved(fla)
        reveal = eval(reveal)
        for rev in reveal:
            self.model.set_revealed_cells(rev)
            self.view.reveal_cell(rev, self.model.get_cell_value(rev))
        self.view.n_secs_start = eval(n_secs)

    def reset(self):
        """method that reset the game,model and view"""
        self.model = Model(self.width, self.height, self.num_mines)
        self.view.newgame()

    def reset_mod(self, diff):
        """method that change the difficulty"""
        self.__init__(*{
            'E': (10, 10, 20, diff),
            'M': (15, 15, 40, diff),
            'H': (20, 20, 60, diff)
        }[diff[0]])
        self.reset()
        if self.difficulty == 'E':
            self.view.setFixedSize(500, 500)
        if self.difficulty == 'M':
            self.view.setFixedSize(600, 600)
        if self.difficulty == 'H':
            self.view.setFixedSize(800, 800)
        self.view.show()

    def reveal_decision(self, index):
        """method that reveal the decision in model and view"""
        cell_value = self.model.get_cell_value(index)
        if index in self.model.get_cells_flagged():
            return None

        if cell_value in range(1, 9):
            self.reveal_cell(index, cell_value)
        elif (
                cell_value == self.model.mine_value()
                and self.model.game_state != "win"
        ):
            self.loss()
        else:
            self.reveal_zeroes(index)

        cells_unrevealed = self.height * self.width - len(self.model.get_cells_revealed())
        if cells_unrevealed == self.num_mines and self.model.game_state != "loss":
            self.win()

    def reveal_cell(self, index, value):
        """method that add revealed cells in model and reveal cell in view"""
        if index not in self.model.get_cells_flagged():
            self.model.get_cells_revealed().add(index)
            self.view.reveal_cell(index, value)

    def reveal_zeroes(self, index):
        """method that add zeroes cells in model and reveal cell in view"""

        self.reveal_cell(index, 0)

        for coords in get_adjacent.get_adjacent(index):
            if (
                    0 <= coords[0] <= self.width - 1
                    and self.height - 1 >= coords[1] >= 0 == self.model.get_cell_value(coords)
                    and coords not in self.model.get_cells_revealed()
            ):
                self.reveal_zeroes(coords)
            elif (
                    0 <= coords[0] <= self.width - 1
                    and self.height - 1 >= coords[1] >= 0 != self.model.get_cell_value(coords)
                    and coords not in self.model.get_cells_revealed()
            ):
                cell_value = self.model.get_cell_value(coords)
                self.reveal_cell(coords, cell_value)

    def update_flagged_cell(self, index):
        """method that update flagged cells in model and view"""
        if (
                index not in self.model.get_cells_revealed()
                and index not in self.model.get_cells_flagged()
        ):
            if self.view.flags < self.num_mines:
                self.model.get_cells_flagged().add(index)
                self.view.flag_cell(index)
                self.view.flags += 1
                self.view.flagCnt.setText(str(self.view.flags) + "/" + str(self.num_mines))
        elif (
                index not in self.model.get_cells_revealed()
                and index in self.model.get_cells_flagged()
        ):
            self.model.get_cells_flagged().remove(index)
            self.view.unflag_cell(index)
            self.view.flags -= 1
            self.view.flagCnt.setText(str(self.view.flags) + "/" + str(self.num_mines))

    def update_flagged_cell_saved(self, index):
        """method that update flagged cells saved in model and view"""
        if self.view.flags < self.num_mines:
            self.model.get_cells_flagged().add(index)
            self.view.flag_cell(index)
            self.view.flags += 1
            self.view.flagCnt.setText(str(self.view.flags) + "/" + str(self.num_mines))

    def win(self):
        """method that controll the win"""

        self.model.change_game_state("win")
        self.view.display_win()

        for row in range(self.height):
            for col in range(self.width):
                cell_value = self.model.get_cell_value((col, row))
                self.view.reveal_cell((col, row), cell_value)

    def loss(self):
        """method that controll the loss"""

        self.model.change_game_state("loss")
        self.view.display_loss()

        for row in range(self.height):
            for col in range(self.width):
                cell_value = self.model.get_cell_value((col, row))
                self.view.reveal_cell((col, row), cell_value)
