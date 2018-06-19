from tkinter import *
class Report(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self._text = Text(self, state=DISABLED, *args, **kwargs)
        self._text.pack(side='left', fill='both', expand=1)

        scrollbar['command'] = self._text.yview
        self._text['yscrollcommand'] = scrollbar.set

    def write(self, text):
        self._text.configure(state=NORMAL)
        self._text.insert(END, text+'\n')
        self._text.configure(state=DISABLED)
        self._text.yview_moveto('1.0')  # Прокрутка до конца вниз после вывода

    def clear(self):
        self._text.configure(state=NORMAL)
        self._text.delete(0.0, END)
        self._text.configure(state=DISABLED)

    def flush(self):
        # Метод нужен для полного видимого соответствия классу StringIO в части вывода
        pass