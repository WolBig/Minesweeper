import os
import time
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def read_diff(diff, result):
    """method that read and control the time results"""
    if os.path.exists('best_winner.txt'):
        win = open('best_winner.txt', 'r')
        win_res = []
        for i in win.readlines():
            win_res.append(i)
        win = open('best_winner.txt', 'w')
        if diff == 'E' and int(win_res[0]) > result:
            win_res[0] = str(result) + '\n'
        if diff == 'M' and int(win_res[1]) > result:
            win_res[1] = str(result) + '\n'
        if diff == 'H' and int(win_res[2]) > result:
            win_res[2] = str(result) + '\n'

        for i in win_res:
            win.write(i)


def clear_save():
    """method that clear saved file"""
    if os.path.exists('saved.txt'):
        win = open('saved.txt', 'r+')
        win.truncate(0)


class View(QMainWindow):

    """

        This class provides to display the current state of game,the time and the best result.
        The interaction with users is manage by this class.
        The section of GUI code is was created with use of Qt Designer.

        Attributes:
            width               number of column of grid
            height              number of rows of grid
            num_mines           number of mines
            n_secs_start        number of second that start the timer
            n_secs              number of second runtime
            controller          reference to controller(MVC)
            _timer              timer used to manage the time

    """

    def __init__(self, width, height, num_mines, controller, parent=None):
        super(View, self).__init__(parent)
        self.n_secs_start = 0
        self.n_secs = 0
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.controller = controller
        self.setWindowTitle('Minesweeper')
        self.setWindowIcon(QIcon('minesweeper.ico'))
        self.setStyleSheet("QMenuBar { background-color: #dddddd; }")
        self.setFixedSize(500, 500)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.fileMenu = QMenu("&Difficulty", self)
        self.ExitMenu = QMenu("&Exit", self)
        self.ExitMenu.addAction(QAction("&Save", self, triggered=self.save_progress))
        self.ExitMenu.addAction(QAction("&NotSave", self, triggered=self.not_save_progress))
        self.fileMenu.addAction(
            QAction("&Easy", self.centralwidget, triggered=partial(self.controller.reset_mod, 'E')))
        self.fileMenu.addAction(
            QAction("&Medium", self.centralwidget, triggered=partial(self.controller.reset_mod, 'M')))
        self.fileMenu.addAction(
            QAction("&Hard", self.centralwidget, triggered=partial(self.controller.reset_mod, 'H')))
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.ExitMenu)

        self.vLayout = QVBoxLayout(self.centralwidget)
        self.hLayout = QHBoxLayout()

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)

        self.hLayout.addStretch()
        self.hLayout.addLayout(self.gridLayout)
        self.hLayout.addStretch()

        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addStretch()

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch()

        self.timeLabel = QLabel(str(0) + str(0) + str(0) + ' Sec')
        self.timeLabel.setStyleSheet('QLabel {font:  16px; color: #b6135d}')
        self.flagLabel = QLabel("Mines: ")
        self.flagLabel.setStyleSheet('QLabel {font:  16px; color: black}')
        self.flagCnt = QLabel()
        self.flags = 0
        self.flagCnt.setText("0/" + str(self.num_mines))
        self.flagCnt.setStyleSheet('QLabel {font:  16px; color: black}')
        self.clearBtn = QPushButton()
        self.clearBtn.setFixedSize(50, 50)
        icon = QPixmap('icons/happy.png')
        self.clearBtn.setIcon(QIcon(icon))
        self.clearBtn.setIconSize(QSize(50, 50))
        self.clearBtn.setFlat(True)
        self.clearBtn.clicked.connect(self.reset_view)

        self.resultsLabel = QLabel('Best : ' + str(self.read_best()))
        self.resultsLabel.setStyleSheet('QLabel {font:  16px; color: #b6135d}')

        self.buttonLayout.addWidget(self.timeLabel)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.clearBtn)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.flagLabel)
        self.buttonLayout.addWidget(self.flagCnt)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.resultsLabel)
        self.buttonLayout.addStretch()

        self.gridLayout.addLayout(self.buttonLayout, 0, 0, 1, width)
        self._timer = QTimer()
        self.newgame()

    def newgame(self):
        """method that inizialize the button grid"""
        self.buttons = []
        self.firstclick = 1
        for i in range(self.width):
            l = []
            for j in range(self.width):
                self.botton = QPushButton()
                self.botton.setFixedSize(35, 35)
                l.append(self.botton)
                self.gridLayout.addWidget(self.botton, i + 1, j)
                self.botton.setStatusTip(str(i) + str(j))
                self.botton.setObjectName(str(i) + ',' + str(j))
                self.botton.row = i
                self.botton.col = j
                self.botton.isMine = False
                self.botton.mineCount = -1
                self.botton.setFlat(False)
                self.botton.setEnabled(True)
                self.botton.installEventFilter(self)
            self.buttons.append(l)
        self.n_secs_start = 0
        self.n_secs = 0
        return

    def save_progress(self):
        """method that saved the game"""
        if not os.path.exists('saved.txt'):
            os.mknod('saved.txt')
        win = open('saved.txt', 'w')
        win.write(str(self.controller.difficulty) + '\n')
        for i in self.controller.model.grid:
            win.write(str(i) + '\n')
        win.write(str(self.controller.model.get_cells_revealed()) + '\n')
        win.write(str(self.controller.model.get_cells_flagged()) + '\n')
        win.write(str(self.n_secs))
        win.close()
        self.close()

    def not_save_progress(self):
        """method that close but don't save the game"""
        clear_save()
        self.close()

    def update_timer(self):
        """method that update the timer"""
        self.n_secs = self.n_secs_start + int(time.time()) - self._timer_start_nsecs
        self.timeLabel.setText(("%03d" % self.n_secs) + ' Sec')

    def eventFilter(self, obj, event):
        """method that filter the right and left mouse press"""
        word = str.split(obj.objectName(), ',')
        y = word[0]
        x = word[1]
        if event.type() == QEvent.MouseButtonPress:
            if self.firstclick == 1:
                self._timer.timeout.connect(self.update_timer)
                self._timer_start_nsecs = int(time.time())
                self._timer.start(1000)  # 1 second timer
                self.firstclick -= 1
            if event.button() == Qt.LeftButton:
                self.controller.reveal_decision((int(x), int(y)))
            elif event.button() == Qt.RightButton:
                self.controller.update_flagged_cell((int(x), int(y)))
        return QObject.event(obj, event)

    def reset_view(self):
        """method that reset the view"""
        icon = QPixmap('icons/happy.png')
        self.clearBtn.setIcon(QIcon(icon))
        self.clearBtn.setIconSize(QSize(50, 50))
        self.clearBtn.setFlat(True)
        self.flags = 0
        self.n_secs = 0
        self.flagCnt.setText("0/" + str(self.num_mines))
        self._timer.stop()
        self.timeLabel.setText(str(0) + str(0) + str(0) + ' Sec')
        self.controller.reset()
        clear_save()

    def reveal_cell(self, index, value):
        """method that reveal the cell in view"""
        x, y = index
        if value == -1:
            icon = QPixmap('icons/grenade.png')
            self.buttons[y][x].setIcon(QIcon(icon))
            self.buttons[y][x].setIconSize(QSize(20, 20))
        else:
            self.buttons[y][x].setText(str(value))

    def flag_cell(self, index):
        """method that flag the cell in view"""
        x, y = index
        icon = QPixmap('icons/flag.png')
        self.buttons[y][x].setIcon(QIcon(icon))
        self.buttons[y][x].setIconSize(QSize(20, 20))

    def unflag_cell(self, index):
        """method that unflag the cell in view"""
        x, y = index
        self.buttons[y][x].setIcon(QIcon())

    def display_loss(self):
        """method that display loss"""
        icon = QPixmap('icons/sad.png')
        self.clearBtn.setIcon(QIcon(icon))
        self.clearBtn.setIconSize(QSize(50, 50))
        self.clearBtn.setFlat(True)
        clear_save()

    def display_win(self):
        """method that display win"""
        icon = QPixmap('icons/win.png')
        self.clearBtn.setIcon(QIcon(icon))
        self.clearBtn.setIconSize(QSize(50, 50))
        self.clearBtn.setFlat(True)
        self._timer.stop()
        read_diff(self.controller.difficulty, self.n_secs)
        self.resultsLabel.setText('Best : ' + str(self.read_best()))
        clear_save()

    def read_best(self):
        """method that read the best results"""
        if os.path.exists('best_winner.txt'):
            win = open('best_winner.txt', 'r')
            win_res = []
            for i in win.readlines():
                win_res.append(i)
            if self.controller.difficulty == 'E':
                return int(win_res[0])
            if self.controller.difficulty == 'M':
                return int(win_res[1])
            if self.controller.difficulty == 'H':
                return int(win_res[2])
