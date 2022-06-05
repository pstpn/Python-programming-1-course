# Информация о программе:
# 
# [ЗАЩИТА ЛАБОРАТОРНОЙ РАБОТЫ]
# 
# Программа позволяет найти корни функции, заданной вручную, на отрезке упрощенным методом Ньютона.
# Реализована в рамках курса по "Программированию на Python".
# 
# Автор: Постнов Степан Андреевич, студент МГТУ им. Н.Э.Баумана


import tkinter as tk
from math import *

window = tk.Tk()
window['bg'] = 'gray22'
window.geometry('1024x810+0+0')
window.title('Приближенные корни функции')
message_1, message_2, message_3, message_4 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()


def f(x):
    func = entry_func.get()
    return eval(func)


def counting_x(x1, eps):
    diff_x0 = ((f(x1 + 1e-13) - f(x1)) / 1e-13)
    while abs(f(x1)) > eps:
        x1 = x1 - f(x1) / diff_x0
    answer.delete(0.0, 'end')
    answer.insert(0.0, f'Полученный корень: {str(x1)}')


def counting():
    x0, x1, eps = entry_a.get(), entry_b.get(), entry_eps.get()
    counting_x(float(x0), float(eps))


label_func = tk.Label(window, text='Функция', foreground='white', background='gray22',
                      font=('Comic Sans MS', 15, 'bold'))
label_func.place(x=10, y=60)
entry_func = tk.Entry(fg='white', bg='gray22', width=20, font=('Comic Sans MS', 13, 'bold'),
                      textvariable=message_1)

entry_func.place(x=110, y=65)
label_a = tk.Label(window, text='на отрезке от', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_a.place(x=340, y=60)

entry_a = tk.Entry(fg='white', bg='gray22', width=7, font=('Comic Sans MS', 13, 'bold'), textvariable=message_2)
entry_a.place(x=500, y=65)
label_b = tk.Label(window, text='до', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_b.place(x=600, y=60)

entry_b = tk.Entry(fg='white', bg='gray22', width=7, font=('Comic Sans MS', 13, 'bold'), textvariable=message_3)
entry_b.place(x=650, y=65)

label_eps = tk.Label(window, text='и точностью', foreground='white', background='gray22',
                     font=('Comic Sans MS', 15, 'bold'))
label_eps.place(x=740, y=60)
entry_eps = tk.Entry(fg='white', bg='gray22', width=10, font=('Comic Sans MS', 13, 'bold'), textvariable=message_4)

entry_eps.place(x=880, y=65)

button_counting = tk.Button(text='Имеет корень', command=counting, activebackground='gray30', activeforeground='gray',
                            bg='gray20', fg='white', font=('Comic Sans MS', 17, 'bold'), relief='raised', bd='17',
                            width=20)
button_counting.place(x=440, y=280)

answer = tk.Text(width=70, height=2, fg='red', bg='gray22', relief='flat',
                 font=('Comic Sans MS', 13, 'bold'))
answer.place(x=440, y=180)

window.mainloop()
