import tkinter as tk
import random
import sys

# 弹窗计数器（初始为0）
window_count = 0
# 最大弹窗数量
MAX_WINDOWS = 100
# 程序运行标志
running = True
# 存储 after ID 用于取消任务
after_id = None


def create_warm_tip(root):
    global window_count

    if not running or window_count >= MAX_WINDOWS:
        return

    try:
        # 创建弹窗
        window = tk.Toplevel(root)

        # 获取屏幕宽高
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 随机窗口位置
        window_width = 250
        window_height = 60
        x = random.randrange(0, screen_width - window_width)
        y = random.randrange(0, screen_height - window_height)

        # 设置窗口
        window.title('温馨提示')
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 随机提示文字
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

        # 创建标签
        label = tk.Label(
            window,
            text=tip,
            bg=bg,
            font=('微软雅黑', 16),
            width=30,
            height=3
        )
        label.pack()

        # 窗口置顶
        window.attributes('-topmost', True)

        # 为弹窗和标签绑定退出事件
        window.bind('<Return>', on_enter_key)
        window.bind('<Escape>', on_enter_key)
        window.bind('<KeyPress>', lambda e: print(f"Key pressed: {e.keysym}"))  # 调试用
        label.bind('<Return>', on_enter_key)
        label.bind('<Escape>', on_enter_key)

        # 强制弹窗获取焦点
        window.focus_force()
        window.grab_set_global()  # 全局捕获输入

        window_count += 1
        print(f"已创建弹窗: {window_count}")  # 调试信息

    except Exception as e:
        print(f"创建窗口错误: {e}")


def auto_pop_tips(root, interval=300):
    global after_id
    if running and window_count < MAX_WINDOWS:
        create_warm_tip(root)
        after_id = root.after(interval, auto_pop_tips, root, interval)
    elif window_count >= MAX_WINDOWS:
        print(f"已达到最大弹窗数量（{MAX_WINDOWS}个），自动暂停")


def on_enter_key(event=None):
    """按Enter键或ESC键退出程序"""
    global running, after_id

    print("退出命令已接收")  # 调试信息

    running = False

    # 取消预定的任务
    if after_id:
        try:
            # 获取根窗口
            root = None
            if event and hasattr(event, 'widget'):
                root = event.widget.winfo_toplevel()
                root.after_cancel(after_id)
            else:
                tk._default_root.after_cancel(after_id)
        except:
            pass
        after_id = None

    # 关闭所有窗口
    def safe_quit():
        try:
            root = tk._default_root
            if root:
                for child in root.winfo_children():
                    if isinstance(child, tk.Toplevel):
                        try:
                            child.destroy()
                        except:
                            pass
                root.quit()
                root.destroy()
        except:
            pass
        sys.exit(0)

    # 立即退出
    safe_quit()


def main():
    global running, window_count, after_id

    running = True
    window_count = 0
    after_id = None

    # 创建主窗口但不最小化，而是隐藏
    root = tk.Tk()
    root.title("温馨提示程序")

    # 不最小化，而是隐藏标题栏并置于后台
    root.overrideredirect(True)  # 隐藏标题栏
    root.geometry("1x1+0+0")  # 设置为极小尺寸
    root.withdraw()  # 隐藏窗口

    # 绑定退出事件到根窗口
    root.bind('<Return>', on_enter_key)
    root.bind('<Escape>', on_enter_key)

    # 确保根窗口能接收键盘事件
    root.focus_set()

    print("温馨提示程序开始运行...")
    print("点击一下弹窗后，按 Enter 键或 ESC 键可随时退出程序")
    print("注意：请确保其中一个弹窗有焦点（点击一下弹窗）")

    # 启动定时弹窗
    auto_pop_tips(root, 300)

    try:
        root.mainloop()
    except Exception as e:
        print(f"程序异常: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()