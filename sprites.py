import pygame as pg
import random
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
        # 不同的状态
        self.walking = False
        self.jumping = False
        # 当前帧(用于判断当前要执行哪个动画)
        self.current_frame = 0
        self.last_update = 0
        self.load_images() # 加载图片
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0) # 速度
        self.acc = vec(0, 0) # 加速度

    def load_images(self):
        # 站立状态
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK) # 将图像矩阵中除图像外周围的元素都设置为透明的

        # 走动状态
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            # 水平翻转
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        # 跳跃状态
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump(self):
        # 跳跃到其他平台 - 玩家对象x加减1，为了做碰撞检测，只有站立在平台上，才能实现跳跃
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        # 动画
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # 获得加速度
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # 速度与加速度
        self.vel += self.acc
        # 如果速度小于0.1，则速度为0（比如这样设置，不然速度永远无法0）
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def animate(self):
        '''
        pygame 中的时间是以毫秒（千分之一秒）表示的。
        通过 pygame.time.get_ticks 函数可以获得 pygame.init 后经过的时间的毫秒数。
        '''
        now = pg.time.get_ticks()

        if self.vel.x != 0: # 判断速度在x轴方向是否为0，从而判断玩家对象是否移动
            self.walking = True
        else:
            self.walking = False

        # 走动状态下的动画
        if self.walking:
            # 当前时间 - 上次时间 大于 180，即间隔时间大于180时
            if now - self.last_update > 180:
                self.last_update = now
                # 当前帧 加一 与 walk_frames_l 长度取余，从而得到当前要做哪个东西
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                # 向左走还是向右走
                if self.vel.x > 0:
                    # 当前帧要做的动作
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # 站立状态下的动画
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # 载入图片
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        # 随机选择一种
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
