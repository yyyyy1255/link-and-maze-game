import math
import turtle as t
import random
import subprocess
from PIL import Image
import time
from collections import deque  # 用于广度优先搜索（BFS）


# 全局变量
score = 0  # 分数初始化为0
current_level = 1  # 当前等级初始化为1
time_left = 60  # 倒计时时间，单位为秒
paused = False  # 添加暂停变量
timer_id = None  # 添加全局定时器ID变量
start_time = None  # 游戏开始时间初始化为None
health = 3  # 初始血量为3
ai_active = False  # AI是否激活
ai_timer_active = False  # AI定时器是否激活
hint_displayed = False  # 添加提示显示状态变量
fog_mode = False  # 迷雾模式状态
torch_active = False  # 火把效果是否激活
ai_button = None  # AI按钮
hint_button = None  # 提示按钮
ai_enabled = False  # AI按钮是否启用状态
hint_enabled = False  # 提示按钮是否启用状态

# 初始化全局变量
screen_width = 760  # 屏幕宽度
screen_height = 760  # 屏幕高度

walls = []  # 墙壁列表
golds = []  # 金币列表
enemies = []  # 敌人列表
torches = [] # 火把列表
end_pos = ()  # 终点位置
message_turtle = None  # 消息乌龟对象


def resize_image(image_path, size):
    """
    调整图片大小的函数
    :param image_path: 图片路径
    :param size: 新的大小
    """
    img = Image.open(image_path)  # 打开图片
    img = img.resize(size, Image.LANCZOS)  # 调整图片大小
    img.save(image_path)  # 保存调整后的图片


