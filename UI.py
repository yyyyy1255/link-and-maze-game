import tkinter as Tk  # 导入 tkinter 模块
from tkinter import font, messagebox
from pathlib import Path  # 从 pathlib 模块导入 Path 类
from PIL import Image, ImageTk  # 从 PIL (Pillow) 模块导入 Image 和 ImageTk 类
from pygame import mixer  # 从 pygame 模块导入 mixer
import 简单, 中等, 困难, 娱乐

# 定义应用程序类
class MyApp(object):
    # 重新加载图片的方法
    def reload_image(self):
        self.img = Tk.PhotoImage(file='UI.png')  # 重新加载 UI.png 图片
        self.canv.itemconfig(self.img_, image=self.img)  # 更新画布上的图片

    # 打开排行榜的方法
    def open_leaderboard(self):
        def open_leaderboard_file(level):
            filename = None
            # 根据选择的难度设置文件名
            if level == '简单':
                filename = '简单排行榜.txt'
            elif level == '中等':
                filename = '中等排行榜.txt'
            elif level == '困难':
                filename = '困难排行榜.txt'
            if filename:
                try:
                    # 读取排行榜文件内容
                    with open(filename, 'r') as file:
                        leaderboard_text = file.read()
                    leaderboard_window = Tk.Toplevel()  # 创建新窗口
                    leaderboard_window.title(f"{level}排行榜")  # 设置窗口标题

                    # 设置窗口大小和位置
                    window_width = 400
                    window_height = 500
                    screen_width = leaderboard_window.winfo_screenwidth()
                    screen_height = leaderboard_window.winfo_screenheight()
                    x = (screen_width - window_width) // 2
                    y = (screen_height - window_height) // 2
                    leaderboard_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

                    # 添加背景图片
                    bg_image = Image.open("background.webp")  # 打开背景图片
                    bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # 调整图片大小
                    bg_photo = ImageTk.PhotoImage(bg_image)  # 转换为 PhotoImage 对象

                    # 创建画布并添加图片
                    canvas = Tk.Canvas(leaderboard_window, width=window_width, height=window_height)
                    canvas.pack(fill="both", expand=True)
                    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

                    # 在画布上显示文本
                    canvas.create_text(135, 155, anchor="nw", text="通关用时(秒)：", font=self.my_font, width=280)
                    canvas.create_text(185, 180, anchor="nw", text=leaderboard_text, font=self.my_font, width=280)

                    # 保持对 PhotoImage 的引用，防止图片被垃圾回收
                    canvas.image = bg_photo

                except FileNotFoundError:
                    # 文件未找到时显示警告
                    Tk.messagebox.showwarning("警告", f"{level}排行榜文件未找到！")

        # 创建一个新窗口以选择排行榜难度
        leaderboard_window = Tk.Toplevel()
        leaderboard_window.title("选择排行榜难度")

        # 设置窗口大小和位置
        screen_width = leaderboard_window.winfo_screenwidth()
        screen_height = leaderboard_window.winfo_screenheight()
        window_width = 300
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        leaderboard_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建标签和按钮
        label = Tk.Label(leaderboard_window, text="请选择要查看的排行榜难度：", font=self.my_font)
        label.pack()

        btn_simple = Tk.Button(leaderboard_window, text="简单排行榜", command=lambda: open_leaderboard_file('简单'), width=20, height=3, bg='lightblue', fg='white', font=self.my_font)
        btn_medium = Tk.Button(leaderboard_window, text="中等排行榜", command=lambda: open_leaderboard_file('中等'), width=20, height=3, bg='lightgreen', fg='white', font=self.my_font)
        btn_hard = Tk.Button(leaderboard_window, text="困难排行榜", command=lambda: open_leaderboard_file('困难'), width=20, height=3, bg='salmon', fg='white', font=self.my_font)

        # 设置按钮的位置
        btn_simple.pack(pady=10)
        btn_medium.pack(pady=10)
        btn_hard.pack(pady=10)

    # 显示设置选项的方法
    def show_settings(self):
        settings_text = (
            "设置选项：\n"
            "1. 音量设置。\n"
            "2. 游戏难度设置。\n"
            "3. 显示选项设置。"
        )
        messagebox.showinfo("设置", settings_text)  # 显示设置信息

    # 显示附加功能帮助的方法
    def add_feature(self):
        feature = (
            "## 游戏教程和引导\n"
            "在游戏开始时，屏幕上会随机分布各种水果图案。玩家需要在规定的时间内，通过点击两个相同的水果图案将其消除。只有当两个水果图案可以通过三个转折及以下的直线连接时，才能消除。\n"
            "## 提示和建议\n"
            "如果你找不到可以消除的水果图案对，可以点击提示按钮，系统会自动为你找到一对可以消除的水果图案。\n"
            "## 常见问题和解答\n"
            "Q: 我点击了两个相同的水果图案，为什么它们没有消除？\n"
            "A: 只有当两个水果图案可以通过三个转折及以下的直线连接时，才能消除。\n"
            "Q: 我找不到可以消除的水果图案对，怎么办？\n"
            "A: 你可以点击“提示”按钮，系统会自动为你找到一对可以消除的水果图案。\n"
            "## 设置和控制说明\n"
            "在游戏的设置菜单中，你可以调整游戏的音量\n"
            "在主UI界面，你可以选择不同的游戏难度，以及查看你的游戏记录(排行榜)。\n"
        )
        messagebox.showinfo("附加功能帮助", feature)  # 显示附加功能帮助信息

    # 显示游戏规则的方法
    def show_rules(self):
        rules_image = Image.open("游戏规则.jpg")  # 打开游戏规则图片文件
        resized_image = rules_image.resize((400, 400))  # 调整图片大小
        rules_photo = ImageTk.PhotoImage(resized_image)  # 转换为 PhotoImage 对象

        rules_message = Tk.Toplevel()  # 创建新窗口
        rules_message.title("游戏规则")  # 设置窗口标题

        # 计算窗口位置，使其居中显示
        screen_width = rules_message.winfo_screenwidth()
        screen_height = rules_message.winfo_screenheight()
        window_width = 400
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        rules_message.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建标签并显示图片
        label = Tk.Label(rules_message, image=rules_photo)
        label.image = rules_photo  # 保存对图片对象的引用，防止被垃圾回收
        label.pack()

    # 切换音乐播放状态的方法
    def toggle_music(self):
        if self.music_on:
            mixer.music.pause()  # 暂停音乐
        else:
            mixer.music.unpause()  # 继续播放音乐
        self.music_on = not self.music_on  # 切换音乐状态

    # 设置音量的方法
    def set_volume(self, volume):
        volume = float(volume)
        mixer.music.set_volume(volume)  # 设置音乐音量

    # 初始化应用程序的方法
    def __init__(self, parent):
        self.root = parent
        self.root.title("欢迎登陆水果连连看")  # 设置窗口标题

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算窗口的 x 和 y 坐标，使其位于屏幕中央
        window_width = 900
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口的几何位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.canv = Tk.Canvas(self.root)  # 创建画布
        self.image1 = Image.new('RGBA', (50, 50), (0, 0, 0, 0))  # 创建透明图片
        self.photo = ImageTk.PhotoImage(self.image1)  # 转换为 PhotoImage 对象
        self.img = Tk.PhotoImage(file='UI.png')  # 加载 UI 图片
        self.img_ = self.canv.create_image(0, 0, anchor='nw', image=self.img)  # 在画布上显示图片
        self.canv.place(x=0, y=0, height=700, width=900)  # 设置画布位置和大小
        self.my_font = font.Font(family='Helvetica', size=12, weight='bold')  # 创建字体对象
        self.input_ = Tk.Variable()  # 创建变量
        self.input_area = Tk.Entry(self.root, textvariable=self.input_, width=20)  # 创建输入框
        self.music_on = True  # 初始化音乐状态为开启
        self.volume = Tk.DoubleVar()  # 创建双精度变量
        mixer.init()  # 初始化音频混合器
        self.volume.set(mixer.music.get_volume())  # 设置音量
        volume_scale = Tk.Scale(self.root, from_=0, to=1, orient=Tk.HORIZONTAL, resolution=0.01, length=200,
                                variable=self.volume, command=self.set_volume, bg='lightblue', fg='white', font=self.my_font)
        volume_label = Tk.Label(self.root, text="音量大小", bg='lightblue', fg='white', font=self.my_font)
        volume_scale.place(x=690, y=120)  # 设置音量滑块的位置
        volume_label.place(x=690, y=100)  # 设置音量标签的位置

        # 创建按钮
        btn1 = Tk.Button(self.root, text="简单", command=lambda: self.startGame(self.input_.get(), 1), width=20, height=3, bg='lightblue', fg='white', font=self.my_font)
        btn2 = Tk.Button(self.root, text="中等", command=lambda: self.startGame(self.input_.get(), 2), width=20, height=3, bg='lightgreen', fg='white', font=self.my_font)
        btn3 = Tk.Button(self.root, text="困难", command=lambda: self.startGame(self.input_.get(), 3), width=20, height=3, bg='salmon', fg='white', font=self.my_font)
        btn4 = Tk.Button(self.root, text="开始游戏", image=self.photo,command=lambda: self.openFrame(self.input_.get(), 1), width=300, height=2, bg='salmon', fg='white', font=self.my_font)
        btn5 = Tk.Button(self.root, text="排行榜", image=self.photo, command=self.open_leaderboard, width=90, height=2, bg='lightblue', fg='white', font=self.my_font)
        btn6 = Tk.Button(self.root, text="退出游戏", image=self.photo, command=self.root.destroy, width=80, height=2, bg='salmon', fg='white', font=self.my_font)
        btn7 = Tk.Button(self.root, text="设置：", command=self.show_settings, width=5, height=1, bg='lightblue', fg='white', font=self.my_font)
        btn8 = Tk.Button(self.root, text="附加功能帮助", command=self.add_feature, width=10, height=1, bg='lightblue', fg='white', font=self.my_font)
        btn9 = Tk.Button(self.root, text="音乐开/关", command=self.toggle_music, width=10, height=1, bg='lightblue', fg='white', font=self.my_font)
        btn10 = Tk.Button(self.root, text="游戏规则", command=self.show_rules, width=10, height=1, bg='lightblue', fg='white', font=self.my_font)

        # 设置按钮的位置
        btn1.place(x=150, y=360)
        btn2.place(x=370, y=360)
        btn3.place(x=590, y=360)
        btn4.place(x=300, y=340)
        btn5.place(x=400, y=35)
        btn6.place(x=780, y=460)
        btn7.place(x=840, y=44)
        btn8.place(x=20, y=14)
        btn9.place(x=790, y=80)
        btn10.place(x=20, y=50)

    # 隐藏主窗口
    def hide(self):
        self.root.withdraw()  # 隐藏主窗口

    # 打开难度选择界面
    def openFrame(self, total, level):
        self.hide()  # 隐藏主窗口
        self.new_root = Tk.Tk()  # 创建新窗口

        # 获取屏幕尺寸
        screen_width = self.new_root.winfo_screenwidth()
        screen_height = self.new_root.winfo_screenheight()

        # 计算窗口的 x 和 y 坐标，使其位于屏幕中央
        window_width = 210
        window_height = 430
        x = (screen_width - window_height) // 2
        y = (screen_height - window_height) // 2

        self.new_root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.new_root.title("难度选择")  # 设置窗口标题

        # 创建难度选择按钮
        btn1 = Tk.Button(self.new_root, text="简单", command=lambda: self.startGame(total, 1), width=20, height=3, bg='lightblue', fg='white', font=self.my_font)
        btn2 = Tk.Button(self.new_root, text="中等", command=lambda: self.startGame(total, 2), width=20, height=3, bg='lightgreen', fg='black', font=self.my_font)
        btn3 = Tk.Button(self.new_root, text="困难", command=lambda: self.startGame(total, 3), width=20, height=3, bg='salmon', fg='white', font=self.my_font)
        btn4 = Tk.Button(self.new_root, text="娱乐", command=lambda: self.startGame(total, 4), width=20, height=3, bg='lightpink', fg='white', font=self.my_font)
        btn5 = Tk.Button(self.new_root, text="返回游戏开始界面", command=self.goBack, width=20, height=3, bg='gray', fg='white', font=self.my_font)

        # 设置按钮的位置
        btn1.grid(row=0, padx=10, pady=10)
        btn2.grid(row=1, padx=10, pady=10)
        btn3.grid(row=2, padx=10, pady=10)
        btn4.grid(row=3, padx=10, pady=10)
        btn5.grid(row=4, padx=10, pady=10)

    # 返回主界面
    def goBack(self):
        self.new_root.destroy()  # 销毁新窗口
        self.root.deiconify()  # 重新显示主窗口

    # 开始游戏，根据选择的难度启动相应的模块
    def startGame(self, total, level):
        try:
            self.new_root.destroy()  # 尝试销毁新窗口
        except AttributeError:
            pass
        self.hide()  # 隐藏主窗口
        if level == 1:
            简单.main()  # 启动简单模块
        elif level == 2:
            中等.main()  # 启动中等模块
        elif level == 3:
            困难.main()  # 启动困难模块
        elif level == 4:
            娱乐.main()  # 启动娱乐模块

# 应用程序入口
def main():
    root = Tk.Tk()  # 创建主窗口

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的 x 和 y 坐标，使其位于屏幕中央
    window_width = 900
    window_height = 500
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 设置窗口几何位置
    app = MyApp(root)  # 创建应用程序实例
    mixer.init()  # 初始化音频混合器
    root_path = Path(__file__).parent  # 获取当前文件的父目录
    music_file = root_path.joinpath('背景音乐.ogg')  # 设置音乐文件路径
    if music_file.exists():
        mixer.music.load(music_file)  # 加载音乐文件
        mixer.music.play(loops=-1)  # 循环播放音乐
    else:
        print(f"文件未找到: {music_file}")  # 文件未找到时打印错误信息
    root.mainloop()  # 进入主事件循环

if __name__ == '__main__':
    main()  # 调用主函数
