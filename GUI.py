# !/usr/bin/env python3
"""
Simple GUI
saves to file

Author: James Rose
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Rectangle, Color
# from StockNewsSummarizer import main
import pandas as pd
import os
home = os.path.expanduser("~/")
downloads = os.path.join(home, "Downloads")


def update_Rect(instance, size):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.size = (800, 800)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=update_Rect, pos=update_Rect)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(Label(text="Ticker Symbol: "))
        self.symbol = TextInput(multiline=False, hint_text="Enter Your Symbol")
        self.inside.add_widget(self.symbol)

        self.avaliable_sources = ['yahoo', 'CNBC', 'SeekingAlpha']
        self.avaliable_sources_lower = [s.lower() for s in self.avaliable_sources]
        sources = ", ".join(self.avaliable_sources)
        self.inside.add_widget(Label(text="Source: "))
        self.sources = TextInput(multiline=False, hint_text=sources)
        self.inside.add_widget(self.sources)

        self.inside.add_widget(Label(text="Depth: "))
        self.depth = TextInput(multiline=False, hint_text='5')
        self.inside.add_widget(self.depth)

        self.inside.add_widget(Label(text="Threads: "))
        self.threads = TextInput(multiline=False, hint_text='4')
        self.inside.add_widget(self.threads)

        self.inside.add_widget(Label(text="# of Ranked Sentences: "))
        self.top_n = TextInput(multiline=False, hint_text='5')
        self.inside.add_widget(self.top_n)

        self.add_widget(self.inside)

        self.submit = Button(text="Scrape Articles", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)



    def pressed(self, instance):
        symbol = self.symbol.text.strip()
        sources = self.sources.text.strip().lower()
        depth = self.depth.text.strip()
        threads = self.threads.text.strip()
        top_n = self.top_n.text.strip()
        if sources == '':
            sources = ['all']
        else:
            src_lst = [source.strip() for source in sources.split(',')]
            sources = [source for source in src_lst if source in self.avaliable_sources_lower]
            if len(sources) == 0:
                sources = ['all']
        if not depth.isdigit():
            depth = 5
        if not threads.isdigit():
            threads = 4
        if not top_n.isdigit():
            top_n = 5
        content = main(symbol, sources=sources, threads=threads, depth=depth, top_n=top_n)
        df = pd.DataFrame(data=content)
        temp_out = os.path.join(downloads, "StockNewScrapperOut.csv")
        df.to_csv(temp_out)
        os.system("libreoffice {}".format(temp_out))
        self.symbol.text = ""
        self.sources.text = ""
        self.depth.text = ""
        self.threads.text = ""




class MyApp(App):
    def build(self):
        self.title = "Stock News Summary"
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