def run_maze_game(ui_width, ui_height):
    global score, current_level, time_left, end_pos, paused, timer_id, message_turtle, walls, golds, enemies, start_time, health, width, height, width0, height0, hint_displayed, screen_width, screen_height, fog_mode, ai_button, hint_button, ai_enabled, hint_enabled

    # 根据用户输入初始化游戏窗口的尺寸
    width0 = ui_width
    height0 = ui_height
    width = ui_width
    height = ui_height

    # 初始化游戏变量
    score = 0  # 初始化得分
    current_level = 1
    time_left = 60  # 每次游戏开始时重置倒计时
    health = 3  # 每次游戏开始时重置血量

    start_time = time.time()  # 记录开始时间

    # 调整按钮图片大小
    resize_image('pause_button.gif', (48, 48))
    resize_image('restart_button.gif', (48, 48))
    resize_image('redraw_button.gif', (48, 48))
    resize_image('exit_button.gif', (48, 48))
    resize_image('home_button.gif', (48, 48))
    resize_image('ai_button.gif', (48, 48))
    resize_image('hint_button.gif', (48, 48))  # 提示按钮图片大小
    resize_image('next_level_button.gif', (48, 48))  # 下一层按钮图片大小
    resize_image('fog_button.gif', (48, 48))  # 迷雾按钮图片大小
    resize_image('torch.gif', (48, 48))# 火把图片大小

    # 初始化屏幕
    mz = t.Screen()
    mz.setup(screen_width, screen_height)
    mz.bgcolor('black')
    mz.title('迷宫小游戏')
    mz.register_shape('wall.gif')
    mz.register_shape('pr.gif')
    mz.register_shape('pl.gif')
    mz.register_shape('e.gif')
    mz.register_shape('gold.gif')
    mz.register_shape('end.gif')  # 终点形状
    mz.register_shape('pause_button.gif')  # 暂停按钮形状
    mz.register_shape('restart_button.gif')  # 重启按钮形状
    mz.register_shape('redraw_button.gif')  # 重绘按钮形状
    mz.register_shape('exit_button.gif')  # 退出按钮形状
    mz.register_shape('home_button.gif')  # 主页按钮形状
    mz.register_shape('ai_button.gif')  # AI按钮形状
    mz.register_shape('hint_button.gif')  # 提示按钮形状
    mz.register_shape('next_level_button.gif')  # 下一层按钮形状
    mz.register_shape('fog_button.gif')  # 迷雾按钮形状
    mz.register_shape('torch.gif')  # 火把按钮形状
    mz.tracer(0)

    # 显示倒计时的Turtle
    timer_turtle = t.Turtle()
    timer_turtle.hideturtle()
    timer_turtle.penup()
    timer_turtle.goto(0, screen_height // 2 - 40)
    timer_turtle.color('white')
    timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))

    # 显示得分的Turtle
    score_turtle = t.Turtle()
    score_turtle.hideturtle()
    score_turtle.penup()
    score_turtle.goto(screen_width // 2 - 85, screen_height // 2 - 40)
    score_turtle.color('white')
    score_turtle.write(f"当前得分: {score}", align='center', font=('Arial', 20, 'bold'))

    # 显示血量的Turtle
    health_turtle = t.Turtle()
    health_turtle.hideturtle()
    health_turtle.penup()
    health_turtle.goto(-screen_width // 2 + 60, screen_height // 2 - 40)
    health_turtle.color('white')
    health_turtle.write(f"血量: {health}", align='center', font=('Arial', 20, 'bold'))

    # 用来显示消息的Turtle
    message_turtle = t.Turtle()
    message_turtle.hideturtle()
    message_turtle.penup()
    message_turtle.goto(0, screen_height // 2 - 60)  # 将文字置于倒计时下方
    message_turtle.color('yellow')

    # 用来显示提示路径的Turtle
    hint_turtle = t.Turtle()
    hint_turtle.hideturtle()
    hint_turtle.penup()
    hint_turtle.color('yellow')

    # 迷雾覆盖层
    fog_turtle = t.Turtle()
    fog_turtle.hideturtle()
    fog_turtle.penup()
    fog_turtle.color('black')

    # 更新倒计时的函数
    def update_timer():
        global time_left, paused, timer_id, start_time
        if not paused and time_left > 0:
            time_left -= 1  # 每次调用减去1秒
            timer_turtle.clear()
            timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))
            timer_id = mz.ontimer(update_timer, 1000)  # 每秒更新一次
        elif time_left <= 0:
            game_over()  # 如果时间用完，调用游戏结束函数

    def generate_maze(width, height):
        # 生成一个宽度为width，高度为height的迷宫
        maze = [['X'] * width for _ in range(height)]  # 创建一个全是'X'的矩阵表示迷宫
        start_x, start_y = 1, 1  # 起点坐标
        maze[start_y][start_x] = ' '  # 将起点设为空格
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # 定义四个方向

        def dfs(x, y):
            # 深度优先搜索算法生成迷宫
            random.shuffle(directions)  # 随机打乱方向
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 'X':
                    maze[ny][nx] = ' '  # 设置新位置为空格
                    maze[ny - dy // 2][nx - dx // 2] = ' '  # 打通墙壁
                    dfs(nx, ny)  # 递归调用

        dfs(start_x, start_y)  # 从起点开始生成迷宫

        maze[start_y][start_x] = 'P'  # 设置玩家起始位置
        maze[height - 2][width - 2] = 'E'  # 设置终点位置

        # 确保终点位置可达
        if maze[height - 2][width - 3] == 'X' and maze[height - 3][width - 2] == 'X':
            if width > 3:
                maze[height - 2][width - 3] = ' '  # 打通一面墙
            elif height > 3:
                maze[height - 3][width - 2] = ' '  # 打通另一面墙
        # 随机放置金币
        for _ in range(int(math.sqrt(width*height)/5)):
            while True:
                gx, gy = random.randint(1, width - 2), random.randint(1, height - 2)
                if maze[gy][gx] == ' ':
                    maze[gy][gx] = 'G'
                    break

        # 随机放置敌人
        for _ in range(int(math.sqrt(width*height)/5)):
            while True:
                mx, my = random.randint(1, width - 2), random.randint(1, height - 2)
                if maze[my][mx] == ' ':
                    maze[my][mx] = 'M'
                    break

        # 随机放置火把
        for _ in range(int(math.sqrt(width*height)/5)):
            while True:
                tx, ty = random.randint(1, width - 2), random.randint(1, height - 2)
                if maze[ty][tx] == ' ':
                    maze[ty][tx] = 'T'
                    break

        return maze  # 返回生成的迷宫

    generated_maze = generate_maze(width, height)  # 生成一个迷宫
    levels = [generated_maze]  # 将生成的迷宫存储在levels列表中

    class Enemy(t.Turtle):
        def __init__(self):
            super().__init__()
            self.ht()  # 隐藏乌龟图形
            self.shape('e.gif')  # 设置敌人的形状
            self.speed(0)  # 设置速度为最快
            self.penup()  # 提起笔以避免绘图
            self.fx = random.choice(['U', 'D', 'R', 'L'])  # 随机选择一个初始方向
            self.timer_id = None

        def move(self):
            if not self.isvisible() or paused:
                return  # 如果敌人不可见或游戏暂停，则不移动
            self.turn()  # 转向
            go_x, go_y = self.xcor(), self.ycor()
            if self.fx == 'U':
                go_y += 24  # 向上移动
            elif self.fx == 'D':
                go_y -= 24  # 向下移动
            elif self.fx == 'R':
                go_x += 24  # 向右移动
            elif self.fx == 'L':
                go_x -= 24  # 向左移动
            if (go_x, go_y) not in walls:  # 如果目标位置不是墙
                self.goto(go_x, go_y)  # 移动到新位置
                if self.distance(player) < 24:
                    self.attack_player()  # 如果靠近玩家，攻击玩家
            self.timer_id = t.ontimer(self.move, random.randint(100, 300))  # 随机时间后再次调用move函数

        def turn(self):
            if self.distance(player) < 48:  # 如果敌人距离玩家很近
                if self.xcor() < player.xcor():
                    self.fx = 'R'  # 向右转
                elif self.xcor() > player.xcor():
                    self.fx = 'L'  # 向左转
                elif self.ycor() > player.ycor():
                    self.fx = 'D'  # 向下转
                elif self.ycor() < player.ycor():
                    self.fx = 'U'  # 向上转
            else:
                self.fx = random.choice(['U', 'D', 'R', 'L'])  # 随机选择一个方向

        def attack_player(self):
            global health
            health -= 1  # 减少玩家的血量
            health_turtle.clear()
            health_turtle.write(f"血量: {health}", align='center', font=('Arial', 20, 'bold'))
            if health <= 0:
                game_over()  # 如果血量为0，游戏结束
            else:
                self.stamp()  # 标记当前位置
                self.goto(-1000, -1000)  # 移动敌人到远处

    class Gold(t.Turtle):
        def __init__(self):
            super().__init__()
            self.ht()  # 隐藏乌龟图形
            self.shape('gold.gif')  # 设置金块的形状
            self.speed(0)  # 设置速度为最快
            self.penup()  # 提起笔以避免绘图

    class End(t.Turtle):
        def __init__(self):
            super().__init__()
            self.ht()  # 隐藏乌龟图形
            self.shape('end.gif')  # 设置终点的形状
            self.speed(0)  # 设置速度为最快
            self.penup()  # 提起笔以避免绘图

    class Torch(t.Turtle):
        def __init__(self):
            super().__init__()
            self.ht()  # 隐藏乌龟图形
            self.shape('torch.gif')  # 设置火把的形状为图片文件 'torch.gif'
            self.speed(0)  # 设置速度为最快
            self.penup()  # 提起笔以避免绘图

    class Player(t.Turtle):
        def __init__(self):
            super().__init__()
            self.ht()  # 隐藏乌龟图形
            self.shape('pr.gif')  # 设置玩家的初始形状
            self.speed(0)  # 设置速度为最快
            self.penup()  # 提起笔以避免绘图

        def go_right(self):
            if not paused:
                go_x = self.xcor() + 24  # 计算向右移动后的新x坐标
                go_y = self.ycor()  # y坐标保持不变
                self.shape('pr.gif')  # 设置形状为向右
                self.move(go_x, go_y)  # 移动玩家

        def go_left(self):
            if not paused:
                go_x = self.xcor() - 24  # 计算向左移动后的新x坐标
                go_y = self.ycor()  # y坐标保持不变
                self.shape('pl.gif')  # 设置形状为向左
                self.move(go_x, go_y)  # 移动玩家

        def go_up(self):
            if not paused:
                go_x = self.xcor()  # x坐标保持不变
                go_y = self.ycor() + 24  # 计算向上移动后的新y坐标
                self.move(go_x, go_y)  # 移动玩家

        def go_down(self):
            if not paused:
                go_x = self.xcor()  # x坐标保持不变
                go_y = self.ycor() - 24  # 计算向下移动后的新y坐标
                self.move(go_x, go_y)  # 移动玩家

        def move(self, go_x, go_y):
            if (go_x, go_y) not in walls:  # 如果目标位置不是墙
                self.goto(go_x, go_y)  # 移动到新位置
                self.look_for_gold(go_x, go_y)  # 检查是否有金币
                self.check_for_end(go_x, go_y)  # 检查是否到达终点
                self.look_for_torch(go_x, go_y)  # 检查是否有火把
                if fog_mode:
                    update_fog()
            else:
                print('哎呀，撞到墙了')  # 如果撞到墙，打印信息

        def clear_auto_move(self):
            global ai_timer_active
            ai_timer_active = False  # 停止自动移动

        def look_for_gold(self, go_x, go_y):
            global score, time_left
            for g in golds:
                if g.distance(player) == 0:  # 如果玩家与金币重合
                    score += 1  # 增加分数
                    time_left += 3  # 吃到金币增加3秒
                    score_turtle.clear()
                    score_turtle.write(f"当前得分: {score}", align='center', font=('Arial', 20, 'bold'))
                    timer_turtle.clear()
                    timer_turtle.write(f"时间剩余: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))
                    print(f"当前得分: {score}")
                    g.ht()  # 隐藏金币
                    golds.remove(g)  # 从金币列表中移除
                    self.show_message()  # 显示信息
                    check_all_gold_collected()  # 检查是否所有金币已被收集

        def look_for_torch(self, go_x, go_y):
            global fog_mode
            for t in torches:
                if t.distance(player) == 0:  # 如果玩家与火把重合
                    t.ht()  # 隐藏火把
                    torches.remove(t)  # 从火把列表中移除
                    self.activate_torch()  # 激活火把效果

        def activate_torch(self):
            global fog_mode, torch_active, paused
            if not fog_mode:  # 检查是否处于迷雾状态
                return  # 如果不是，则不进行任何操作
            torch_active = True
            fog_mode = False  # 驱散迷雾
            fog_turtle.clear()  # 清除迷雾覆盖层
            message_turtle.clear()
            message_turtle.color('yellow')  # 确保消息显示为黄色
            message_turtle.goto(0, screen_height // 2 - 65)  # 确保消息位置在倒计时下方
            message_turtle.write("捡到1个火把，迷雾驱散5秒", align='center', font=('Arial', 18, 'bold'))
            mz.ontimer(message_turtle.clear, 2000)  # 2秒后清除信息
            mz.ontimer(self.deactivate_torch, 5000)  # 5秒后恢复迷雾

        def deactivate_torch(self):
            global fog_mode, torch_active, paused
            if not torch_active:
                return  # 如果火把已经不活跃，不进行任何操作
            torch_active = False
            if not paused and fog_mode == False:  # 只有在非暂停状态下且当前为非迷雾状态才恢复迷雾
                fog_mode = True  # 恢复迷雾模式
                update_fog()  # 更新迷雾覆盖层

        def check_for_end(self, go_x, go_y):
            if (go_x, go_y) == end_pos:  # 如果玩家到达终点
                fog_turtle.clear()  # 清除迷雾
                success()  # 调用成功函数

        def show_message(self):
            message_turtle.clear()
            message_turtle.color('yellow')  # 确保消息显示为黄色
            message_turtle.goto(0, screen_height // 2 - 65)  # 确保消息位置在倒计时下方
            message_turtle.write("您已吃到一个金币，得分+1，剩余时间+3", align='center', font=('Arial', 18, 'bold'))
            mz.ontimer(message_turtle.clear, 2000)  # 2秒后清除信息

        def auto_move(self, path):
            if not path or not ai_active:
                return
            next_pos = path.pop(0)  # 取得路径中的下一个位置
            self.goto(next_pos)  # 移动到下一个位置
            self.look_for_gold(*next_pos)  # 检查是否有金币
            self.check_for_end(*next_pos)  # 检查是否到达终点
            if path and ai_active:
                mz.ontimer(lambda: self.auto_move(path), 100)  # 继续自动移动，每100毫秒更新一次

    # 定义一个名为 Pen 的类，继承自 Turtle
    class Pen(t.Turtle):
        # Pen 类的构造函数
        def __init__(self):
            super().__init__()  # 初始化父类 Turtle
            self.ht()  # 隐藏海龟（画笔）
            self.shape('wall.gif')  # 设置海龟的形状为图片文件 'wall.gif'
            self.speed(0)  # 将绘图速度设置为最快
            self.penup()  # 提起画笔，防止移动时绘制线条

        # 创建迷宫的方法，基于预定义的关卡布局
        def make_maze(self):
            global walls, golds, enemies, torches, end_pos  # 声明全局变量
            level = levels[current_level - 1]  # 获取当前关卡的布局
            for i in range(len(level)):  # 遍历关卡的每一行
                row = level[i]
                for j in range(len(row)):  # 遍历每一行的每一个字符
                    screen_x = -width * 12 + 24 * j  # 计算屏幕上的 x 坐标
                    screen_y = height * 12 - 24 * i  # 计算屏幕上的 y 坐标
                    char = row[j]  # 获取当前字符
                    if char == 'X':  # 如果字符是 'X'，表示墙
                        self.goto(screen_x, screen_y)  # 移动到对应坐标
                        self.stamp()  # 在该位置盖章
                        walls.append((screen_x, screen_y))  # 将墙的坐标加入列表
                    elif char == 'P':  # 如果字符是 'P'，表示玩家
                        player.goto(screen_x, screen_y)  # 将玩家移动到该位置
                        player.st()  # 显示玩家
                    elif char == 'G':  # 如果字符是 'G'，表示金块
                        gold = Gold()  # 创建一个金块对象
                        golds.append(gold)  # 将金块加入列表
                        gold.goto(screen_x, screen_y)  # 将金块移动到该位置
                        gold.st()  # 显示金块
                    elif char == 'E':  # 如果字符是 'E'，表示终点
                        end.goto(screen_x, screen_y)  # 将终点移动到该位置
                        end.st()  # 显示终点
                        end_pos = (screen_x, screen_y)  # 记录终点位置
                    elif char == 'M':  # 如果字符是 'M'，表示敌人
                        enemy = Enemy()  # 创建一个敌人对象
                        enemy.goto(screen_x, screen_y)  # 将敌人移动到该位置
                        enemy.st()  # 显示敌人
                        enemies.append(enemy)  # 将敌人加入列表
                    elif char == 'T':  # 如果字符是 'T'，表示火把
                        torch = Torch()  # 创建一个火把对象
                        torches.append(torch)  # 将火把加入列表
                        torch.goto(screen_x, screen_y)  # 将火把移动到该位置
                        torch.st()  # 显示火把

    def success():
        global timer_id
        end_time = int(time.time() - start_time)  # 计算完成时间
        if timer_id is not None:
            mz.ontimer(None, timer_id)  # 停止计时器
        message_turtle.clear()
        message_turtle.color('green')
        timer_turtle.clear()  # 停止倒计时显示
        timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))
        if current_level == len(levels):
            print('您已成功通关!')
            show_success_msg('您已成功通关!', 'green', f'剩余时间 {time_left} 秒', f'当前得分 {score} ')
        # 记录玩家完成时间并排序排行榜
        record_and_sort_time(time_left)

    def game_over():
        global timer_id
        # 停止倒计时
        if timer_id is not None:
            mz.ontimer(None, timer_id)
        fog_turtle.clear()  # 清除迷雾
        print('游戏失败!')
        show_success_msg(' 游戏失败', 'gray', f'请不要气馁', f'点击按钮重新开始')

        # 用来写成功消息的画笔

    success_pen = t.Turtle()

    # 显示成功消息的函数
    def show_success_msg(title, color, msg1, msg2):
        success_pen.ht()
        success_pen.speed(0)
        success_pen.penup()
        success_pen.goto(-150, -150)
        success_pen.fillcolor(color)  # 设置填充色
        success_pen.begin_fill()  # 开始填充
        for _ in range(4):
            success_pen.fd(300)
            success_pen.left(90)
        success_pen.end_fill()  # 结束填充
        success_pen.goto(-80, 30)
        success_pen.color('yellow')
        success_pen.write(title, align='left', font=('Arial', 20, 'bold'))
        success_pen.goto(-80, -30)
        success_pen.write(msg1, align='left', font=('Arial', 20, 'bold'))
        success_pen.goto(-80, -60)
        success_pen.write(msg2, align='left', font=('Arial', 20, 'bold'))

    # 定义进入下一关的方法
    def next_level(x=None, y=None):
        global current_level, time_left, timer_id, start_time, width, height, score, health, screen_width, screen_height, ai_enabled, hint_enabled
        current_level += 1  # 当前关卡增加1
        width += 3  # 增加迷宫的宽度
        height += 3  # 增加迷宫的高度

        # 增加窗口大小
        screen_width = min(screen_width + 48, 800)  # 每次增加48像素，最大宽度800像素
        screen_height = min(screen_height + 48, 800)  # 每次增加48像素，最大高度800像素

        # 调整窗口大小
        mz.setup(screen_width, screen_height)

        # 清除提示信息
        success_pen.clear()

        # 重置得分和时间
        score = 0
        time_left = 60
        health = 3
        ai_enabled = False  # 重新禁用AI按钮
        hint_enabled = False  # 重新禁用提示按钮

        # 重置开始时间
        start_time = time.time()

        # 隐藏并清空现有的金币、敌人和火把
        for g in golds:
            g.ht()
        for e in enemies:
            e.ht()
        for t in torches:
            t.ht()
        golds.clear()
        enemies.clear()
        torches.clear()

        # 清除迷宫的砖墙
        pen.clear()
        walls.clear()  # 清空全局walls列表

        # 生成新迷宫
        new_maze = generate_maze(width, height)
        levels.append(new_maze)

        # 重建迷宫
        pen.make_maze()

        # 重置得分显示
        score_turtle.clear()
        score_turtle.write(f"得分: {score}", align='center', font=('Arial', 20, 'bold'))

        # 重置时间显示
        timer_turtle.clear()
        timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))

        # 重置血量显示
        health_turtle.clear()
        health_turtle.write(f"血量: {health}", align='center', font=('Arial', 20, 'bold'))

        # 停止并重新启动定时器
        if timer_id is not None:
            mz.ontimer(None, timer_id)
        update_timer()

    def restart_game(x, y):
        global score, current_level, time_left, paused, timer_id, start_time, health, width, height, screen_width, screen_height, ai_enabled, hint_enabled
        score = 0  # 重置得分
        current_level = 1  # 重置当前关卡
        time_left = 60  # 重置剩余时间
        health = 3  # 重置血量
        paused = False  # 重置暂停状态
        width, height = width0, height0  # 重置迷宫尺寸
        screen_width, screen_height = 760, 760  # 重置屏幕尺寸
        ai_enabled = False  # 重新禁用AI按钮
        hint_enabled = False  # 重新禁用提示按钮

        # 保持窗口大小不变
        mz.setup(screen_width, screen_height)

        # 重置开始时间
        start_time = time.time()

        # 清除之前的定时器
        if timer_id is not None:
            mz.ontimer(None, timer_id)
            timer_id = None

        # 清除提示信息
        success_pen.clear()

        # 隐藏并清空现有的金币和敌人
        for g in golds:
            g.ht()
        for e in enemies:
            if e.timer_id:
                t.ontimer(None, e.timer_id)
            e.ht()
        golds.clear()
        enemies.clear()

        # 清除迷宫的砖墙
        pen.clear()
        walls.clear()  # 清空全局walls列表

        # 生成新迷宫
        pen.make_maze()

        # 重新启动定时器
        update_timer()

        # 重置得分显示
        score_turtle.clear()
        score_turtle.write(f"当前得分: {score}", align='center', font=('Arial', 20, 'bold'))

        # 重置时间显示
        timer_turtle.clear()
        timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))

        # 重置血量显示
        health_turtle.clear()
        health_turtle.write(f"血量: {health}", align='center', font=('Arial', 20, 'bold'))

    # 定义切换暂停状态的方法
    def toggle_pause(x, y):
        global paused
        paused = not paused  # 切换暂停状态
        if not paused:
            update_timer()  # 更新定时器
            for e in enemies:
                t.ontimer(e.move, random.randint(100, 300))  # 重新启动敌人的移动定时器

    def redraw_maze(x, y):
        global walls, golds, enemies, torches, end, end_pos, score, time_left, timer_id, start_time, health, ai_enabled, hint_enabled
        # 重置开始时间
        start_time = time.time()

        # 隐藏并清空现有的金币、敌人和火把
        for g in golds:
            g.ht()
        for e in enemies:
            e.ht()
        for t in torches:
            t.ht()
        golds.clear()
        enemies.clear()
        torches.clear()
        ai_enabled = False  # 重新禁用AI按钮
        hint_enabled = False  # 重新禁用提示按钮

        # 清除迷宫的砖墙
        pen.clear()
        walls.clear()  # 清空全局walls列表

        # 生成新迷宫
        new_maze = generate_maze(width, height)
        levels[0] = new_maze

        # 重建迷宫
        pen.make_maze()


        # 重置得分和时间
        score = 0
        time_left = 60
        health = 3

        # 重置得分显示
        score_turtle.clear()
        score_turtle.write(f"当前得分: {score}", align='center', font=('Arial', 20, 'bold'))

        # 重置时间显示
        timer_turtle.clear()
        timer_turtle.write(f"剩余时间: {time_left} 秒", align='center', font=('Arial', 20, 'bold'))

        # 重置血量显示
        health_turtle.clear()
        health_turtle.write(f"血量: {health}", align='center', font=('Arial', 20, 'bold'))

        # 停止并重新启动定时器
        if timer_id is not None:
            mz.ontimer(None, timer_id)
        update_timer()

    def check_all_gold_collected():
        global ai_enabled, hint_enabled
        if not golds:  # 如果所有金币都被收集
            ai_enabled = True  # 解锁AI按钮
            hint_enabled = True  # 解锁提示按钮
            message_turtle.clear()
            message_turtle.color('yellow')  # 确保消息显示为黄色
            message_turtle.goto(0, screen_height // 2 - 65)  # 确保消息位置在倒计时下方
            message_turtle.write("所有金币已收集，AI和提示功能已解锁", align='center', font=('Arial', 18, 'bold'))
            mz.ontimer(message_turtle.clear, 2000)  # 2秒后清除信息

    # 定义退出游戏的方法
    def exit_game(x, y):
        global timer_id
        if timer_id is not None:
            mz.ontimer(None, timer_id)
        t.bye()  # 关闭 Turtle 窗口

    # 定义返回主界面的方法
    def go_home(x, y):
        global timer_id
        if timer_id is not None:
            mz.ontimer(None, timer_id)
        t.bye()  # 关闭 Turtle 窗口
        subprocess.Popen(["python", "UI.py"])  # 打开主 UI 窗口

    # 定义记录并排序时间的方法
    def record_and_sort_time(seconds):
        with open('排行榜.txt', 'a', encoding='utf-8') as f:
            f.write(str(seconds) + '\n')
        sort_file_by_numbers("排行榜.txt")

    # 定义按数字排序文件的方法
    def sort_file_by_numbers(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines.sort(key=lambda x: float(x.strip()), reverse=True)
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    # 定义广度优先搜索算法（BFS）
    def bfs(start, goal):
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            x, y = current
            for dx, dy in [(-24, 0), (24, 0), (0, -24), (0, 24)]:
                neighbor = (x + dx, y + dy)
                if neighbor not in walls and neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = current
        path = []
        while goal:
            path.append(goal)
            goal = visited[goal]
        path.reverse()
        return path

    # 定义激活AI的方法
    def activate_ai(x, y):
        global ai_active, ai_timer_active
        if not ai_enabled:
            return  # 如果AI按钮未解锁，不执行任何操作
        ai_active = not ai_active
        if ai_active:
            ai_timer_active = True
            start = (player.xcor(), player.ycor())
            goal = end_pos
            path = bfs(start, goal)
            player.auto_move(path[1:])
        else:
            player.clear_auto_move()

    # 定义显示提示的方法
    def show_hint(x, y):
        global hint_displayed
        if not hint_enabled:
            return  # 如果提示按钮未解锁，不执行任何操作
        hint_turtle.clear()
        if hint_displayed:
            hint_displayed = False
            return
        start = (player.xcor(), player.ycor())
        goal = end_pos
        path = bfs(start, goal)
        hint_turtle.penup()
        for pos in path:
            hint_turtle.goto(pos)
            hint_turtle.dot(10, 'yellow')
        hint_displayed = True

    def update_fog():
        fog_turtle.clear()
        fog_turtle.color('black')
        fog_turtle.shape('square')
        fog_turtle.shapesize(3, 3, 1)  # 增大形状大小以覆盖更大的单元格
        player_x, player_y = player.xcor(), player.ycor()
        for i in range(-width * 12 - 12, width * 12 + 12, 24):  # 扩大覆盖范围
            for j in range(-height * 12 - 12, height * 12 + 12, 24):  # 扩大覆盖范围
                if abs(player_x - i) > 72 or abs(player_y - j) > 72:  # 增加阈值以扩大迷雾范围
                    fog_turtle.goto(i, j)
                    fog_turtle.stamp()

    # 定义切换迷雾模式的方法
    def toggle_fog_mode(x, y):
        global fog_mode
        fog_mode = not fog_mode
        if fog_mode:
            update_fog()
        else:
            fog_turtle.clear()

    # 初始化游戏
    score = 0  # 初始化分数
    pen = Pen()  # 创建一个 Pen 对象
    player = Player()  # 创建一个 Player 对象
    walls = []  # 初始化墙壁列表
    golds = []  # 初始化金币列表
    enemies = []  # 初始化敌人列表
    end = End()  # 创建一个 End 对象
    end_pos = ()  # 初始化终点位置
    pen.make_maze()  # 生成迷宫

    # 创建按钮的函数
    def create_button(image, x, y, text, onclick_function):
        mz.addshape(image)  # 添加背景图形状
        button = t.Turtle()  # 创建一个新的 Turtle 对象作为按钮
        button.penup()  # 提起画笔
        button.shape(image)  # 设置按钮的形状为指定的图片
        button.shapesize(stretch_wid=1, stretch_len=2)  # 调整按钮大小，这里缩小了按钮
        button.goto(x, y)  # 调整按钮位置
        button.onclick(onclick_function)  # 设置按钮点击事件
        button.st()  # 显示按钮

        # 创建按钮文字
        text_turtle = t.Turtle()  # 创建一个新的 Turtle 对象用于显示文字
        text_turtle.hideturtle()  # 隐藏 Turtle
        text_turtle.penup()  # 提起画笔
        text_turtle.goto(x, y - 45)  # 调整文字位置，确保文字显示在按钮下方
        text_turtle.color('white')  # 设置文字颜色为白色
        text_turtle.write(text, align='center', font=('Arial', 12, 'bold'))  # 写入文字

        return button  # 返回按钮对象

    # 创建各个按钮
    create_button('pause_button.gif', -screen_width // 2 + 60, -screen_height // 2 + 60, '暂停', toggle_pause)
    create_button('restart_button.gif', -screen_width // 2 + 140, -screen_height // 2 + 60, '重新开始', restart_game)
    hint_button = create_button('hint_button.gif', -screen_width // 2 + 220, -screen_height // 2 + 60, '提示', show_hint)  # 添加提示按钮
    ai_button = create_button('ai_button.gif', -screen_width // 2 + 300, -screen_height // 2 + 60, 'AI', activate_ai)  # 添加AI按钮
    create_button('redraw_button.gif', -screen_width // 2 + 380, -screen_height // 2 + 60, '重绘迷宫', redraw_maze)
    create_button('next_level_button.gif', -screen_width // 2 + 460, -screen_height // 2 + 60, '下一层', next_level)
    create_button('fog_button.gif', -screen_width // 2 + 540, -screen_height // 2 + 60, '迷雾模式',toggle_fog_mode)  # 添加迷雾模式按钮
    create_button('home_button.gif', -screen_width // 2 + 620, -screen_height // 2 + 60, '主页', go_home)  # 添加主页按钮
    create_button('exit_button.gif', -screen_width // 2 + 700, -screen_height // 2 + 60, '退出', exit_game)

    # 监听键盘事件
    mz.listen()
    mz.onkey(player.go_right, 'Right')  # 右箭头键
    mz.onkey(player.go_left, 'Left')  # 左箭头键
    mz.onkey(player.go_up, 'Up')  # 上箭头键
    mz.onkey(player.go_down, 'Down')  # 下箭头键
    mz.onkey(next_level, 'Return')  # 回车键

    # 设置敌人的移动定时器
    for e in enemies:
        t.ontimer(e.move, random.randint(100, 300))

    update_timer()  # 启动倒计时

    # 尝试运行游戏主循环
    try:
        while True:
            mz.update()  # 更新屏幕
    except t.Terminator:
        print("游戏结束")  # 捕获终止异常，打印游戏结束信息

    mz.mainloop()  # 开始事件循环，保持窗口打开

# 运行游戏
#run_maze_game(20, 20)
