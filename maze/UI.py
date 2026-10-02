import tkinter as tk  # 导入Tkinter库
from tkinter import messagebox, font  # 从Tkinter库导入消息框和字体模块
from PIL import Image, ImageTk  # 从PIL库导入图像处理模块
import maze  # 导入迷宫游戏模块
from tkinter import DoubleVar, Scale, Label  # 从Tkinter库导入双变量、滑动条和标签模块
import pygame  # 导入Pygame库

class UI:
    def __init__(self):
        self.root = tk.Tk()  # 创建主窗口
        self.center_window(self.root, 800, 500)  # 居中显示窗口，尺寸为800x500
        self.root.title("欢迎登录迷宫小游戏")  # 设置窗口标题

        # 初始化pygame的混音器
        pygame.mixer.init()

        # 加载背景音乐
        pygame.mixer.music.load("背景音乐.mp3")  # 确保背景音乐文件放在正确的路径下
        initial_volume = 1.0  # 设置初始音量
        pygame.mixer.music.set_volume(initial_volume)  # 设置背景音乐音量
        pygame.mixer.music.play(-1)  # 循环播放背景音乐

        # 字体
        self.my_font = font.Font(family='Helvetica', size=12, weight='bold')  # 创建字体样式

        # 背景图片
        bg_image = Image.open("background.webp")  # 打开背景图片
        bg_image = bg_image.resize((800, 500), Image.Resampling.LANCZOS)  # 调整图片大小
        self.bg_photo = ImageTk.PhotoImage(bg_image)  # 转换为Tkinter兼容的图片格式

        # 创建Canvas并设置背景图片
        self.canvas = tk.Canvas(self.root, width=800, height=500)  # 创建Canvas画布
        self.canvas.pack(fill="both", expand=True)  # 填充整个窗口
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")  # 在画布上放置背景图片

        # 创建标签和输入框的组合框架
        self.frame_width = tk.Frame(self.root, bg="#F0F0F0")  # 创建用于输入迷宫宽度的框架
        self.frame_height = tk.Frame(self.root, bg="#F0F0F0")  # 创建用于输入迷宫高度的框架

        # 创建并放置迷宫宽度的标签和输入框
        self.label_width = tk.Label(self.frame_width, text="迷宫宽度：", font=self.my_font, width=12, bg="#FFC0CB")
        self.entry_width = tk.Entry(self.frame_width, font=self.my_font, width=2)

        # 创建并放置迷宫高度的标签和输入框
        self.label_height = tk.Label(self.frame_height, text="迷宫高度：", font=self.my_font, width=12, bg="#F5F5DC")
        self.entry_height = tk.Entry(self.frame_height, font=self.my_font, width=2)

        self.label_width.pack(side="left")  # 将迷宫宽度标签放置在框架中
        self.entry_width.pack(side="left")  # 将迷宫宽度输入框放置在框架中
        self.label_height.pack(side="left")  # 将迷宫高度标签放置在框架中
        self.entry_height.pack(side="left")  # 将迷宫高度输入框放置在框架中

        # 音量调节器
        self.volume = DoubleVar()  # 创建双变量用于音量控制
        self.volume.set(initial_volume)  # 将初始音量设为1.0
        self.volume_button = tk.Button(self.root, text="音乐开/关", command=self.toggle_music, font=self.my_font, width=10, height=1, bg="#CD7F32", fg="white")
        volume_scale = Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, length=150,
                             variable=self.volume, command=self.adjust_volume, bg='#F5F5DC', font=self.my_font)
        volume_label = Label(self.root, text="音量大小", bg='#F5F5DC', font=self.my_font)
        volume_scale.place(x=620, y=180)  # 放置音量滑动条
        volume_label.place(x=620, y=160)  # 放置音量标签
        self.volume_button.place(x=658, y=115)  # 放置音量按钮

        # 创建按钮
        self.start_button = tk.Button(self.root, text="开始游戏", command=self.start_game, font=self.my_font, width=14, height=1,  bg="#F5F5DC")
        self.rules_button = tk.Button(self.root, text="游戏规则", command=self.show_rules, font=self.my_font, width=10, height=1, bg="#CD7F32", fg="white")
        self.leaderboard_button = tk.Button(self.root, text="排行榜", command=self.open_leaderboard, font=self.my_font, width=14, height=1,  bg="#F5F5DC")
        self.help_button = tk.Button(self.root, text="附加功能帮助", command=self.show_help, font=self.my_font, width=10, height=1, bg="#CD7F32", fg="white")
        self.settings_button = tk.Button(self.root, text="设置", command=self.show_settings, font=self.my_font, width=10, height=1, bg="#CD7F32", fg="white")
        self.exit_button = tk.Button(self.root, text="退出游戏", command=self.exit_game, font=self.my_font, width=14, height=1, bg="#CD7F32", fg="white")

        # 在Canvas上放置小部件
        self.canvas.create_window(400, 200, window=self.frame_width)
        self.canvas.create_window(400, 245, window=self.frame_height)
        self.canvas.create_window(400, 285, window=self.start_button)
        self.canvas.create_window(90, 130, window=self.rules_button)
        self.canvas.create_window(400, 330, window=self.leaderboard_button)
        self.canvas.create_window(90, 85, window=self.help_button)
        self.canvas.create_window(715, 85, window=self.settings_button)
        self.canvas.create_window(400, 380, window=self.exit_button)

        self.root.mainloop()  # 进入Tkinter的主循环

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()  # 获取屏幕宽度
        screen_height = window.winfo_screenheight()  # 获取屏幕高度
        x = (screen_width - width) // 2  # 计算窗口的X坐标
        y = (screen_height - height) // 2  # 计算窗口的Y坐标
        window.geometry(f'{width}x{height}+{x}+{y}')  # 设置窗口的几何位置和大小

    def open_leaderboard(self):
        leaderboard_window = tk.Toplevel()  # 创建排行榜窗口
        self.center_window(leaderboard_window, 400, 500)  # 设置排行榜窗口大小并居中
        leaderboard_window.title("排行榜")
        window_width = 400
        window_height = 500
        try:
            with open('排行榜.txt', 'r') as file:  # 读取排行榜文件
                leaderboard_text = file.read()
                # 添加背景图片
                bg_image = Image.open("background1.webp")  # 打开背景图片
                bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # 调整图片大小
                bg_photo = ImageTk.PhotoImage(bg_image)  # 转换为Tkinter兼容的图片格式

                canvas = tk.Canvas(leaderboard_window, width=window_width, height=window_height)  # 创建Canvas画布
                canvas.pack(fill="both", expand=True)  # 填充整个窗口
                canvas.create_image(0, 0, image=bg_photo, anchor="nw")  # 在画布上放置背景图片

                # 在Canvas上显示文本
                canvas.create_text(140, 168, anchor="nw", text="剩余时间(秒)：", font=self.my_font, width=280)
                canvas.create_text(185, 185, anchor="nw", text=leaderboard_text, font=self.my_font, width=280)

                # 保持对PhotoImage的引用
                canvas.image = bg_photo
        except FileNotFoundError:
            messagebox.showwarning("警告", "排行榜文件未找到！")  # 如果文件未找到，显示警告

    def start_game(self):
        ui_width = int(self.entry_width.get())  # 获取用户输入的迷宫宽度
        ui_height = int(self.entry_height.get())  # 获取用户输入的迷宫高度

        if ui_width % 2 == 0:
            ui_width += 1  # 确保宽度为奇数
        if ui_height % 2 == 0:
            ui_height += 1  # 确保高度为奇数

        self.root.destroy()  # 销毁主窗口
        maze.run_maze_game(ui_width, ui_height)  # 传递宽度和高度参数启动迷宫游戏

    def show_rules(self):
        rules = (
            "迷宫小游戏规则：\n"
            "1. 使用方向键移动玩家。\n"
            "2. 初始时间为60秒，在规定时间内到达终点就算游戏通关。\n"
            "3. 初始血量为三滴，碰到敌人扣一滴血如果血量扣完游戏直接失败。\n"
            "4. 收集金币可增加得分和剩余时间，每吃到一个金币得分+1，剩余时间+3。\n"
            "5. 您可以选择点击迷雾模式按钮开启迷雾模式，此状态下您的视野将受限。\n"
            "6. 收集火把可以短暂获得5秒的视野。\n"
            "7. 提示按钮会提示并用黄点帮你标注到达终点的路线。\n"
            "8. AI按钮会自动帮你到达终点。\n"
            "9. 重绘迷宫按钮会仍保持你给定的宽度和高度重新绘制迷宫。\n"
            "10. 下一层按钮会将你给定的宽度和高度加一后绘制新的迷宫。\n"

        )
        messagebox.showinfo("游戏规则", rules)  # 显示游戏规则

    def show_help(self):
        help_text = (
            "迷宫游戏帮助：\n"
            "1. 输入迷宫的宽度和高度，确保为奇数。\n"
            "2. 请先输入宽度和高度后再点击开始游戏进入迷宫。\n"
            "3. 难度随宽度和高度增大而增大，但金币数，火把数也会增多"
            "3. 使用方向键控制角色移动。\n"
            "4. 尽量收集所有金币并避开敌人。\n"
            "5. 收集火把可以获得5秒的视野。\n"
            "6. 完成迷宫后进入下一关。"
        )
        messagebox.showinfo("帮助", help_text)  # 显示帮助信息

    def show_settings(self):
        settings_text = (
            "设置选项：\n"
            "1. 音量设置。\n"
            "2. 游戏难度设置。\n"
            "3. 显示选项设置。"
        )
        messagebox.showinfo("设置", settings_text)  # 显示设置选项

    def toggle_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()  # 暂停音乐
            self.volume_button.config(text="音乐关")  # 更新按钮文本
        else:
            pygame.mixer.music.unpause()  # 继续播放音乐
            self.volume_button.config(text="音乐开")  # 更新按钮文本

    def adjust_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))  # 调整音乐音量

    def exit_game(self):
        self.root.destroy()  # 关闭主窗口

UI()  # 实例化UI类
