#coding:utf-8
import pygame, sys, time
from pygame.locals import *
import os, random, time
import json

import mine_sweeper
import ui
import gc
print(gc.get_threshold())
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
class TileDisplay(): 
    def __init__(self, value):
        self.image = pygame.image.load(u'tile_back32.png') 
        self.image_back = pygame.image.load(u'tile_back32.png')
        self.image_flag = pygame.image.load(u'tile_flag32.png')
        self.image_question = pygame.image.load(u'tile32_QUESTIONMARK.png')

        self.image_num = []
        for i in range(10):
            self.image_num.append(pygame.image.load(u'tile32_' + str(i) + '.png'))

        self.offset_x = (WIDTH - TILE_X * TILE_SIZE) / 2
        self.offset_y = TILE_SIZE * 2 
        self.rect = (value[u'tile_coords'][0] * TILE_SIZE + self.offset_x, \
                value[u'tile_coords'][1] * TILE_SIZE + self.offset_y, TILE_SIZE, TILE_SIZE)
        self.tile_value = value

    def update(self):
        if self.tile_value[u'tile_state'] == u'COVER':
            self.image = pygame.image.load(u'tile_back32.png')
        if self.tile_value[u'tile_state'] == u'UNCOVER':
            if self.tile_value[u'tile_type'] == 'Mine':
                self.image = self.image_num[9]
            if self.tile_value[u'tile_type'] == 'Empty':
                self.image = self.image_num[self.tile_value[u'hint_num']]
        if self.tile_value[u'tile_state'] == u'MARKFLAG':            
            self.image = self.image_flag 
        if self.tile_value[u'tile_state'] == u'MARKQUESTION':
            self.image = self.image_question
#-------------------------------------------------------------------------
class TitleMenu:
    def __init__(self):
        self.TILE_X = 0
        self.TILE_Y = 0
        self.lv1_btn = ui.Button(u'button_lv1.png', (WIDTH / 2, 100))
        self.lv2_btn = ui.Button(u'button_lv2.png', (WIDTH / 2, 200))
        self.lv3_btn = ui.Button(u'button_lv3.png', (WIDTH / 2, 300))
        self.rank_btn = ui.Button(u'button_rank.png', (WIDTH / 2, 400))

        self.exit_btn = ui.Button(u'exit32.png', (WIDTH - TILE_SIZE, HEIGHT - TILE_SIZE))
        self.titleMenu_ui_sprites = pygame.sprite.Group()

        self.titleMenu_ui_sprites.add(self.lv1_btn)
        self.titleMenu_ui_sprites.add(self.lv2_btn)
        self.titleMenu_ui_sprites.add(self.lv3_btn)
        self.titleMenu_ui_sprites.add(self.exit_btn)
        self.titleMenu_ui_sprites.add(self.rank_btn)

        self.game_process = 'title'

    def titleMenu(self, btn, pos):
        self.mouse_button = btn
        self.mouse_pos = pos

        if self.mouse_button == 1:# start & quit
            if self.lv1_btn.checkClick(self.mouse_button, self.mouse_pos):
                self.TILE_X = 9
                self.TILE_Y = 9
                self.game_process = 'init_board'
            if self.lv2_btn.checkClick(self.mouse_button, self.mouse_pos):
                self.TILE_X = 16
                self.TILE_Y = 16
                self.game_process = 'init_board'
            if self.lv3_btn.checkClick(self.mouse_button, self.mouse_pos):
                self.TILE_X = 24
                self.TILE_Y = 16
                self.game_process = 'init_board'
            if self.rank_btn.checkClick(self.mouse_button, self.mouse_pos):
                self.game_process = 'rank_board'
            if self.exit_btn.checkClick(self.mouse_button, self.mouse_pos):
                pygame.quit()
                sys.exit()

        DISPLAYSURF.blit(background, (0, 0, WIDTH, HEIGHT))
    
        self.titleMenu_ui_sprites.update()
        self.titleMenu_ui_sprites.draw(DISPLAYSURF)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    def returnXY(self):
        return (self.TILE_X, self.TILE_Y)

    def returnGameProcess(self):
        return self.game_process
