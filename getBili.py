import requests
import re

from lxml import etree
from webbrowser import open as web_open
from textwrap import fill

from tkdev4 import DevWindow
from ttkbootstrap import ttk, Style


class GetBili(object):
    def __init__(self, window, bar):
        self.bar = bar
        self.win = window
        if bar == 1:
            self.button = ttk.Button(master=self.win, text="B站推荐", command=self.show_buttons,
                                     style="success.Toolbutton")
        else:
            self.response = None
            self.frame = ttk.LabelFrame(window, text="BiliBili首页推荐", width=10)
            self.buttons = self.create_buttons()
            self.update = ttk.Button(master=self.frame, text="刷新", command=self.refresh)
            self.update.grid(row=7, column=0, padx=10, pady=10)

    header = {
        'referer': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
    }

    url = 'https://www.bilibili.com/'

    def getVideoInfo(self):
        i = 0
        try:
            self.response = requests.get(url=self.url, headers=self.header, timeout=(4.05, 27))
            i += 3
        except requests.exceptions.RequestException:
            i += 1
            videos_list = []
            for x in range(0, 6):
                videos_list.append({'title': "连接失败", 'link': "https://baidu.com"})
            return videos_list

        html_text = self.response.text

        tree = etree.HTML(html_text)

        video_links = tree.xpath('//div[@class="bili-video-card__wrap __scale-wrap"]/a[@target="_blank"]/@href')

        titles = re.findall('<picture class="v-img bili-video-card__cover">.*?alt="(.*?)".*?</picture>', html_text,
                            re.S)
        videos_list = []

        # 清理列表
        video_links = [link for link in video_links if len(link) <= 50][:6]
        titles = titles[:6]

        for title, link in zip(titles, video_links):
            title = fill(title, 17)
            videos_list.append({'title': title, 'link': link})

        return videos_list

    def create_buttons(self):
        videos_list = self.getVideoInfo()
        buttons = []
        for i, video in enumerate(videos_list):
            if self.bar == 0:
                button = ttk.Button(master=self.frame, width=30, text=video['title'],
                                command=lambda v=video: web_open(v['link']))
            else:
                button = ttk.Button(master=self.win, width=30, text=video['title'],
                                command=lambda v=video: web_open(v['link']))
            button.grid(row=i, column=0, padx=10, pady=3)
            buttons.append(button)
        return buttons

    def refresh(self):
        for button, video in zip(self.buttons, self.getVideoInfo()):
            button.text = video['title']
            button.update()

    def show_buttons(self):
        self.win = DevWindow()
        self.win.geometry("350x450")
        self.style = Style("newtabtheme")
        self.win.title("BiliBili首页推荐")
        self.buttons = self.create_buttons()

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
