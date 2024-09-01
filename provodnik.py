import tkinter as tk
from tkinter import filedialog
import os


def file_select():
    filename = filedialog.askopenfilename(initialdir="/", title='Выберите файл:',
                                          filetypes=(('Текстовый файл', '*.txt'), ('Все файлы', '*.*')))
    if filename:
        text['text'] = 'Выбранный файл: ' + filename
        os.startfile(filename)


window = tk.Tk()
window.title('Проводник')
window.geometry('350x350')
window.configure(bg='black')
window.resizable(False, False)

text = tk.Label(window, text='Файл:', height=5, width=62,
                background='silver', foreground='blue')
text.grid(column=1, row=1)

button_select = tk.Button(window, width=20, height=3,
                          text='Выбрать файл:', background='silver', foreground='blue', command=file_select)
button_select.grid(column=1, row=2, pady=4)

window.mainloop()