#------------------------------------------------------------------------
class Board:
    def __init__(self, x, y):
        self.TILE_X = x
        self.TILE_Y = y
        self.T_calcu = [[0 for y in range(TILE_Y)]for x in range(TILE_X)]
        self.board_ui_sprites = pygame.sprite.Group()

        self.empty_img = ui.Button(u'tile32_0.png', (WIDTH / 2 - TILE_SIZE * 3.5, HEIGHT - TILE_SIZE))
        self.mine_img = ui.Button(u'tile32_9.png', (WIDTH / 2 - TILE_SIZE / 2, HEIGHT - TILE_SIZE))
        self.flag_img = ui.Button(u'tile_flag32.png', (WIDTH / 2 + TILE_SIZE * 2.5, HEIGHT - TILE_SIZE) )    
        self.timer_img = ui.Button(u'timer32.png', (WIDTH / 2 - TILE_SIZE / 2, TILE_SIZE))


        self.board_ui_sprites.add(self.flag_img)    
        self.board_ui_sprites.add(self.mine_img)    
        self.board_ui_sprites.add(self.empty_img)    
        self.board_ui_sprites.add(self.timer_img)

        self.restart_btn = ui.Button(u'restart32.png', (TILE_SIZE, HEIGHT - TILE_SIZE))
        self.exit_btn = ui.Button(u'exit32.png', (WIDTH - TILE_SIZE, HEIGHT - TILE_SIZE))

        self.board_ui_sprites.add(self.restart_btn)
        self.board_ui_sprites.add(self.exit_btn)

        self.my_tile = mine_sweeper.Tile(self.TILE_X, self.TILE_Y)
        self.my_tile.initMine()
        self.my_tile.initHint()
       
        self.TILE_value = self.my_tile.returnTile()
        for x in range(self.TILE_X):
            for y in range(self.TILE_Y):
                self.T_calcu[x][y] = TileDisplay(self.TILE_value[x][y])


        self.game_state = 0#0--not start yet, 1--processing, 2--game over
        self.game_time = 0
        self.start_time = 0

        self.rank = [0 for i in range(4)]
        self.rank_list = [[]for i in range(3)]
        self.write_mark = 0

    def board(self, btn, pos):
        self.game_process = 'board'
        self.mouse_button = btn
        self.mouse_pos = pos
        self.game_font = pygame.font.SysFont('arial', 20)
        self.game_font2 = pygame.font.SysFont('arial', 20)
        BLACK = (0,0,0)
        RED = (255,0,0)
        DISPLAYSURF.blit(background, (0, 0, WIDTH, HEIGHT))

        self.tile_pos = (int((self.mouse_pos[0] - (WIDTH - self.TILE_X * TILE_SIZE) / 2) / TILE_SIZE), \
                    int((self.mouse_pos[1] - TILE_SIZE * 2)/ TILE_SIZE))

        if self.mouse_button == 1:# restart & quit
            if self.restart_btn.checkClick(self.mouse_button, self.mouse_pos):        
                self.game_process = 'title'
            if self.exit_btn.checkClick(self.mouse_button, self.mouse_pos):
                pygame.quit()
                sys.exit()

        if self.mouse_button == 1 or self.mouse_button == 3:
            if self.mouse_button == 1:
                self.mouse_button = u'LEFT'
            if self.mouse_button == 3:
                self.mouse_button = u'RIGHT'

            if -1 < self.tile_pos[0] < self.TILE_X and -1 < self.tile_pos[1] < self.TILE_Y:
                self.my_tile.getClick(self.tile_pos, self.mouse_button)

                for x in range(self.TILE_X):
                    for y in range(self.TILE_Y):
                        self.T_calcu[x][y].tile_value = self.TILE_value[x][y]
                        self.T_calcu[x][y].update()
                
                if self.my_tile.returnGameState() == 0:
                    self.game_state = u'END'

            if self.game_state == 0:
                self.game_state = 1# mark the first mouse click

        if self.my_tile.returnGameResult() == 1:
            self.win_text = self.game_font.render('YOU WIN!!!', True, RED)
            DISPLAYSURF.blit(self.win_text, (WIDTH / 2 + TILE_SIZE * 6, HEIGHT - 40))
            if self.write_mark == 0:
                self.addToRankList()
        if self.my_tile.returnGameResult() == 2:
            self.win_text = self.game_font.render('YOU LOSE!!!', True, RED)
            DISPLAYSURF.blit(self.win_text, (WIDTH / 2 + TILE_SIZE * 6, HEIGHT - 40))

        if self.game_state == 0 :
            self.game_time = 0
        if self.game_state == 1:
            self.start_time = pygame.time.get_ticks()
            self.game_state = 'After First Click'
        if self.game_state == 'After First Click':
            self.game_time = int((pygame.time.get_ticks() - self.start_time) / 1000)


        self.time_text = self.game_font.render(str(self.game_time), True, BLACK)
        DISPLAYSURF.blit(self.time_text, (WIDTH / 2 + TILE_SIZE, 20, TILE_SIZE, TILE_SIZE))
        
        self.empty_text = self.game_font.render(str(self.my_tile.returnEmptyNum()), True, BLACK)
        self.mine_text = self.game_font.render(str(self.my_tile.returnMineNum()), True, BLACK)
        self.flag_text = self.game_font.render(str(self.my_tile.returnMarkNum()), True, BLACK)
        DISPLAYSURF.blit(self.empty_text, (WIDTH / 2 - TILE_SIZE * 2.5, HEIGHT - 45, TILE_SIZE, TILE_SIZE))
        DISPLAYSURF.blit(self.mine_text, (WIDTH / 2 + 20 , HEIGHT - 45, TILE_SIZE, TILE_SIZE))
        DISPLAYSURF.blit(self.flag_text, (WIDTH / 2 + 110, HEIGHT - 45, TILE_SIZE, TILE_SIZE))

        for x in range(self.TILE_X):
            for y in range(self.TILE_Y):
                self.T_calcu[x][y].tile_value = self.TILE_value[x][y]
                self.T_calcu[x][y].update()
                DISPLAYSURF.blit(self.T_calcu[x][y].image, self.T_calcu[x][y].rect)
        
        self.board_ui_sprites.update()
        self.board_ui_sprites.draw(DISPLAYSURF)        

        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    def addToRankList(self):
        self.write_mark = 1
        self.rank_file = open('rank_file.json', 'r')
        
        try:
            self.rank_list = json.load(self.rank_file)
            self.rank_file.close()
        except:
            pass
        
        self.rank_file = open('rank_file.json', 'w')
        
        self.rank[0] = str(self.TILE_X) + '*' + str(self.TILE_Y)
        self.rank[1] = str(self.my_tile.returnMineNum())
        self.rank[2] = str(self.game_time)
        #self.rank[3] = str(time.asctime(time.localtime(time.time())))
        self.rank[3] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print self.rank

        if self.TILE_X == 9:
            self.rank_list[0].append(self.rank)
            self.rank_list[0].sort(key=lambda x: x[2])
            if len(self.rank_list[0]) > 10:
                self.rank_list[0] = self.rank_list[0][:10]
        if self.TILE_X == 16:
            self.rank_list[1].append(self.rank)
            self.rank_list[1].sort(key=lambda x: x[2])
            if len(self.rank_list[1]) > 10:
                self.rank_list[1] = self.rank_list[1][:10]
        if self.TILE_X == 24:
            self.rank_list[2].append(self.rank)
            self.rank_list[2].sort(key=lambda x: x[2])
            if len(self.rank_list[2]) > 10:
                self.rank_list[2] = self.rank_list[0][:10]

        self.rank_file.write(json.dumps(self.rank_list))
        self.rank_file.close()
        print 'Write rank finish'

    def returnGameProcess(self):        
        return self.game_process
