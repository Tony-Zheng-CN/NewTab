# -*- coding:GBK -*-
import ttkbootstrap
from tkdev4 import DevWindow, DevManage
from getBili import GetBili
from getInfo import GetInfo
from TalkBot import TalkBot
from screeninfo import get_monitors

global bar
bar = 0


def setTran(win):
    win.config(bg="#ABCDEF")
    win.wm_attributes("-transparent", "#ABCDEF")


def setAcrylic(win):
    Manage = DevManage(win)
    Manage.use_acrylic(True)


def setBlur(win):
    Manage = DevManage(win)
    Manage.use_mica(True)


def setDrug(win):
    Manage = DevManage(win)
    Manage.send_message_move_window(win)


def setBar(win):
    def find_monitor_under_mouse():
        x, y = win.winfo_pointerxy()
        for monitor in get_monitors():
            if monitor.x <= x <= monitor.x + monitor.width and \
                    monitor.y <= y <= monitor.y + monitor.height:
                return monitor
        return None



    def follow_mouse():
        monitor = find_monitor_under_mouse()
        if monitor:
            win.geometry("1920x" + str(int(win.winfo_screenheight() / 30)) + "+" + str(monitor.x) + "+" + str(monitor.y))
        win.after(50, follow_mouse)

    global bar
    Manage = DevManage(win)
    Manage.use_acrylic()
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.geometry(str(win.winfo_screenwidth()) + "x" + str(int(win.winfo_screenheight() / 30)) + "+0+0")
    bar = 1
    follow_mouse()


main_win = DevWindow()
main_win_style = ttkbootstrap.Style("newtabtheme")

# setAcrylic(main_win)
setBar(main_win)
# setDrug(main_win)

bili = GetBili(main_win, bar)
sys_info = GetInfo(main_win, bar)
talk_bot = TalkBot(main_win, bar)

bili.grid(row=0, column=0, rowspan=2, padx=10)
sys_info.grid(row=0, column=1)
talk_bot.grid(row=1, column=1, padx=10)

sys_info.update()

main_win.mainloop()
