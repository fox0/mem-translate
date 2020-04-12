"""
Приложение и слой UI
"""
import logging
from _thread import start_new_thread
from tkinter import Frame, Menu
from tkinter.constants import N, S, END, INSERT, WORD
from tkinter.filedialog import Open
from tkinter.scrolledtext import ScrolledText

from api import translate_yandex
from text import do_import

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

        menu = Menu(self.master)
        self.master.configure(menu=menu)

        menu_file = Menu(menu)
        menu_file.add_command(label='Открыть', command=self.on_import)
        menu.add_cascade(label='Файл', menu=menu_file)

        WIDTH = 73

        self.text = ScrolledText(self, bg='white', height=31, width=WIDTH, undo=True, wrap=WORD)
        self.text['font'] = DEFAULT_FONT
        self.text.tag_configure(TAG_NAME, background='#aaf')
        self.text.focus_set()
        self.text.bind('<Key>', self.on_key_text)
        self.text.grid_configure(row=0, column=0, rowspan=2)

        self.text_fuzz = ScrolledText(self, bg='white', height=15, width=WIDTH, wrap=WORD)
        self.text_fuzz['font'] = DEFAULT_FONT
        self.text_fuzz.bind('<Key>', lambda event: 'break')
        self.text_fuzz.grid_configure(row=0, column=1, sticky=N)

        self.text_tran = ScrolledText(self, bg='white', height=15, width=WIDTH, wrap=WORD)
        self.text_tran['font'] = DEFAULT_FONT
        self.text_tran.bind('<Key>', lambda event: 'break')
        self.text_tran.grid_configure(row=1, column=1, sticky=S)

        self.grid_configure()

    def destroy(self):
        # todo
        print('destroy')
        super().destroy()

    def on_import(self):
        """Обработчик кнопки Открыть"""
        filename = Open(initialdir='../you-can/source/', filetypes=(('Текст', '*.txt'),)).show()
        ls = do_import(filename)
        for line in ls:
            if line:
                self.text.insert(END, line)
                i = self.text.index(INSERT).split('.', 1)[0]
                self.text.tag_add(TAG_NAME, f'{i}.0', f'{i}.{len(line)}')
                self.text.insert(END, '\n>>> \n')
                continue
            self.text.insert(END, '  <cut>\n')
        log.debug(self.text.tag_ranges(TAG_NAME))

    def on_key_text(self, event):
        """Обработчик нажатий любой клавиши в главном textArea"""
        if event.keycode == 36:  # Return
            self.pressed_enter()
            return 'break'
        log.debug(event)

    def pressed_enter(self):
        t = self.text.tag_nextrange(TAG_NAME, self.text.index(INSERT))
        if not t:
            return

        b, e = t
        i = int(e.split('.')[0]) + 1
        self.text.mark_set(INSERT, f'{i}.4')  # '>>> '
        self.text.see(INSERT)

        text = self.text.get(b, e)
        self.text_tran.delete('1.0', END)
        start_new_thread(self.thread_translate, (text,))

    def thread_translate(self, text):
        try:
            text2 = translate_yandex(text)
        except BaseException as ex:
            text2 = str(ex)
        self.text_tran.insert('1.0', text2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = App()
    app.mainloop()
