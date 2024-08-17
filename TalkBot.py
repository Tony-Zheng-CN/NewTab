# -*- coding:GBK -*-
import ttkbootstrap
from ttkbootstrap import ttk
from sympy import sympify
from tkdev4 import DevWindow


class TalkBot(object):
    def __init__(self, window, bar):
        self.bar = bar
        self.win = window
        if bar == 1:
            self.button = ttk.Button(master=self.win, text="计算器", command=self.go_bar, style="success.Toolbutton")
        else:
            self.frame = ttk.LabelFrame(self.win, text="计算器")
            self.go = ttk.Button(master=self.frame, text="开始", command=self.go)
            self.input = ttk.Entry(master=self.frame, width=15)
            self.output = ttk.Entry(master=self.frame, width=20)
            self.output.grid(row=1, column=0, columnspan=2)
            self.go.grid(row=0, column=0)
            self.input.grid(row=0, column=1)

    def go_bar(self):
        self.win = DevWindow()
        self.style = ttkbootstrap.Style("newtabtheme")
        self.win.title("计算器")
        self.win.geometry("500x100")
        self.go = ttk.Button(master=self.win, text="开始", command=self.go)
        self.input = ttk.Entry(master=self.win, width=15)
        self.output = ttk.Entry(master=self.win, width=20)
        self.output.grid(row=1, column=0, columnspan=2)
        self.go.grid(row=0, column=0)
        self.input.grid(row=0, column=1)

    def go(self):
        input_value = self.input.get()
        try:
            """expr = sympify(input_value)
            result = expr.evalf()"""
            from AIMod import AIBot
            result = AIBot(input_value)
            output_text = f"计算结果: {result}"
            self.output.delete(0, "end")
            self.output.insert(0, output_text)
        except Exception as e:
            self.output.delete(0, "end")
            self.output.insert(0, f"错误: {str(e)}")

    def grid(self, row, column, padx=0, pady=0, sticky="n", columnspan=1, rowspan=1):
        if self.bar == 0:
            self.frame.grid(row=row, column=column, pady=pady, padx=padx, sticky=sticky, columnspan=columnspan,
                            rowspan=rowspan)
        else:
            self.button.grid(row=row, column=column, pady=pady, padx=padx, sticky=sticky, columnspan=columnspan,
                            rowspan=rowspan)

    def place(self, x, y):
        if self.bar == 0:
            self.frame.place(x=x, y=y)
        else:
            self.button.place(x=x, y=y)

    def height(self):
        if self.bar == 0:
            return self.frame.winfo_reqwidth()
        else:
            return self.button.winfo_reqheight()

    def width(self):
        if self.bar == 0:
            return self.frame.winfo_reqwidth()
        else:
            return self.button.winfo_reqwidth()
