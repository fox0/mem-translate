from tkinter import Frame, Button, Label
from tkinter.constants import N, INSERT, WORD
from tkinter.scrolledtext import ScrolledText

__version__ = '0.0.1'


class App(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # screen_width = self.winfo_screenwidth()
        # print(screen_width, self.winfo_screenheight())

        self.master.title(f'Mem-translate {__version__}')
        self.master.minsize(300, 200)
        self.grid()

        # self.hi_there = Button(self, text="Hello World\n(click me)", command=self.say_hi)
        # # self.hi_there.pack(side="top")
        # self.hi_there.grid(row=0)

        self.text = self.get_widget_text(row=1, column=0)

        Label(self, text='Нечёткие совпадения').grid(row=0, column=1)
        self.text_fuzz = self.get_widget_text_fuzz(row=1, columm=0)

        # self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        # self.quit.pack(side="bottom")

        # todo event QUIT

    def get_widget_text(self, row: int, column: int) -> ScrolledText:
        """Главный виджет textArea"""
        w = ScrolledText(self, bg='white', height=32, width=73, undo=True, wrap=WORD)
        w['font'] = 'roboto', '12'
        # txt.pack(expand=True, fill='both')
        w.bind('<Key>', self.handle_key_text)
        w.insert(1.0, self.get_text())
        w.grid(row=row, column=column)
        w.focus_set()
        return w

    @staticmethod
    def get_text() -> str:
        with open('../you-can/source/01.txt') as f:
            text = f.read()
        return text

    def get_widget_text_fuzz(self, row: int, columm: int) -> ScrolledText:
        w = ScrolledText(self, bg='white', height=10, width=73, wrap=WORD)  # , state='disabled')
        w['font'] = 'roboto', '12'
        w.insert(1.0, 'text tetet')
        w.configure(state='disabled')
        w.grid(row=1, column=1, sticky=N)
        return w

    def handle_key_text(self, event):
        if event.keycode == 36:  # Return
            pos = self.text.index(INSERT)
            self.text.insert(pos, '\n\n')
            return
        print(event)


if __name__ == '__main__':
    app = App()
    app.mainloop()