#--------------------------------------------------------------------------
class RankBoard:
    def __init__(self):
        self.Tiles_sprites = pygame.sprite.Group()
        self.rankboard_ui_sprites = pygame.sprite.Group()

        self.exit_btn = ui.Button(u'exit32.png', (WIDTH - TILE_SIZE, HEIGHT - TILE_SIZE))

        self.rankboard_ui_sprites.add(self.exit_btn)

        self.isGetList = 0
        self.rank_list = [[]for i in range(3)]

        self.lv1_btn = ui.Button(u'button_lv1.png', (100, 50))
        self.lv2_btn = ui.Button(u'button_lv2.png', (400, 50))
        self.lv3_btn = ui.Button(u'button_lv3.png', (680, 50))

        self.rankboard_ui_sprites.add(self.lv1_btn)
        self.rankboard_ui_sprites.add(self.lv2_btn)
        self.rankboard_ui_sprites.add(self.lv3_btn)


    def rankBoard(self, btn, pos):
        self.game_process = 'rank_board'
        self.mouse_button = btn
        self.mouse_pos = pos
        self.game_font = pygame.font.SysFont('arial', 20)
        self.game_font2 = pygame.font.SysFont('arial', 20)
        BLACK = (0,0,0)
        RED = (255,0,0)
        DISPLAYSURF.blit(background, (0, 0, WIDTH, HEIGHT))

        if self.mouse_button == 1:#quit
            if self.exit_btn.checkClick(self.mouse_button, self.mouse_pos):
                self.game_process = 'title'
                self.isGetList = 0

        self.rankboard_ui_sprites.update()
        self.rankboard_ui_sprites.draw(DISPLAYSURF)
        
        self.showRank()
        for rank_type in self.rank_list:
            self.counter = 0
            for rank in rank_type:
                if rank[0] == '9*9':
                    self.tile_text_9 = self.game_font.render(str(rank[0]), True, BLACK)
                    self.time_text_9 = self.game_font.render(str(rank[2]), True, BLACK)
                    self.date_text_9 = self.game_font.render(str(rank[3]), True, BLACK)

                    DISPLAYSURF.blit(self.time_text_9, (10, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    DISPLAYSURF.blit(self.date_text_9, (50, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    self.counter += 20
            self.counter = 0
            for rank in rank_type:
                if rank[0] == '16*16':
                    self.tile_text_16 = self.game_font.render(str(rank[0]), True, BLACK)
                    self.time_text_16 = self.game_font.render(str(rank[2]), True, BLACK)
                    self.date_text_16 = self.game_font.render(str(rank[3]), True, BLACK)

                    DISPLAYSURF.blit(self.time_text_16, (310, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    DISPLAYSURF.blit(self.date_text_16, (350, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    self.counter += 20
            self.counter = 0
            for rank in rank_type:
                if rank[0] == '24*16':
                    self.tile_text_24 = self.game_font.render(str(rank[0]), True, BLACK)
                    self.time_text_24 = self.game_font.render(str(rank[2]), True, BLACK)
                    self.date_text_24 = self.game_font.render(str(rank[3]), True, BLACK)

                    DISPLAYSURF.blit(self.time_text_24, (610, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    DISPLAYSURF.blit(self.date_text_24, (650, 100 + self.counter, TILE_SIZE, TILE_SIZE))
                    self.counter += 20
        
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    def showRank(self):
        self.rank_file = open('rank_file.json', 'r')
        try:
            self.rank_list = json.load(self.rank_file)
            self.rank_file.close()
        except:
            pass
        self.isGetList = 1

    def returnGameProcess(self):
        return self.game_process

def initRankFile():
    if os.path.exists('rank_file.json'):
        print 'rank file exist'
    else:
        print 'rank file do not exist, creat'
        rank_file = open('rank_file.json','w')
        rank_file.write(json.dumps([[]for i in range(3)]))
        rank_file.close()
#--------------------------------------------------------------------------
def main():
    pygame.init()
    initRankFile()
    global TILE_X, TILE_Y, background
    global FPSCLOCK, FPS
    global DISPLAYSURF, WIDTH, HEIGHT
    global TILE_SIZE

    mouse_pos = (None, None)
    mouse_button = 0
    TILE_X = 0
    TILE_Y = 0
    TILE_SIZE = 32 

    WIDTH = 800 #TILE_SIZE * TILE_X
    HEIGHT = 640 #TILE_SIZE * TILE_Y

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(u'Mine Sweeper')
    FPS = 60 
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)

    game_process = 'title'

    FPSCLOCK = pygame.time.Clock()
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(WHITE)

    rank_board = RankBoard()
#--------------------------------------------------------------------------------
    while True:
        titleMenu = TitleMenu()
#--------------------------------------------------------------------------------
        while game_process == 'title':
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == MOUSEBUTTONUP:
                    mouse_button = event.button
            titleMenu.titleMenu(mouse_button, mouse_pos)
            mouse_button = 0
            game_process = titleMenu.returnGameProcess()
            TILE_X, TILE_Y = titleMenu.returnXY()
#--------------------------------------------------------------------------------
        while game_process == 'rank_board':
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == MOUSEBUTTONUP:
                    mouse_button = event.button
            rank_board.rankBoard(mouse_button, mouse_pos)
            rank_board.showRank()
            mouse_button = 0
            game_process = rank_board.returnGameProcess()
#--------------------------------------------------------------------------------
        if game_process == 'init_board':
            print TILE_X, TILE_Y
            board = Board(TILE_X, TILE_Y)
            game_process = 'board'
#--------------------------------------------------------------------------------
        while game_process == 'board':
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == MOUSEBUTTONUP:
                    mouse_button = event.button
                mouse_state = pygame.mouse.get_pressed()
            board.board(mouse_button, mouse_pos)
            mouse_button = 0
            game_process = board.returnGameProcess()

#--------------------------------------------------------------------------------
main()
