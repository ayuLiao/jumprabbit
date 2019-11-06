import pygame as pg
from settings import *
vec = pg.math.Vector2 # 二维变量

# 加载与解析精灵图片
class Spritesheet:
    def __init__(self, filename):
        # 主要要使用convert()进行优化， convert()方法会 改变图片的像素格式
        # 这里加载了整张图片
        self.spritesheet = pg.image.load(filename).convert()

    # 从比较大的精灵表中，通过相应的xml位置，抓取中出需要的元素
    def get_image(self, x, y, width, height):
        # 创建Surface对象(画板对象)
        image = pg.Surface((width, height))
        # blit — 画一个图像到另一个
        # 将整张图片中，对应位置(x,y)对应大小(width,height)中的图片画到画板中
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #  pygame.transform.scale 缩放的大小
        # 这里将图片缩放为原来的一半
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # 加载 bunny1_ready状态的兔子图片
        # self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        self.image = self.game.spritesheet.get_image(581, 1265, 121, 191)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0) # 速度
        self.acc = vec(0, 0) # 加速度

    def jump(self):
        # 跳跃到其他平台 - 玩家对象x加减1，为了做碰撞检测，只有站立在平台上，才能实现跳跃
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
