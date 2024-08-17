from psutil import cpu_percent, virtual_memory
from ttkbootstrap import ttk
from time import localtime


class GetInfo(object):
    def __init__(self, window, bar):
        self.bar = bar
        if bar == 1:
            self.win = window
            self.cpu = ttk.Label(master=self.win, text="CPU: ")
            self.mem = ttk.Label(master=self.win, text="Mem: ")
            self.time = ttk.Label(master=self.win, text="Mem: ")
            self.cpu.place(x=1520, y=2)
            self.mem.place(x=1620, y=2)
            self.time.place(x=1720, y=2)
        else:
            self.frame = ttk.LabelFrame(window, text="系统信息")
            self.win = window
            self.cpu = ttk.Label(master=self.frame, text="CPU使用率: ")
            self.mem = ttk.Label(master=self.frame, text="内存使用率: ")
            self.cpu.grid(row=0, column=0)
            self.mem.grid(row=1, column=0)

    def update(self):
        if self.bar == 0:
            self.cpu.config(text="CPU使用率: " + str(cpu_percent()) + "%")
            self.mem.config(text="内存使用率: " + str(virtual_memory().percent) + "%")
            self.win.after(1000, self.update)
        else:
            self.cpu.config(text="CPU: " + str(cpu_percent()) + "%")
            self.mem.config(text="Mem: " + str(virtual_memory().percent) + "%")
            self.time.config(text="Time: " + str(localtime().tm_year) + "/" + str(localtime().tm_mon) + "/" + str(localtime().tm_mday) + "  " + str(localtime().tm_hour) + ":" + str(localtime().tm_min))
            self.win.after(1000, self.update)

    def grid(self, row, column, padx=0, pady=0, sticky="n", columnspan=1, rowspan=1):
        if self.bar == 0:
            self.frame.grid(row=row, column=column, pady=pady, padx=padx, sticky=sticky, columnspan=columnspan,
                            rowspan=rowspan)
        else:
            pass

    def place(self, x, y):
        if self.bar == 0:
            self.frame.place(x=x, y=y)
        else:
            pass

    def height(self):
        if self.bar == 0:
            return self.frame.winfo_reqwidth()
        else:
            return None

    def width(self):
        if self.bar == 0:
            return self.frame.winfo_reqwidth()
        else:
            return None
