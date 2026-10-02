import sys  # 导入sys模块，用于访问与Python解释器相关的变量和函数
import math  # 导入math模块，提供数学运算函数
import random  # 导入random模块，用于生成随机数
import pygame  # 导入pygame模块，用于创建视频游戏
import subprocess  # 导入subprocess模块，用于创建新的进程，连接到它们的输入/输出/错误管道，并获取它们的返回码

# 定义颜色常量
WHITE = (255, 255, 255)  # 白色
GRAY = (128, 128, 128)  # 灰色
LIGHT_BLUE = (173, 216, 230)  # 浅蓝色

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

settings = Settings()  # 创建一个Settings对象
map_list = []  # 图像列表映射
image_list = []  # 图像列表
button_size = (50, 50)  # 定义统一的按钮大小

# 图像按钮类
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
        self.checked = False  # 按钮的选中状态

    def display(self):  # 显示按钮
        if self.checked:  # 如果按钮被选中
            pygame.draw.rect(self.image, (0, 205, 205, 255),
                             (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 2)
        else:  # 如果按钮未被选中
            pygame.draw.rect(self.image, (0, 205, 205, 0),
                             (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 2)
        self.screen.blit(self.image, (self.x, self.y))  # 将图像绘制到屏幕上

    def hide(self):  # 隐藏按钮
        self.checked = False  # 取消选中状态
        self.image.fill((255, 255, 240))  # 用指定颜色填充图像

    def is_checkable(self):  # 检查按钮是否可选中
        return True

    def click(self):  # 点击按钮
        self.checked = not self.checked  # 切换选中状态
        return self.checked

    def reset(self):  # 重置按钮
        self.checked = False  # 取消选中状态

    def get_geometry(self):  # 获取按钮的几何属性
        return self.x, self.y, self.w, self.h

    def get_center(self):  # 获取按钮的中心坐标
        return self.x + self.w / 2, self.y + self.h / 2

# 水平扫描函数
def horizontal_scan(points):
    column = settings.game_col  # 游戏列数
    p1_x = int(points[0].number % column)  # 第一个点的x坐标
    p1_y = int(points[0].number / column)  # 第一个点的y坐标
    p2_x = int(points[1].number % column)  # 第二个点的x坐标
    p2_y = int(points[1].number / column)  # 第二个点的y坐标

    if p1_y == p2_y:  # 如果两点在同一行
        return False

    hLine1 = min(p1_y, p2_y)  # 最小的行数
    hLine2 = max(p1_y, p2_y)  # 最大的行数
    leftLimit = 0  # 左边界
    rightLimit = column - 1  # 右边界

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
    return False  # 如果不能通过水平扫描连接两点，返回False

# 垂直扫描函数
def vertical_scan(points):
    row = settings.game_row  # 游戏行数
    column = settings.game_col  # 游戏列数
    p1_x = int(points[0].number % column)  # 第一个点的x坐标
    p1_y = int(points[0].number / column)  # 第一个点的y坐标
    p2_x = int(points[1].number % column)  # 第二个点的x坐标
    p2_y = int(points[1].number / column)  # 第二个点的y坐标

    if p1_x == p2_x:  # 如果两点在同一列
        return False

    vLine1 = min(p1_x, p2_x)  # 最小的列数
    vLine2 = max(p1_x, p2_x)  # 最大的列数
    topLimit = 0  # 上边界
    bottomLimit = row - 1  # 下边界

    # 以下是一些复杂的逻辑判断，用于确定上下边界和是否可以通过垂直扫描连接两点
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
    return False  # 如果不能通过垂直扫描连接两点，返回False

# 判断两点是否可以清除
def can_clear(points):
    if points[0].element != points[1].element:  # 如果两点的元素不同
        return False  # 返回False
    else:  # 否则
        if vertical_scan(points) or horizontal_scan(points):  # 如果两点可以通过垂直扫描或水平扫描连接
            return True  # 返回True
        else:  # 否则
            return False  # 返回False

# 处理按钮点击事件
def handle_button_click(btns, click_list):
    global score  # 声明score为全局变量
    score += 10  # 分数增加10
    click_list[0].hide()  # 隐藏第一个被点击的按钮
    click_list[1].hide()  # 隐藏第二个被点击的按钮

    index1 = click_list[0].number  # 获取第一个被点击的按钮的编号
    index2 = click_list[1].number  # 获取第二个被点击的按钮的编号
    click_list = []  # 清空点击列表
    map_list[index1] = 0  # 将地图列表中对应的位置设置为0
    map_list[index2] = 0  # 将地图列表中对应的位置设置为0
    return click_list  # 返回点击列表

# 构建地图
def build_map():
    t_list = []  # 临时列表
    m_list = []  # 地图列表
    for i in range(0, settings.map_total, 2):  # 对于每个网格
        e = math.ceil(random.random() * settings.element_num)  # 生成一个随机的元素
        t_list.append(e)  # 将元素添加到临时列表
        t_list.append(e)  # 将元素添加到临时列表

    for i in range(0, settings.map_total):  # 对于每个网格
        index = int(random.random() * (settings.map_total - i))  # 生成一个随机的索引
        m_list.append(t_list[index])  # 将临时列表中对应的元素添加到地图列表
        t_list.pop(index)  # 从临时列表中删除该元素
    return m_list  # 返回地图列表

# 判断游戏是否结束
def is_over():
    for each in map_list:  # 对于地图列表中的每个元素
        if each > 0:  # 如果元素大于0
            return False  # 返回False
    return True  # 否则，返回True

# 定义一个函数，用于按数字排序文件中的行
def sort_file_by_numbers(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # 打开文件进行读取
        lines = file.readlines()  # 读取文件中的所有行
        lines.sort(key=lambda x: float(x.strip()))  # 对行进行排序，排序的关键字是将每行转换为浮点数
    with open(filename, 'w', encoding='utf-8') as file:  # 打开文件进行写入
        file.writelines(lines)  # 将排序后的行写入文件

# 声明全局变量screen
global screen
# 定义一个函数，用于重置游戏
def reset_game():
    global map_list, image_list, play, paused, start_ticks, last_update_time, remind_count, shuffle_count, paused_time
    # 以下是一些游戏状态的初始化操作
    map_list = build_map()
    image_list = []
    for i in range(0, settings.map_total):
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

# 定义一个函数，用于洗牌游戏
def shuffle_game():
    global map_list, image_list
    # 以下是一些洗牌的操作
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
        x = int(i % settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[0]) / 2
        y = int(i / settings.game_col) * settings.grid_size + (settings.grid_size - settings.scale_size[1]) / 2 + 100
        if map_list[i] != 0:
            element = './image/' + str(map_list[i]) + '.png'
            image_list.append(ImageBtn(screen, element, x, y, i, map_list[i], settings.scale_size))
    print("洗牌已完成")

# 定义一个函数，用于找到可以清除的配对
def find_pair_to_clear():
    for i in range(len(image_list)):
        for j in range(i + 1, len(image_list)):
            if map_list[image_list[i].number] != 0 and map_list[image_list[j].number] != 0:
                points = [image_list[i], image_list[j]]
                if points[0].element == points[1].element and can_clear(points):
                    return points
    return None

# 定义一个函数，用于显示胜利的屏幕
def display_win_screen(screen, seconds, remind_count, shuffle_count):
    font = pygame.font.SysFont('SimHei', 24)  # 定义字体
    youwin = pygame.image.load(settings.win_image)  # 加载胜利的图片
    youwin = pygame.transform.scale(youwin, (settings.screen_width, settings.screen_height))  # 缩放图片
    screen.blit(youwin, (0, 0))  # 将图片绘制到屏幕上

    # 以下是一些绘制文字的操作
    # 调整文字的位置
    text1 = font.render(f'通关时间:', True, (0, 0, 0))
    win_text = font.render(f'{seconds:.2f} 秒', True, (0, 0, 0))
    text2 = font.render(f'次数: ', True, (0, 0, 0))
    remind_text = font.render(f' {remind_count}', True, (0, 0, 0))
    shuffle_text = font.render(f' {shuffle_count}', True, (0, 0, 0))

    screen.blit(text1, (settings.screen_width // 2 + 100, 170))
    screen.blit(win_text, (settings.screen_width // 2 + 100, 200))
    screen.blit(text2, (settings.screen_width // 2 + 150, 270))
    screen.blit(remind_text, (settings.screen_width // 2 + 150, 340))
    screen.blit(shuffle_text, (settings.screen_width // 2 + 150, 460))

    pygame.display.update()  # 更新屏幕显示

    waiting = True
    while waiting:  # 等待用户的输入
        for event in pygame.event.get():  # 获取所有的事件
            if event.type == pygame.QUIT:  # 如果事件类型是退出
                pygame.quit()  # 退出pygame
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件类型是按下键盘或鼠标按钮
                waiting = False  # 结束等待


# 定义主函数
def main():
    global screen, score, paused, start_ticks, last_update_time, play, map_list, image_list, paused_time, remind_count, shuffle_count
    # 声明一些全局变量

    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode(settings.screen_size)  # 设置游戏窗口的大小
    pygame.display.set_caption(settings.title)  # 设置游戏窗口的标题
    font = pygame.font.SysFont('SimHei', 24)  # 设置字体和字号
    game_over_font = pygame.font.SysFont('SimHei', 48)  # 设置游戏结束时的字体和字号
    total_time = 60.0  # 设置游戏的总时间

    # 初始化一些游戏状态
    paused = False
    paused_time = 0
    score = 0
    play = True
    game_over = False
    remind_count = 0
    shuffle_count = 0

    reset_game()  # 调用reset_game函数重置游戏

    # 定义一些按钮，并设置它们的图片、位置、大小等属性
    pause_button = ImageBtn(screen, './image/18.png', 10, 40, 0, 'pause', (80, 50), buffer=30)
    remind_button = ImageBtn(screen, './image/16.png', 100, 40, 0, 'remind', (90, 50), buffer=30)
    shuffle_button = ImageBtn(screen, './image/17.png', 190, 40, 2, 'restart', (80, 50), buffer=30)
    quit_button = ImageBtn(screen, './image/15.png', 280, 40, 1, 'quit', (80, 50), buffer=30)
    home_button = ImageBtn(screen, './image/19.png', 360, 5, 3, 'home', (40, 40), buffer=30)
    restart_button = ImageBtn(screen, './image/20.png', 360, 45, 3, 'home', (45, 45), buffer=30)

    running = True  # 设置游戏的运行标志为True

    while running:  # 当游戏正在运行时
        for event in pygame.event.get():  # 获取所有的事件
            if event.type == pygame.QUIT:  # 如果事件类型是退出
                running = False  # 设置运行标志为 False
                break  # 跳出事件循环
            if event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件类型是鼠标按下
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标的位置
                print(mouse_pos)  # 打印鼠标的位置
                # 以下是一些判断鼠标点击位置的操作，用于判断用户点击了哪个按钮
                # 如果用户点击了暂停按钮
                if 2 < mouse_pos[0] < 92 and 35 < mouse_pos[1] < 92:
                    paused = not paused  # 切换暂停状态
                    if paused:  # 如果游戏被暂停
                        paused_start_ticks = pygame.time.get_ticks()  # 记录暂停开始的时间
                    else:  # 如果游戏被恢复
                        paused_end_ticks = pygame.time.get_ticks()  # 记录暂停结束的时间
                        paused_time += paused_end_ticks - paused_start_ticks  # 计算暂停的总时间
                    print("暂停按钮已被点击")
                # 如果用户点击了提示按钮
                elif 100 < mouse_pos[0] < 185 and 35 < mouse_pos[1] < 92:
                    print("提示按钮已被点击")
                    remind_count += 1  # 增加提示次数
                    points = find_pair_to_clear()  # 找到可以清除的配对
                    if points:  # 如果找到了配对
                        pygame.draw.line(screen, (255, 0, 0), points[0].get_center(), points[1].get_center(),
                                         5)  # 在屏幕上画一条连接两个点的线
                        pygame.display.update()  # 更新屏幕显示
                        pygame.time.wait(300)  # 等待300毫秒
                        handle_button_click(image_list, points)  # 处理按钮点击事件
                # 如果用户点击了洗牌按钮
                elif 195 < mouse_pos[0] < 270 and 35 < mouse_pos[1] < 92:
                    print("洗牌按钮已被点击")
                    shuffle_game()  # 洗牌
                    shuffle_count += 1  # 增加洗牌次数
                # 如果用户点击了退出按钮
                elif 280 < mouse_pos[0] < 355 and 35 < mouse_pos[1] < 92:
                    print("退出按钮已被点击")
                    running = False  # 设置运行标志为 False
                    break  # 跳出事件循环
                # 如果用户点击了主页按钮
                elif 360 < mouse_pos[0] < 400 and 5 < mouse_pos[1] < 45:
                    print("主页按钮已被点击")
                    pygame.quit()  # 退出当前Pygame窗口
                    subprocess.Popen(["python", "UI.py"])  # 重新打开UI窗口
                    return  # 确保不再执行Pygame相关操作
                # 如果用户点击了重新开始按钮
                elif 360 < mouse_pos[0] < 400 and 50 < mouse_pos[1] < 80:
                    print("重新开始按钮已被点击")
                    reset_game()  # 重置游戏
                else:  # 如果用户点击了其他位置
                    for btn in image_list:  # 对于图像列表中的每个按钮
                        geo = btn.get_geometry()  # 获取按钮的几何属性
                        x = geo[0]
                        y = geo[1]
                        w = geo[2]
                        h = geo[3]
                        if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:  # 如果鼠标点击的位置在按钮的范围内
                            if btn.is_checkable():  # 如果按钮可以被选中
                                if not btn.click():  # 如果按钮被点击
                                    settings.points.clear()  # 清空点的列表
                                    break
                                if settings.points:  # 如果点的列表不为空
                                    settings.points.append(btn)  # 将按钮添加到点的列表
                                    if can_clear(settings.points):  # 如果点的列表中的点可以被清除
                                        pygame.draw.line(screen, (255, 0, 0), settings.points[0].get_center(),
                                                         settings.points[1].get_center(), 5)  # 在屏幕上画一条连接两个点的线
                                        pygame.display.update()  # 更新屏幕显示
                                        pygame.time.wait(100)  # 等待100毫秒
                                        for point in settings.points:  # 对于点的列表中的每个点
                                            map_list[point.number] = 0  # 将地图列表中对应的位置设置为0
                                            point.number = 0  # 将点的编号设置为0
                                            point.hide()  # 隐藏点
                                    else:  # 如果点的列表中的点不能被清除
                                        for point in settings.points:  # 对于点的列表中的每个点
                                            point.reset()  # 重置点
                                    settings.points.clear()  # 清空点的列表
                                else:  # 如果点的列表为空
                                    settings.points.append(btn)  # 将按钮添加到点的列表
                            else:  # 如果按钮不能被选中
                                settings.points = []  # 清空点的列表

        if not running:  # 如果游戏不再运行
            break  # 跳出主循环

        screen.fill((255, 255, 255))  # 将屏幕填充为白色

        # 绘制网格背景
        for i in range(settings.game_row):
            for j in range(settings.game_col):
                rect = pygame.Rect(j * settings.grid_size, i * settings.grid_size + 100, settings.grid_size,
                                   settings.grid_size)
                pygame.draw.rect(screen, LIGHT_BLUE, rect, 1)

        # 显示各个按钮
        pause_button.display()
        remind_button.display()
        shuffle_button.display()
        quit_button.display()
        home_button.display()
        restart_button.display()

        # 如果游戏正在进行
        if play:
            # 如果游戏没有被暂停
            if not paused:
                current_ticks = pygame.time.get_ticks()  # 获取当前的时间
                seconds = (current_ticks - start_ticks - paused_time) / 1000  # 计算游戏已经进行的时间
                last_update_time = current_ticks  # 更新最后更新时间
            else:  # 如果游戏被暂停
                seconds = (last_update_time - start_ticks - paused_time) / 1000  # 计算游戏已经进行的时间

            # 显示计时器
            timer_surface1 = font.render('计时器:' + str(seconds), True, (0, 0, 0))
            screen.blit(timer_surface1, (200, 10))
            seconds_left = total_time - seconds  # 计算剩余时间
            timer_surface2 = font.render('剩余时间:' + str(int(seconds_left)), True, (0, 0, 0))
            screen.blit(timer_surface2, (10, 10))

            # 如果剩余时间小于等于0，游戏结束
            if seconds_left <= 0:
                play = False
                game_over = True

            # 如果游戏已经结束
            if is_over():
                # 打印通关时间、提示次数和洗牌次数
                print("通关时间：", seconds, "秒")
                print("提示次数：", remind_count)
                print("洗牌次数：", shuffle_count)

                # 将通关时间写入文件
                with open('困难排行榜.txt', 'a') as f:
                    f.write(str(seconds) + '\n')

                # 对文件中的时间进行排序
                sort_file_by_numbers("困难排行榜.txt")

                # 游戏停止
                play = False

                # 显示胜利的屏幕
                display_win_screen(screen, seconds, remind_count, shuffle_count)
            else:  # 如果游戏没有结束
                for im in image_list:  # 对于图像列表中的每个图像
                    im.display()  # 显示图像
        else:  # 如果游戏没有进行
            if game_over:  # 如果游戏结束
                # 显示游戏失败的屏幕
                screen.fill(WHITE, (0, 100, settings.screen_width, settings.screen_height - 100))
                game_over_surface = game_over_font.render('游戏失败', True, (255, 0, 0))
                screen.blit(game_over_surface, (200, 150))
                d_surface = font.render('请点击重开按钮重新开始', True, (0, 0, 0))
                screen.blit(d_surface, (160, 200))
                e_surface = font.render('或点击主页按钮更改难度', True, (0, 0, 0))
                screen.blit(e_surface, (160, 230))

        # 如果游戏被暂停
        if paused:
            paused_surface = font.render('游戏暂停', True, (255, 0, 0))
            screen.blit(paused_surface, (150, 90))

        pygame.display.update()  # 更新屏幕显示

    pygame.quit()  # 退出pygame
    sys.exit()  # 退出系统

if __name__ == "__main__":
    main()  # 调用主函数

