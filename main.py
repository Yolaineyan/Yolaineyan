import pygame
import random
import sys

# 定义游戏相关属性
TITLE = '羊了个羊小游戏'
WIDTH = 1920/2 # 放大后的宽度
HEIGHT = 1080/2  # 放大后的高度
FPS = 120

# 自定义游戏常量
T_WIDTH = 55  # 牌的宽度
T_HEIGHT = 55 # 牌的高度

# 下方牌堆的位置
DOCK = pygame.Rect((300, 485), (T_WIDTH *6, T_HEIGHT))  # 调整牌堆的位置

# 上方的所有牌
tiles = []
# 牌堆里的牌
docks = []

# 难度设置
DIFFICULTY = ''

# 清空道具的属性
CLEAR_ITEM_IMAGE = pygame.image.load('images/clear_item.png')  # 假设你有一个清空道具的图片
CLEAR_ITEM_RECT = pygame.Rect((WIDTH - 200, 20), (100, 100))  # 调整道具的位置
has_clear_item = True  # 玩家是否拥有清空道具的标志

# 返回主菜单按钮
BACK_BUTTON_IMAGE = pygame.image.load('images/back_button.png')  # 假设你有一个返回按钮的图片
BACK_BUTTON_RECT = pygame.Rect((10, 10), (100, 50))  # 按钮位置和大小

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 设置为窗口模式，并放大
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# 加载背景和遮罩图像
background = pygame.image.load('images/back.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # 背景适配屏幕
mask = pygame.image.load('images/mask.png')
mask = pygame.transform.scale(mask, (T_WIDTH, T_HEIGHT))  # 遮罩也需要适配
end = pygame.image.load('images/end.png')
end = pygame.transform.scale(end, (WIDTH/2, HEIGHT/2))  # 结束界面适配
win = pygame.image.load('images/win.png')
win = pygame.transform.scale(win, (WIDTH/2, HEIGHT/2))  # 胜利界面适配

# 加载按钮图片
easy_button = pygame.image.load('images/easy_button.png')
normal_button = pygame.image.load('images/normal_button.png')
hard_button = pygame.image.load('images/hard_button.png')

# 播放背景音乐
pygame.mixer.music.load('music/bgm.mp3')
pygame.mixer.music.play(-1)

# 自定义牌类
class CustomTile:
    def __init__(self, image, rect, tag, layer, status):
        self.image = image
        self.rect = rect
        self.tag = tag
        self.layer = layer
        self.status = status

# 难度选择界面
def difficulty_select():
    global DIFFICULTY
    easy_rect = easy_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))  # 调整按钮位置
    normal_rect = normal_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    hard_rect = hard_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    DIFFICULTY = ''  # 初始化难度为空字符串
    while DIFFICULTY not in ['easy', 'normal', 'hard']:
        screen.fill((0, 0, 0))  # 用黑色填充屏幕
        screen.blit(background, (0, 0))  # 绘制背景图像
        screen.blit(easy_button, easy_rect)  # 绘制简单模式按钮
        screen.blit(normal_button, normal_rect)  # 绘制普通模式按钮
        screen.blit(hard_button, hard_rect)  # 绘制困难模式按钮
        pygame.display.update()  # 更新屏幕显示

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    DIFFICULTY = 'easy'
                elif normal_rect.collidepoint(event.pos):
                    DIFFICULTY = 'normal'
                elif hard_rect.collidepoint(event.pos):
                    DIFFICULTY = 'hard'

    return DIFFICULTY

# 初始化牌组，12*12张牌随机打乱
def init_tile_group():
    ts = ['zuanshi', 'hongshi', 'tiedin', 'lvbaoshi', 'meitan', 'qingshi'] * 6
    random.shuffle(ts)
    n = 0
    for k in range(4):  # 4层
        for i in range(4 - k):  # 每层减1行
            for j in range(4 - k):
                t = ts[n]  # 获取排种类
                n += 1
                tile_image = pygame.image.load(f'images/{t}.png')  # 加载对应的图片
                tile_image = pygame.transform.scale(tile_image, (T_WIDTH, T_HEIGHT))
                tile_rect = tile_image.get_rect()
                tile_rect.topleft = (350 + (k * 0.5 + j) * T_WIDTH, 150 + (k * 0.5 + i) * T_HEIGHT * 0.9)
                tile = CustomTile(tile_image, tile_rect, t, k, 1 if k == 3 else 0)
                tiles.append(tile)
    for i in range(6):  # 剩余的6张牌放下面（为了凑整能通关）
        t = ts[n]
        n += 1
        tile_image = pygame.image.load(f'images/{t}.png')
        tile_image = pygame.transform.scale(tile_image, (T_WIDTH, T_HEIGHT))
        tile_rect = tile_image.get_rect()
        tile_rect.topleft = (300 + i * T_WIDTH, 375)  # 调整底部位置
        tile = CustomTile(tile_image, tile_rect, t, 0, 1)
        tiles.append(tile)

