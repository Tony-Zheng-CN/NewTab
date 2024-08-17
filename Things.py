from ttkbootstrap import Style, ttk
from tkdev4 import DevWindow, DevManage
from PIL import ImageTk


class FloatWin(object):
    def __init__(self, message, place="N", title=":)", kind="INFO"):
        self.window = DevWindow()
        self.style = Style(theme="newtabthemem")
        self.window.title(title)
        self.manage = DevManage(self.window)
        self.manage.use_acrylic(0.8)
        self.title = ttk.Label(master=self.window, text=title, font=(None, 20))
        self.message = ttk.Label(master=self.window, text=message, font=(None, 10))
        self.image = ttk.Label(master=self.window)
        if kind == "INFO":
            self.image.image = ImageTk.BitmapImage(file="/image/Inf.png")
        elif kind == "WARN":
            self.image.image = ImageTk.BitmapImage(file="/image/War.png")
        elif kind == "ERROR":
            self.image.image = ImageTk.BitmapImage(file="/image/Err.png")
        self.title.grid(row=0, column=0, columnspan=2)
        self.message.grid(row=1, column=1)
        self.image.grid(row=1, column=0)
