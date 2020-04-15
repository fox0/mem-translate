"""
Приложение и слой UI
"""
import logging
from difflib import SequenceMatcher
from tkinter import Frame, Menu
# from tkinter.constants import N, S, END, INSERT, WORD
from tkinter.filedialog import Open
from tkinter.scrolledtext import ScrolledText
from typing import List

from fuzzywuzzy.process import extractBests

from _thread import start_new_thread

from api import translate_yandex
from text import do_import, PREFIX_TRANSLATE

__version__ = '0.0.2'

log = logging.getLogger(__name__)

DEFAULT_FONT = 'roboto', '12'
TAG_BLUE = 'tag_blue'


class App(Frame):
    """Гланое окно приложения"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # screen_width = self.winfo_screenwidth()
        # print(screen_width, self.winfo_screenheight())

        self.master.title(f'Mem-translate {__version__}')
        self.master.minsize(300, 200)

        menu = Menu(self.master)
        self.master.configure(menu=menu)

        menu_file = Menu(menu)
        menu_file.add_command(label='Импорт', command=self.on_import)
        menu.add_cascade(label='Файл', menu=menu_file)

        width = 73

        self.text = ScrolledText(self, bg='white', height=31, width=width, undo=True, wrap='word')
        self.text['font'] = DEFAULT_FONT
        self.text.tag_configure(TAG_BLUE, background='#aaf')
        self.text.focus_set()
        self.text.bind('<Key>', self.on_key_text)
        self.text.grid_configure(row=0, column=0, rowspan=2)

        self.text_fuzz = ScrolledText(self, bg='white', height=15, width=width, wrap='word')
        self.text_fuzz['font'] = DEFAULT_FONT
        self.text_fuzz.tag_configure(TAG_BLUE, background='#afa')
        self.text_fuzz.bind('<Key>', lambda event: 'break')
        self.text_fuzz.grid_configure(row=0, column=1, sticky='n')

        self.text_tran = ScrolledText(self, bg='white', height=15, width=width, wrap='word')
        self.text_tran['font'] = DEFAULT_FONT
        self.text_tran.bind('<Key>', lambda event: 'break')
        self.text_tran.grid_configure(row=1, column=1, sticky='s')

        self.grid_configure()

    def destroy(self):
        # todo
        log.info('destroy')
        super().destroy()

    def on_import(self):
        """Обработчик кнопки Импорт"""
        filename = Open(initialdir='../you-can/source/', filetypes=(('Текст', '*.txt'),)).show()
        text_ls = do_import(filename)
        self.do_open(text_ls)

    def do_open(self, text_ls: List[str]):
        """Отрисовать текст"""
        for line in text_ls:
            self.text.insert('end', line)
            # добавляем немного подсветки
            # if not line.startswith(PREFIX_TRANSLATE) and line != PREFIX_CUT:
            if not line.startswith('>>>'):
                i = self.text.index('insert').split('.', 1)[0]
                self.text.tag_add(TAG_BLUE, f'{i}.0', f'{i}.{len(line)}')
            self.text.insert('end', '\n')
        log.debug(self.text.tag_ranges(TAG_BLUE))

    def on_key_text(self, event):
        """Обработчик нажатий любой клавиши в главном textArea"""
        if event.keycode == 36:  # Return
            self.do_enter()
            return 'break'
        log.debug(event)

    def do_enter(self):
        tag_range = self.text.tag_nextrange(TAG_BLUE, self.text.index('insert'))
        if not tag_range:
            return
        index1, index2 = tag_range

        # двигаем курсор
        index = int(index2.split('.')[0]) + 1
        self.text.mark_set('insert', f'{index}.{len(PREFIX_TRANSLATE)}')
        self.text.see('insert')

        text: str = self.text.get(index1, index2)

        # переводим текст
        self.text_tran.delete('1.0', 'end')
        start_new_thread(self.thread_translate, (text,))

        # ...
        self.text_fuzz.delete('1.0', 'end')
        start_new_thread(self.thread_fuzz, (text,))

    def thread_translate(self, text: str):
        """Асинхронно запускаем машинный перевод"""
        try:
            text2 = translate_yandex(text)
        except BaseException as ex:
            text2 = str(ex)
        self.text_tran.insert('1.0', text2)

    def thread_fuzz(self, text: str):
        """Асинхронно ищем нечёткие совпадения"""
        # todo закешировать + парсить перевод + перенести в text.py
        ls: list = self.text.get('1.0', 'end').split('\n')
        ls.remove(text)
        choices = [f'{i + 1}: {line}' for i, line in enumerate(ls) if not line.startswith('>>>')]
        result = [f'{line} ({p})' for line, p in extractBests(text, choices, score_cutoff=1, limit=7)]

        # self.text_fuzz.insert('1.0', '\n'.join(result))
        for line in result:
            self.text_fuzz.insert('end', line)
            i = self.text_fuzz.index('insert').split('.', 1)[0]
            for m in SequenceMatcher(None, line.lower(), text.lower()).get_matching_blocks():
                self.text_fuzz.tag_add(TAG_BLUE, f'{i}.{m.a}', f'{i}.{m.a + m.size}')
            self.text_fuzz.insert('end', '\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    App().mainloop()