# 游戏帧绘制函数
def draw():
    screen.blit(background, (0, 0))
    for tile in tiles:
        screen.blit(tile.image, tile.rect)
        if tile.status == 0:
            screen.blit(mask, tile.rect)
    for i, tile in enumerate(docks):
        tile.rect.left = DOCK.x + i * T_WIDTH
        tile.rect.top = DOCK.y
        screen.blit(tile.image, tile.rect)
    if len(docks) >= 7:
        screen.blit(end, (0, 0))
    if not tiles:
        screen.blit(win, (0, 0))
    if has_clear_item:
        screen.blit(CLEAR_ITEM_IMAGE, CLEAR_ITEM_RECT)
    screen.blit(BACK_BUTTON_IMAGE, BACK_BUTTON_RECT)  # 绘制返回主菜单按钮
    pygame.display.flip()

# 鼠标点击响应
def on_mouse_down(pos):
    global docks, has_clear_item
    if BACK_BUTTON_RECT.collidepoint(pos):
        return_to_menu()  # 调用返回主菜单函数
    if len(docks) >= 7 or not tiles:
        return
    if has_clear_item and CLEAR_ITEM_RECT.collidepoint(pos):
        has_clear_item = False  # 消耗道具
        # 将卡槽里的牌放到底部牌堆的上方
        bottom_deck_start_y = 485 - T_HEIGHT  # 底部牌堆的上方起始y坐标
        for i, tile in enumerate(docks):
            tile.status = 1  # 重置状态为可点击
            # 计算应该放置的位置（底部牌堆的上方）
            new_x = 300 + i * T_WIDTH
            new_y = bottom_deck_start_y + (i // 7) * T_HEIGHT
            tile.rect.topleft = (new_x, new_y)
            tiles.append(tile)  # 加入到tiles列表
        docks.clear()  # 清空卡槽
        return
    for tile in reversed(tiles):  # 逆序循环是为了先判断上方的牌
        if tile.status == 1 and tile.rect.collidepoint(pos):
            tile.status = 2
            tiles.remove(tile)
            docks.append(tile)
            # 根据难度检查是否可以消除
            if DIFFICULTY == 'easy':
                # 简单模式下，一张相同的卡片就可以消除
                if len([t for t in docks if t.tag == tile.tag]) >= 1:
                    docks = [t for t in docks if t.tag != tile.tag]
            elif DIFFICULTY == 'normal':
                # 普通模式下，需要两张相同的卡片
                if len([t for t in docks if t.tag == tile.tag]) >= 2:
                    docks = [t for t in docks if t.tag != tile.tag]
            elif DIFFICULTY == 'hard':
                # 困难模式下，需要三张相同的卡片
                if len([t for t in docks if t.tag == tile.tag]) >= 3:
                    docks = [t for t in docks if t.tag != tile.tag]
            for down in tiles:
                if down.layer == tile.layer - 1 and down.rect.colliderect(tile.rect):
                    for up in tiles:
                        if up.layer == down.layer + 1 and up.rect.colliderect(down.rect):
                            break
                    else:
                        down.status = 1
            return

# 返回主菜单
def return_to_menu():
    global tiles, docks, DIFFICULTY, has_clear_item
    tiles.clear()
    docks.clear()
    DIFFICULTY = ''
    has_clear_item = True
    difficulty_select()  # 重新进入难度选择界面
    init_tile_group()  # 重新初始化牌组

# 游戏主循环
def main():
    difficulty_select()  # 调用难度选择界面
    init_tile_group()  # 初始化牌组
    has_clear_item = True  # 玩家开始时拥有清空道具
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_down(event.pos)
        draw()
        clock.tick(FPS)
    pygame.quit()

# 启动游戏
main()
