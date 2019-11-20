# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial' # 绘制时使用的字体
HS_FILE = "highscore.txt" # 记录最高分
SPRITESHEET = "spritesheet_jumper.png" # 精灵图片

# 玩家参数
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# 道具属性
BOOST_POWER = 60
POW_SPAWN_PCT = 7

# 不同元素在不同层
PLAYER_LAYER = 2 # 玩家
PLATFORM_LAYER = 1 # 平台
POW_LAYER = 1 # 道具
MOB_LAYER = 2 # 敌人
CLOUD_LAYER = 0 # 云


# 起始平台
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# 默认的颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE