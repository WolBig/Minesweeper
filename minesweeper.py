import sys
import os
from PyQt5.QtWidgets import QApplication

import controller


def init_game():
    if os.path.exists('saved.txt'):
        win = open('saved.txt', 'r')
        win_res = []
        for i in win.readlines():
            diff = i.split('\n')
            win_res.append(diff[0])
        if not win_res:
            cont = controller.Controller(10, 10, 20, 'E')
        else:
            difficulty = win_res[0]
            cont = controller.Controller(*{
                'E': (10, 10, 20, difficulty),
                'M': (15, 15, 40, difficulty),
                'H': (20, 20, 60, difficulty)
            }[difficulty[0]])
            if win_res[0] == 'E':
                cont.load_all(win_res[1:11], win_res[11], win_res[12], win_res[13])
            if win_res[0] == 'M':
                cont.load_all(win_res[1:16], win_res[16], win_res[17], win_res[18])
            if win_res[0] == 'H':
                cont.load_all(win_res[1:21], win_res[21], win_res[22], win_res[23])
    else:
        cont = controller.Controller(10, 10, 20, 'E')
    cont.view.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_game()
    sys.exit(app.exec_())
