import re
import logging
from _thread import start_new_thread
from tkinter import Frame, Button, Label, Text
from tkinter.constants import N, S, END, INSERT, WORD
from tkinter.scrolledtext import ScrolledText

from api import translate_yandex

__version__ = '0.0.1'

log = logging.getLogger(__name__)

DEFAULT_FONT = 'roboto', '12'
TAG_NAME = 'tag_en'


class App(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # screen_width = self.winfo_screenwidth()
        # print(screen_width, self.winfo_screenheight())

        self.master.title(f'Mem-translate {__version__}')
        self.master.minsize(300, 200)
        self.grid_configure()

        # self.hi_there = Button(self, text="Hello World\n(click me)", command=self.say_hi)
        # # self.hi_there.pack(side="top")
        # self.hi_there.grid(row=0)

        self.text = self.get_widget_text(row=0, column=0, rowspan=2)

        # Label(self, text='Нечёткие совпадения').grid_configure(row=0, column=1)
        self.text_fuzz = self.get_widget_text_fuzz(row=0, column=1)
        self.text_tran = self.get_widget_text_tran(row=1, column=1)

        # self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        # self.quit.pack(side="bottom")

        # todo event QUIT

    def get_widget_text(self, row: int, column: int, rowspan: int) -> ScrolledText:
        """Главный виджет textArea"""
        w = ScrolledText(self, bg='white', height=32, width=73, undo=True, wrap=WORD)
        w['font'] = DEFAULT_FONT
        # txt.pack(expand=True, fill='both')
        w.bind('<Key>', self.onkey_text)
        self.set_text(w)
        w.grid_configure(row=row, column=column, rowspan=rowspan)
        w.focus_set()
        return w

    def get_widget_text_fuzz(self, row: int, column: int) -> ScrolledText:
        w = ScrolledText(self, bg='white', height=15, width=73, wrap=WORD)  # , state='disabled')
        w['font'] = DEFAULT_FONT
        # w.insert('1.0', 'text tetet')
        # w.configure(state='disabled')
        w.grid_configure(row=row, column=column, sticky=N)
        return w

    # todo merge func
    def get_widget_text_tran(self, row: int, column: int) -> ScrolledText:
        w = ScrolledText(self, bg='white', height=15, width=73, wrap=WORD)
        w['font'] = DEFAULT_FONT
        w.grid_configure(row=row, column=column, sticky=S)
        return w

    @staticmethod
    def set_text(w: Text):
        w.tag_configure(TAG_NAME, background='#aaf')

        with open('../you-can/source/01.txt') as f:
            text = f.read()

        for line in re.split(r'\n+', text):
            line = re.sub(r'([.,?])\s+', r'\1\n', line)
            for seq in line.split('\n'):
                w.insert(END, seq)
                i = int(w.index(INSERT).split('.')[0])
                w.tag_add(TAG_NAME, f'{i}.0', f'{i}.{len(seq)}')
                # w.mark_set(f'mark{i}', f'{i}.0')
                w.insert(END, '\n>>> \n')
            w.insert(END, '  <CUT>\n')
        print(w.tag_ranges(TAG_NAME))
        # print(w.mark_names())

    def onkey_text(self, event):
        """Обработчик нажатий лбой клавиши в главном textArea"""
        if event.keycode == 36:  # Return
            self.pressed_enter()
            return 'break'
        print(event)

    def pressed_enter(self):
        t = self.text.tag_nextrange(TAG_NAME, self.text.index(INSERT))
        if not t:
            return

        b, e = t
        i = int(e.split('.')[0]) + 1
        self.text.mark_set(INSERT, f'{i}.4')  # '>>> '

        text = self.text.get(b, e)
        self.text_tran.delete('1.0', END)
        start_new_thread(self.thread_translate, (text,))

    def thread_translate(self, text):
        text2 = translate_yandex(text)
        self.text_tran.insert('1.0', text2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = App()
    app.mainloop()
