import sys
import math
import random
import pygame
import subprocess

# 定义颜色常量
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)

# 全局设置类
class Settings:
    def __init__(self):
        self.screen_size = (self.screen_width, self.screen_height) = (600, 700)  # 游戏窗口大小
        self.game_size = (self.game_row, self.game_col) = (8, 8)  # 游戏网格的行列数
        self.map_total = self.game_row * self.game_col  # 游戏网格总数
        self.element_num = 12  # 游戏中的元素数量
        self.bg_color = (220, 220, 220)  # 背景颜色
        self.title = '水果连连看'  # 游戏标题
        self.win_image = './image/you_win.png'  # 胜利时显示的图片路径
        self.grid_size = min(self.screen_width // self.game_col, self.screen_width // self.game_row)  # 每个网格的大小
        padding = 10  # 填充大小
        self.scale_size = (self.grid_size - padding, self.grid_size - padding)  # 缩放后的网格大小
        self.points = []  # 初始化点的列表，用于存储游戏中的点

settings = Settings()

map_list = []  # 图像列表映射
image_list = []  # 图像列表

button_size = (50, 50)  # 定义统一的按钮大小

class ImageBtn:
    def __init__(self, screen, image_path, x, y, number, element, size, buffer=5):
        self.x = x  # 按钮的 x 坐标
        self.y = y  # 按钮的 y 坐标
        self.buffer = buffer  # 按钮的点击区域缓冲区
        self.active = False  # 按钮的激活状态
        self.element = element  # 按钮的元素
        self.number = number  # 按钮的编号
        self.screen = screen  # 显示按钮的屏幕
        self.image = pygame.image.load(image_path)  # 加载按钮的图像
        self.w = size[0]  # 按钮的宽度
        self.h = size[1]  # 按钮的高度
        self.image = pygame.transform.scale(self.image, size)  # 缩放图像到指定大小
        self.checked = False

    def display(self):
        if self.checked:
            pygame.draw.rect(self.image, (0, 205, 205, 255),
                             (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 2)
        else:
            pygame.draw.rect(self.image, (0, 205, 205, 0),
                             (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 2)
        self.screen.blit(self.image, (self.x, self.y))

    def hide(self):
        self.checked = False
        self.image.fill((255, 255, 240))

    def is_checkable(self):
        return True

    def click(self):
        self.checked = not self.checked
        return self.checked

    def reset(self):
        self.checked = False

    def get_geometry(self):
        return self.x, self.y, self.w, self.h

    def get_center(self):
        return self.x + self.w / 2, self.y + self.h / 2

# 水平扫描函数
def horizontal_scan(points):
    column = settings.game_col
    p1_x = int(points[0].number % column)
    p1_y = int(points[0].number / column)
    p2_x = int(points[1].number % column)
    p2_y = int(points[1].number / column)

    if p1_y == p2_y:
        return False

    hLine1 = min(p1_y, p2_y)
    hLine2 = max(p1_y, p2_y)
    leftLimit = 0
    rightLimit = column - 1

    i = p1_x
    while i > 0:
        if map_list[p1_y * column + i - 1] != 0:
            break
        i -= 1
    leftLimit = i

    i = p2_x
    while i > 0:
        if map_list[p2_y * column + i - 1] != 0:
            break
        i -= 1
    leftLimit = max(leftLimit, i)

    if leftLimit == 0:
        return True

    i = p1_x
    while i < column - 1:
        if map_list[p1_y * column + i + 1] != 0:
            break
        i += 1
    rightLimit = i

    i = p2_x
    while i < column - 1:
        if map_list[p2_y * column + i + 1] != 0:
            break
        i += 1
    rightLimit = min(rightLimit, i)

    if rightLimit == column - 1:
        return True

    if leftLimit > rightLimit:
        return False

    for i in range(leftLimit, rightLimit + 1):
        for j in range(hLine1 + 1, hLine2):
            if map_list[j * column + i] != 0:
                break
        else:
            return True

    return False

# 垂直扫描函数
def vertical_scan(points):
    row = settings.game_row
    column = settings.game_col
    p1_x = int(points[0].number % column)
    p1_y = int(points[0].number / column)
    p2_x = int(points[1].number % column)
    p2_y = int(points[1].number / column)

    if p1_x == p2_x:
        return False

    vLine1 = min(p1_x, p2_x)
    vLine2 = max(p1_x, p2_x)
    topLimit = 0
    bottomLimit = row - 1

    i = p1_y
    while i > 0:
        if map_list[p1_x + (i - 1) * column] != 0:
            break
        i -= 1
    topLimit = i

    i = p2_y
    while i > 0:
        if map_list[p2_x + (i - 1) * column] != 0:
            break
        i -= 1
    topLimit = max(topLimit, i)

    if topLimit == 0:
        return True

    i = p1_y
    while i < row - 1:
        if map_list[p1_x + (i + 1) * column] != 0:
            break
        i += 1
    bottomLimit = i

    i = p2_y
    while i < row - 1:
        if map_list[p2_x + (i + 1) * column] != 0:
            break
        i += 1
    bottomLimit = min(bottomLimit, i)

    if bottomLimit == row - 1:
        return True

    if topLimit > bottomLimit:
        return False

    for i in range(topLimit, bottomLimit + 1):
        for j in range(vLine1 + 1, vLine2):
            if map_list[i * column + j] != 0:
                break
        else:
            return True

    return False

def can_clear(points):
    if points[0].element != points[1].element:
        return False
    else:
        if vertical_scan(points) or horizontal_scan(points):
            return True
        else:
            return False

def handle_button_click(btns, click_list):
    global score
    score += 10  # 需要先声明score为全局变量
    click_list[0].hide()
    click_list[1].hide()

    index1 = click_list[0].number
    index2 = click_list[1].number
    click_list = []
    map_list[index1] = 0
    map_list[index2] = 0
    return click_list

def build_map():
    t_list = []
    m_list = []
    for i in range(0, settings.map_total, 2):
        e = math.ceil(random.random() * settings.element_num)
        t_list.append(e)
        t_list.append(e)

    for i in range(0, settings.map_total):
        index = int(random.random() * (settings.map_total - i))
        m_list.append(t_list[index])
        t_list.pop(index)

    # 确定固定的空缺形状
    empty_shapes = [
    [0,7,14,21,28,35,42,49,56,63],# 第一个形状示例
    [6,7,13,14,15,20,21,22,27,28,29,34,35,36,41,42,43,48,49,50,56,57],# 第二个形状示例
    [16, 17, 22, 23, 27, 28, 35, 36, 40, 41, 46, 47],  # 第三个形状示例
    [0,1,2,5,6,7,8,9,14,15,16,23,40,47,48,49,54,55,56,57,58,61,62,63]# 第四个形状示例
    ]
    # 随机选择一个形状
    empty_indices = random.choice(empty_shapes)
    for index in empty_indices:
        m_list[index] = 0

    return m_list

def is_over():
    for each in map_list:
        if each > 0:
            return False
    return True

global screen

def reset_game():
    global map_list, image_list, play, paused, start_ticks, last_update_time, remind_count, shuffle_count, paused_time
    map_list = build_map()
    image_list = []
    for i in range(0, settings.map_total):
        if map_list[i] != 0:  # 跳过值为 0 的元素
            x = int(i % settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[0]) / 2
            y = int(i / settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[1]) / 2 + 100
            element = './image/' + str(map_list[i]) + '.png'
            image_list.append(ImageBtn(screen, element, x, y, i, map_list[i], settings.scale_size))
    play = True
    paused = False
    start_ticks = pygame.time.get_ticks()  # 重置开始时间
    last_update_time = start_ticks
    paused_time = 0  # 重置暂停时间
    remind_count = 0  # 初始化提示次数
    shuffle_count = 0  # 初始化洗牌次数

def shuffle_game():
    global map_list, image_list
    remaining_elements = [map_list[i] for i in range(len(map_list)) if map_list[i] != 0]
    # 洗牌打乱顺序
    random.shuffle(remaining_elements)
    # 重新分配打乱后的图片到网格中
    j = 0
    for i in range(len(map_list)):
        if map_list[i] != 0:
            map_list[i] = remaining_elements[j]
            j += 1
    # 更新图片按钮
    image_list = []
    for i in range(0, settings.map_total):
        if map_list[i] != 0:  # 跳过值为 0 的元素
            x = int(i % settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[0]) / 2
            y = int(i / settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[1]) / 2 + 100
            element = './image/' + str(map_list[i]) + '.png'
            image_list.append(ImageBtn(screen, element, x, y, i, map_list[i], settings.scale_size))
    print("洗牌已完成")

def find_pair_to_clear():
    for i in range(len(image_list)):
        for j in range(i + 1, len(image_list)):
            if map_list[image_list[i].number] != 0 and map_list[image_list[j].number] != 0:
                points = [image_list[i], image_list[j]]
                if points[0].element == points[1].element and can_clear(points):
                    return points
    return None

def display_win_screen(screen, seconds, remind_count, shuffle_count):
    font = pygame.font.SysFont('SimHei', 24)
    youwin = pygame.image.load(settings.win_image)
    youwin = pygame.transform.scale(youwin, (settings.screen_width, settings.screen_height))
    screen.blit(youwin, (0, 0))

    # 调整文字的位置
    text1 = font.render(f'通关时间:', True, (0, 0, 0))
    win_text = font.render(f'{seconds:.2f} 秒', True, (0, 0, 0))
    text2 = font.render(f'次数: ', True, (0, 0, 0))
    remind_text = font.render(f' {remind_count}', True, (0, 0, 0))
    shuffle_text = font.render(f' {shuffle_count}', True, (0, 0, 0))

    screen.blit(text1, (settings.screen_width // 2 + 60, 120))
    screen.blit(win_text, (settings.screen_width // 2 + 60, 150))
    screen.blit(text2, (settings.screen_width // 2 + 80, 200))
    screen.blit(remind_text, (settings.screen_width // 2 + 90, 240))
    screen.blit(shuffle_text, (settings.screen_width // 2 + 90, 320))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def add_time(seconds):
    global start_ticks, last_update_time, paused_time
    current_ticks = pygame.time.get_ticks()
    start_ticks -= seconds * 1000  # 减少起始时间来增加游戏时间
    if paused:
        paused_time -= seconds * 1000
    last_update_time = current_ticks

def use_bomb():
    global map_list, image_list
    points = find_pair_to_clear()
    if points:
        handle_button_click(image_list, points)

def main():
    global screen, score, paused, start_ticks, last_update_time, play, map_list, image_list, paused_time, remind_count, shuffle_count
    pygame.init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption(settings.title)
    font = pygame.font.SysFont('SimHei', 24)
    game_over_font = pygame.font.SysFont('SimHei', 48)  # 增大字体大小
    total_time = 60.0  # 总时间（秒）

    paused = False
    paused_time = 0  # 初始化暂停时间
    score = 0  # 初始化分数
    play = True
    game_over = False
    remind_count = 0
    shuffle_count = 0

    reset_game()

    # 定义按钮
    pause_button = ImageBtn(screen, './image/18.png', 10, 40, 0, 'pause', (80, 50), buffer=30)
    remind_button = ImageBtn(screen, './image/16.png', 100, 40, 0, 'remind', (90, 50), buffer=30)
    shuffle_button = ImageBtn(screen, './image/17.png', 190, 40, 2, 'restart', (80, 50), buffer=30)
    quit_button = ImageBtn(screen, './image/15.png', 280, 40, 1, 'quit', (80, 50), buffer=30)
    home_button = ImageBtn(screen, './image/19.png', 460, 5, 3, 'home', (40, 40), buffer=30)
    restart_button = ImageBtn(screen, './image/20.png', 460, 45, 3, 'home', (45, 45), buffer=30)
    bomb_button = ImageBtn(screen, './image/bomb.png', 370, 40, 4, 'bomb', (50, 50), buffer=30)
    clock_button = ImageBtn(screen, './image/clock.png', 420, 48, 5, 'clock', (40, 40), buffer=30)
    running = True  # 添加运行标志

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # 设置运行标志为 False
                break  # 跳出事件循环
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if 2 < mouse_pos[0] < 92 and 35 < mouse_pos[1] < 92:
                    paused = not paused
                    if paused:
                        paused_start_ticks = pygame.time.get_ticks()
                    else:
                        paused_end_ticks = pygame.time.get_ticks()
                        paused_time += paused_end_ticks - paused_start_ticks
                    print("暂停按钮已被点击")
                elif 100 < mouse_pos[0] < 185 and 35 < mouse_pos[1] < 92:
                    print("提示按钮已被点击")
                    remind_count += 1  # 增加提示次数
                    points = find_pair_to_clear()
                    if points:
                        pygame.draw.line(screen, (255, 0, 0), points[0].get_center(), points[1].get_center(), 5)
                        pygame.display.update()
                        pygame.time.wait(300)
                        handle_button_click(image_list, points)
                elif 195 < mouse_pos[0] < 270 and 35 < mouse_pos[1] < 92:
                    print("洗牌按钮已被点击")
                    shuffle_game()
                    shuffle_count += 1  # 增加洗牌次数
                elif 280 < mouse_pos[0] < 355 and 35 < mouse_pos[1] < 92:
                    print("退出按钮已被点击")
                    running = False  # 设置运行标志为 False
                    break  # 跳出事件循环
                elif 470 < mouse_pos[0] < 580 and 5 < mouse_pos[1] < 45:
                    print("主页按钮已被点击")
                    pygame.quit()  # 退出当前Pygame窗口
                    subprocess.Popen(["python", "UI.py"])  # 重新打开UI窗口
                    return  # 确保不再执行Pygame相关操作
                elif 470 < mouse_pos[0] < 580 and 50 < mouse_pos[1] < 80:
                    print("重新开始按钮已被点击")
                    reset_game()
                elif 370 < mouse_pos[0] < 430 and 35 < mouse_pos[1] < 92:
                    print("炸弹按钮已被点击")
                    use_bomb()  # 使用炸弹道具
                elif 420 < mouse_pos[0] < 460 and 35 < mouse_pos[1] < 92:
                    print("时钟按钮已被点击")
                    add_time(-10)  # 增加30秒游戏时间
                else:
                    for btn in image_list:
                        geo = btn.get_geometry()
                        x = geo[0]
                        y = geo[1]
                        w = geo[2]
                        h = geo[3]
                        if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
                            if btn.is_checkable():
                                if not btn.click():
                                    settings.points.clear()
                                    break
                                if settings.points:
                                    settings.points.append(btn)
                                    if can_clear(settings.points):
                                        pygame.draw.line(screen, (255, 0, 0), settings.points[0].get_center(), settings.points[1].get_center(), 5)
                                        pygame.display.update()
                                        pygame.time.wait(100)
                                        for point in settings.points:
                                            map_list[point.number] = 0
                                            point.number = 0
                                            point.hide()
                                    else:
                                        for point in settings.points:
                                            point.reset()
                                    settings.points.clear()
                                else:
                                    settings.points.append(btn)
                            else:
                                settings.points = []

        if not running:  # 检查运行标志
            break  # 跳出主循环

        screen.fill((255, 255, 255))

        # 绘制网格背景
        for i in range(settings.game_row):
            for j in range(settings.game_col):
                rect = pygame.Rect(j * settings.grid_size, i * settings.grid_size + 100, settings.grid_size, settings.grid_size)
                pygame.draw.rect(screen, LIGHT_BLUE, rect, 1)

        pause_button.display()
        remind_button.display()
        shuffle_button.display()
        quit_button.display()
        home_button.display()
        restart_button.display()
        bomb_button.display()
        clock_button.display()

        if play:
            if not paused:
                current_ticks = pygame.time.get_ticks()
                seconds = (current_ticks - start_ticks - paused_time) / 1000
                last_update_time = current_ticks
            else:
                seconds = (last_update_time - start_ticks - paused_time) / 1000

            seconds_left = total_time - seconds
            timer_surface2 = font.render('剩余时间:' + str(int(seconds_left)), True, (0, 0, 0))
            timer_surface3 = font.render('游戏道具',True, (0, 0, 0))
            screen.blit(timer_surface3, (360, 10))
            screen.blit(timer_surface2, (10, 10))
            if seconds_left <= 0:
                play = False
                game_over = True
            if is_over():
                print("通关时间：", seconds, "秒")
                print("提示次数：", remind_count)
                print("洗牌次数：", shuffle_count)
                display_win_screen(screen, seconds, remind_count, shuffle_count)
            else:
                for im in image_list:
                    im.display()
        else:
            if game_over:
                screen.fill(WHITE, (0, 100, settings.screen_width, settings.screen_height - 100))
                game_over_surface = game_over_font.render('游戏失败', True, (255, 0, 0))
                screen.blit(game_over_surface, (200, 150))
                d_surface = font.render('请点击重开按钮重新开始', True, (0, 0, 0))
                screen.blit(d_surface, (160, 200))
                e_surface = font.render('或点击主页按钮更改难度', True, (0, 0, 0))
                screen.blit(e_surface, (160, 230))

        if paused:
            paused_surface = font.render('游戏暂停', True, (255, 0, 0))
            screen.blit(paused_surface, (150, 90))
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
