import tkinter as tk
import random

# 弹窗计数器（初始为0）
window_count = 0
# 最大弹窗数量
MAX_WINDOWS = 100
# 程序运行标志
running = True


def create_warm_tip(root):
    global window_count  # 声明使用全局计数器

    # 检查程序是否还在运行
    if not running or window_count >= MAX_WINDOWS:
        return

    # 创建弹窗（关联主窗口 root）
    window = tk.Toplevel(root)

    # 获取屏幕宽高
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 随机窗口位置（确保完全显示）
    window_width = 250
    window_height = 60
    x = random.randrange(0, screen_width - window_width)
    y = random.randrange(0, screen_height - window_height)

    # 设置窗口标题、大小和位置
    window.title('温馨提示')
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 随机提示文字（所有文字前面加上"娟娟"）
    tips = [
        '娟娟多喝水哦~', '娟娟保持微笑呀', '娟娟每天都要元气满满',
        '娟娟记得吃水果', '娟娟保持好心情', '娟娟好好爱自己', '娟娟我想你了',
        '娟娟梦想成真', '娟娟期待下一次见面', '娟娟金榜题名',
        '娟娟顺顺利利', '娟娟早点休息', '娟娟愿所有烦恼都消失',
        '娟娟别熬夜', '娟娟今天过得开心嘛', '娟娟天冷了，多穿衣服'
    ]
    tip = random.choice(tips)

    # 随机背景颜色
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen', 'lavender',
        'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine',
        'mistyrose', 'honeydew', 'lavenderblush', 'oldlace'
    ]
    bg = random.choice(bg_colors)

    # 创建标签显示文字
    tk.Label(
        window,
        text=tip,
        bg=bg,
        font=('微软雅黑', 16),
        width=30,
        height=3
    ).pack()

    # 窗口置顶（新弹窗会显示在最上层）
    window.attributes('-topmost', True)

    # 弹窗数量+1
    window_count += 1


def auto_pop_tips(root, interval=300):  # 间隔时间（毫秒），0.3秒=300毫秒
    # 只有当弹窗数量小于300且程序在运行时，才继续创建
    if running and window_count < MAX_WINDOWS:
        create_warm_tip(root)  # 创建一个弹窗
        # 继续定时递归调用（实现循环弹窗）
        root.after(interval, auto_pop_tips, root, interval)
    elif window_count >= MAX_WINDOWS:
        # 达到300个弹窗后，打印提示并停止
        print(f"已达到最大弹窗数量（{MAX_WINDOWS}个），自动暂停")


def on_enter_key(event):
    """按Enter键退出程序"""
    global running
    running = False  # 停止生成新弹窗

    # 关闭所有已打开的弹窗
    for child in event.widget.winfo_children():
        if isinstance(child, tk.Toplevel):
            try:
                child.destroy()
            except:
                pass

    # 关闭主窗口
    event.widget.quit()
    event.widget.destroy()
    print("程序已退出")


def main():
    global running, window_count
    # 重置运行状态
    running = True
    window_count = 0

    # 创建主窗口（不隐藏，但设置为最小化）
    root = tk.Tk()
    root.title("温馨提示程序")
    root.iconify()  # 最小化窗口，而不是完全隐藏

    # 绑定Enter键退出功能 - 绑定到根窗口
    root.bind('<Return>', on_enter_key)
    root.bind('<Escape>', on_enter_key)

    # 确保窗口能接收键盘事件
    root.focus_set()

    # 为所有弹窗也绑定退出事件
    def bind_to_all_windows(event=None):
        for child in root.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.bind('<Return>', on_enter_key)
                child.bind('<Escape>', on_enter_key)
        root.after(100, bind_to_all_windows)

    bind_to_all_windows()

    print("温馨提示程序开始运行...")
    print("按 Enter 键或 ESC 键可随时退出程序")

    # 启动定时弹窗（间隔0.3秒）
    auto_pop_tips(root, 300)

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    main()