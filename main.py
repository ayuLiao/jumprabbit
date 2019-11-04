# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 5
# Video link: https://youtu.be/OmlQ0XCvIn0
# Jumping

import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # # 玩家在界面中时(y>0)，进行碰撞检测，检测玩家是否碰撞到平台
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # if player reaches top 1/4 of screen
        # 玩家到达游戏框 1/4 处时（注意，游戏框，头部为0，底部为游戏框长度，到到游戏框的1/4处，表示已经到达了顶部一部分了）
        if self.player.rect.top <= HEIGHT / 4:
            # 玩家位置移动（往下移动）
            self.player.pos.y += abs(self.player.vel.y)
            # 平台在游戏框外时，将其注销，避免资源浪费
            for plat in self.platforms:
                # 平台移动位置（往下移动，移动的距离与玩家相同，这样玩家才能依旧站立在原本的平台上）
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT: 
                    plat.kill()

        # 判断平台数，产生新的平台
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            # 随机生成平台
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
