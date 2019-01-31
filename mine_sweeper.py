#coding: utf-8
import random
import sys
sys.setrecursionlimit(100000)
print u'最大允许递归次数：', sys.getrecursionlimit()

class Tile:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.mine = []
        self.mine_counter = 0
        self.hint_counter = 0
        self.counter = 0
        self.game_state = u'NONE'#END, RUNNING, NONE
        self.game_result = u'NONE'#WIN, LOSE, NONE
        self.empty_counter = 0
        self.mark_counter = 0

        self.test = ()
      
    def initMine(self):  
        self.mine_counter = 0
        self.tile = [[{u'tile_type': u'', u'tile_state': 0, u'hint_num': 0, u'tile_coords': (0, 0)} \
                for y in range(self.Y)]for x in range(self.X)]
        for j in range(self.Y):
            for i in range(self.X):
                if random.randint(0, 6) == 0:
                    self.tile[i][j] = {u'tile_type': u'Mine', u'tile_state': u'COVER' , u'hint_num': 0, u'tile_coords': (i, j)}
                    self.mine_counter += 1
                else:
                    self.tile[i][j] = {u'tile_type': u'Empty', u'tile_state': u'COVER' , u'hint_num': 0, u'tile_coords': (i, j)}
        self.mine_num = self.mine_counter
        self.empty_num = self.X * self.Y - self.mine_num
        print u'雷数量为：', self.mine_num
        self.game_state = u'RUNNING' #END || RUNNING
        self.game_result = u'NONE' #WIN || LOSE

    def initHint(self):
        for x in range(self.X):
            for y in range(self.Y):
                if self.tile[x][y][u'tile_type'] == u'Empty':
                    self.hint_counter = 0
                    if x > 0 and x < self.X - 1 and y > 0 and y < self.Y - 1:
                        if self.tile[x-1][y-1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':
                            self.hint_counter += 1
                        if self.tile[x-1][y+1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1

                        if self.tile[x][y-1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1

                        if self.tile[x+1][y-1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':
                            self.hint_counter += 1
                        if self.tile[x+1][y+1][u'tile_type'] == u'Mine':
                            self.hint_counter += 1

                    if x == 0 and  y == 0:#left top
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':#5
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':#7
                            self.hint_counter += 1
                        if self.tile[x+1][y+1][u'tile_type'] == u'Mine':#8
                            self.hint_counter += 1

                    if x == 0 and  y == self.Y - 1:#right top
                        if self.tile[x][y-1][u'tile_type'] == u'Mine':#4
                            self.hint_counter += 1
                        if self.tile[x+1][y-1][u'tile_type'] == u'Mine':#6
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':#7
                            self.hint_counter += 1

                    if x == self.X - 1 and  y == 0:#left bottom
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':#2
                            self.hint_counter += 1
                        if self.tile[x-1][y+1][u'tile_type'] == u'Mine':#3
                            self.hint_counter += 1
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':#5
                            self.hint_counter += 1

                    if x == self.X - 1 and  y == self.Y - 1:#right bottom
                        if self.tile[x-1][y-1][u'tile_type'] == u'Mine':#1
                            self.hint_counter += 1
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':#2
                            self.hint_counter += 1
                        if self.tile[x][y-1][u'tile_type'] == u'Mine':#4
                            self.hint_counter += 1

                    if x == 0 and  y > 0 and  y < self.Y - 1:#top
                        if self.tile[x][y-1][u'tile_type'] == u'Mine':#4
                            self.hint_counter += 1
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':#5
                            self.hint_counter += 1
                        if self.tile[x+1][y-1][u'tile_type'] == u'Mine':#6
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':#7
                            self.hint_counter += 1
                        if self.tile[x+1][y+1][u'tile_type'] == u'Mine':#8
                            self.hint_counter += 1

                    if x > 0 and x < self.X - 1 and  y == 0:#left
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':#2
                            self.hint_counter += 1
                        if self.tile[x-1][y+1][u'tile_type'] == u'Mine':#3
                            self.hint_counter += 1
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':#5
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':#7
                            self.hint_counter += 1
                        if self.tile[x+1][y+1][u'tile_type'] == u'Mine':#8
                            self.hint_counter += 1

                    if x > 0 and x < self.X - 1 and  y == self.Y - 1:#right
                        if self.tile[x-1][y-1][u'tile_type'] == u'Mine':#1
                            self.hint_counter += 1
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':#2
                            self.hint_counter += 1
                        if self.tile[x][y-1][u'tile_type'] == u'Mine':#4
                            self.hint_counter += 1
                        if self.tile[x+1][y-1][u'tile_type'] == u'Mine':#6
                            self.hint_counter += 1
                        if self.tile[x+1][y][u'tile_type'] == u'Mine':#7
                            self.hint_counter += 1

                    if x == self.X - 1 and  y > 0 and y < self.Y - 1:#bottom
                        if self.tile[x-1][y-1][u'tile_type'] == u'Mine':#1
                            self.hint_counter += 1
                        if self.tile[x-1][y][u'tile_type'] == u'Mine':#2
                            self.hint_counter += 1
                        if self.tile[x-1][y+1][u'tile_type'] == u'Mine':#3
                            self.hint_counter += 1
                        if self.tile[x][y-1][u'tile_type'] == u'Mine':#4
                            self.hint_counter += 1
                        if self.tile[x][y+1][u'tile_type'] == u'Mine':#5
                            self.hint_counter += 1

                    self.tile[x][y][u'hint_num'] = self.hint_counter

        self.displayTile()

    def showEmpty(self, x, y):
#-------
#|1|2|3|
#|4|T|5|
#|6|7|8|
#-------
        if x > 0 and x < self.X - 1 and y > 0 and y < self.Y - 1:
            if self.tile[x-1][y-1][u'tile_type'] == u'Empty' and self.tile[x-1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y-1][u'hint_num'] == 0:#1
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y-1)
                if self.tile[x-1][y-1][u'hint_num'] > 0:
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y+1][u'tile_type'] == u'Empty' and self.tile[x-1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y+1][u'hint_num'] == 0:#3
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y+1)
                if self.tile[x-1][y+1][u'hint_num'] > 0:
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y-1][u'tile_type'] == u'Empty' and self.tile[x+1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y-1][u'hint_num'] == 0:#6
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y-1)
                if self.tile[x+1][y-1][u'hint_num'] > 0:
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y+1][u'tile_type'] == u'Empty' and self.tile[x+1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y+1][u'hint_num'] == 0:#8
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y+1)
                if self.tile[x+1][y+1][u'hint_num'] > 0:
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'

        if x == 0 and y > 0 and y < self.Y - 1:#top
            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y-1][u'tile_type'] == u'Empty' and self.tile[x+1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y-1][u'hint_num'] == 0:#6
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y-1)
                if self.tile[x+1][y-1][u'hint_num'] > 0:
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y+1][u'tile_type'] == u'Empty' and self.tile[x+1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y+1][u'hint_num'] == 0:#8
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y+1)
                if self.tile[x+1][y+1][u'hint_num'] > 0:
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'

        if x > 0 and x < self.X - 1 and y == 0:#left
            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y+1][u'tile_type'] == u'Empty' and self.tile[x-1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y+1][u'hint_num'] == 0:#3
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y+1)
                if self.tile[x-1][y+1][u'hint_num'] > 0:
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y+1][u'tile_type'] == u'Empty' and self.tile[x+1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y+1][u'hint_num'] == 0:#8
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y+1)
                if self.tile[x+1][y+1][u'hint_num'] > 0:
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'

        if x > 0 and x < self.X - 1 and y == self.Y - 1:#right
            if self.tile[x-1][y-1][u'tile_type'] == u'Empty' and self.tile[x-1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y-1][u'hint_num'] == 0:#1
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y-1)
                if self.tile[x-1][y-1][u'hint_num'] > 0:
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y-1][u'tile_type'] == u'Empty' and self.tile[x+1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y-1][u'hint_num'] == 0:#6
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y-1)
                if self.tile[x+1][y-1][u'hint_num'] > 0:
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

        if x == self.X - 1 and y > 0 and y < self.Y - 1:#bottom
            if self.tile[x-1][y-1][u'tile_type'] == u'Empty' and self.tile[x-1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y-1][u'hint_num'] == 0:#1
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y-1)
                if self.tile[x-1][y-1][u'hint_num'] > 0:
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y+1][u'tile_type'] == u'Empty' and self.tile[x-1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y+1][u'hint_num'] == 0:#3
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y+1)
                if self.tile[x-1][y+1][u'hint_num'] > 0:
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'

        if x == 0 and y == 0:#left top
            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'        

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y+1][u'tile_type'] == u'Empty' and self.tile[x+1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y+1][u'hint_num'] == 0:#8
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y+1)
                if self.tile[x+1][y+1][u'hint_num'] > 0:
                    self.tile[x+1][y+1][u'tile_state'] = u'UNCOVER'

        if x == 0 and y == self.Y - 1:#right top
            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y-1][u'tile_type'] == u'Empty' and self.tile[x+1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x+1][y-1][u'hint_num'] == 0:#6
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y-1)
                if self.tile[x+1][y-1][u'hint_num'] > 0:
                    self.tile[x+1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x+1][y][u'tile_type'] == u'Empty' and self.tile[x+1][y][u'tile_state'] == u'COVER':
                if self.tile[x+1][y][u'hint_num'] == 0:#7
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x+1, y)
                if self.tile[x+1][y][u'hint_num'] > 0:
                    self.tile[x+1][y][u'tile_state'] = u'UNCOVER'

        if x == self.X - 1 and y == 0 :#left bottom
            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y+1][u'tile_type'] == u'Empty' and self.tile[x-1][y+1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y+1][u'hint_num'] == 0:#3
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y+1)
                if self.tile[x-1][y+1][u'hint_num'] > 0:
                    self.tile[x-1][y+1][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y+1][u'tile_type'] == u'Empty' and self.tile[x][y+1][u'tile_state'] == u'COVER':
                if self.tile[x][y+1][u'hint_num'] == 0:#5
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y+1)
                if self.tile[x][y+1][u'hint_num'] > 0:
                    self.tile[x][y+1][u'tile_state'] = u'UNCOVER'

        if x == self.X - 1 and y == self.Y - 1:#right bottom
            if self.tile[x-1][y-1][u'tile_type'] == u'Empty' and self.tile[x-1][y-1][u'tile_state'] == u'COVER':
                if self.tile[x-1][y-1][u'hint_num'] == 0:#1
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y-1)
                if self.tile[x-1][y-1][u'hint_num'] > 0:
                    self.tile[x-1][y-1][u'tile_state'] = u'UNCOVER'

            if self.tile[x-1][y][u'tile_type'] == u'Empty' and self.tile[x-1][y][u'tile_state'] == u'COVER':
                if self.tile[x-1][y][u'hint_num'] == 0:#2
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x-1, y)
                if self.tile[x-1][y][u'hint_num'] > 0:
                    self.tile[x-1][y][u'tile_state'] = u'UNCOVER'

            if self.tile[x][y-1][u'tile_type'] == u'Empty' and self.tile[x][y-1][u'tile_state'] == u'COVER':
                if self.tile[x][y-1][u'hint_num'] == 0:#4
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'
                    self.showEmpty(x, y-1)
                if self.tile[x][y-1][u'hint_num'] > 0:
                    self.tile[x][y-1][u'tile_state'] = u'UNCOVER'

    def reverseTile(self, x, y):
        self.tile[x][y][u'tile_state'] = u'UNCOVER' 

    def markTile(self, x, y):
        if self.tile[x][y][u'tile_state'] <> u'UNCOVER':
            if self.tile[x][y][u'tile_state'] == u'COVER':
                self.temp = u'MARKFLAG'
            if self.tile[x][y][u'tile_state'] == u'MARKFLAG':
                self.temp = u'MARKQUESTION'
            if self.tile[x][y][u'tile_state'] == u'MARKQUESTION':
                self.temp = u'COVER'
            self.tile[x][y][u'tile_state'] = self.temp 

    def getClick(self, (x, y), button):
        if self.game_state == u'RUNNING':        
            if button == u'LEFT':
                self.reverseTile(x, y)
                self.checkWin()
                self.checkLose()
                if self.tile[x][y][u'tile_type'] == 'Empty' and self.tile[x][y][u'hint_num'] == 0:
                    self.showEmpty(x, y)

            if button == u'RIGHT':                
                self.markTile(x, y)

            if button == u'LEFT&RIGHT':
                #self.showAdjacent()
                print u'LEFT & RIGHT'

    def showAdjacent(self):
        pass

    def checkWin(self):
        self.counter = 0
        for x in range(self.X):
            for y in range(self.Y):
                if self.tile[x][y]['tile_type'] == u'Empty' and self.tile[x][y][u'tile_state'] == u'UNCOVER':
                    self.counter += 1
        if self.X * self.Y - self.mine_num == self.counter:
            print u'You Win!'
            self.game_state = u'END' 
            self.game_result = u'WIN' 
    
    def checkLose(self):
        for x in range(self.X):
            for y in range(self.Y):
                if self.tile[x][y][u'tile_type'] == u'Mine' and self.tile[x][y][u'tile_state'] == u'UNCOVER':
                    print u'You Lose!'
                    self.game_state = u'END'#0--end, 1--processing
                    self.game_result = u'LOSE'

        if self.game_result == u'LOSE':
            for x in range(self.X):
                for y in range(self.Y):
                    if self.tile[x][y][u'tile_type'] == u'Mine':
                        self.tile[x][y][u'tile_state'] = u'UNCOVER'

    def returnTile(self):
        return self.tile

    def returnMineNum(self):
        return self.mine_num

    def returnEmptyNum(self):
        self.empty_counter = 0
        for j in range(self.Y):
            for i in range(self.X):
                if self.tile[i][j][u'tile_type'] == u'Empty' and self.tile[i][j][u'tile_state'] == u'UNCOVER':
                    self.empty_counter += 1
        self.empty_num = self.X * self.Y - self.mine_num - self.empty_counter
        return self.empty_num

    def returnMarkNum(self):
        self.mark_counter = 0
        for j in range(self.Y):
            for i in range(self.X):
                if self.tile[i][j][u'tile_state'] == 2:
                    self.mark_counter += 1
        return self.mark_counter

    def returnGameState(self):
        return self.game_state# RUNNING || END

    def returnGameResult(self):
        return self.game_result #WIN || LOSE

    def displayTile(self):
        for y in range(self.Y):
            for x in range(self.X):
                if self.tile[x][y][u'tile_type'] == u'Mine':
                    print 9,
                    self.mine_counter += 1
                elif self.tile[x][y][u'tile_type'] == u'Empty':
                    print self.tile[x][y][u'hint_num'],
            print ''

    def displayEmpty(self):
        for x in range(self.X):
            for y in range(self.Y):
                if self.tile[x][y][u'tile_type'] == u'Empty' and self.tile[x][y][u'hint_num'] == 0:
                    self.test = (x, y)
                    print self.test                    
                if self.test <> ():
                    break
            if self.test <> ():
                    break
        print self.test
        self.showEmpty(self.test[0], self.test[1])

        for x in range(self.X):
            for y in range(self.Y):
                if self.tile[x][y][u'tile_type'] == u'Mine':
                    print 9,
                elif self.tile[x][y][u'tile_type'] == u'Empty':
                    if self.tile[x][y][u'tile_state'] == 0:
                        print self.tile[x][y][u'hint_num'],
                    if self.tile[x][y][u'tile_state'] == 1:
                        print u'X',
            print ''


def main():
    test = Tile(10, 20)
    test.initMine()
    test.initHint()
    test.displayEmpty()
    #test.showWhite(1, 1)
    #test.displayEmpty()


    
if __name__ == '__main__':
    main()



