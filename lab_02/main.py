import tkinter as tk
from tkinter.ttk import Treeview, Scrollbar, Style
from math import *
import matplotlib.pyplot as plt
import numpy as np


window = tk.Tk()
window['bg'] = 'gray22'
window.title('Приближенные корни функции')
heads = ['№ корня', '[xi; xi+h]', 'x\'', 'f(x\')', 'Кол-во итераций', 'Код ошибки']
window.geometry('1024x810+0+0')
message_1, message_2, message_3, message_4, message_5, message_6 = tk.StringVar(), tk.StringVar(), tk.StringVar(), \
                                                                   tk.StringVar(), tk.StringVar(), tk.StringVar()
sqrs = False

tk.Label(text='Здравствуй, пользователь!', foreground='white', background='gray22',
         font=('Comic Sans MS', 20, 'bold')).pack()


def table_new():
    style = Style()
    style.theme_use('clam')

    table = Treeview(show='headings')
    table['columns'] = heads

    table.heading(heads[0], text=heads[0], anchor='center')
    table.column(heads[0], anchor='center', width=30)

    table.heading(heads[1], text=heads[1], anchor='center')
    table.column(heads[1], anchor='center', width=150)

    table.heading(heads[2], text=heads[2], anchor='center')
    table.column(heads[2], anchor='center', width=50)

    table.heading(heads[3], text=heads[3], anchor='center')
    table.column(heads[3], anchor='center', width=50)

    table.heading(heads[4], text=heads[4], anchor='center')
    table.column(heads[4], anchor='center', width=30)

    table.heading(heads[5], text=heads[5], anchor='center')
    table.column(heads[5], anchor='center', width=10)

    scroll = Scrollbar(table, command=table.yview)
    table.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH, pady=250)

    return table


table = table_new()


def clear_all():
    entry_func.delete(0, 'end')
    entry_a.delete(0, 'end')
    entry_b.delete(0, 'end')
    entry_h.delete(0, 'end')
    entry_n_max.delete(0, 'end')
    entry_eps.delete(0, 'end')


def check_input_func(func, x):
    try:
        eval(func)
    except Exception:
        entry_func.configure(bg='red')
        return False
    entry_func.configure(bg='gray22')
    return True


def check_input_section(a, b):
    try:
        float(a)
    except Exception:
        entry_a.configure(bg='red')
        try:
            float(b)
        except Exception:
            entry_b.configure(bg='red')
            return False, False
        return False, False
    try:
        float(b)
    except Exception:
        entry_b.configure(bg='red')
        return False, False
    entry_a.configure(bg='gray22')
    entry_b.configure(bg='gray22')
    if float(a) >= float(b):
        entry_a.configure(bg='red')
        entry_b.configure(bg='red')
        return False, False
    return float(a), float(b)


def check_input_step(h):
    try:
        float(h)
    except Exception:
        entry_h.configure(bg='red')
        return False
    if float(h) <= 0:
        entry_h.configure(bg='red')
        return False
    entry_h.configure(bg='gray22')
    return float(h)


def check_input_count(n_max):
    if str(n_max).isdigit() and int(n_max) > 0:
        entry_n_max.configure(bg='gray22')
        return int(n_max)
    entry_n_max.configure(bg='red')
    return False


def check_input_eps(eps):
    try:
        float(eps)
    except Exception:
        entry_eps.configure(bg='red')
        return False
    if float(eps) <= 0:
        entry_eps.configure(bg='red')
        return False
    entry_eps.configure(bg='gray22')
    return float(eps)


def f(x):
    func = entry_func.get()
    if check_input_func(func, x):
        return eval(func)
    else:
        return 'error'


def counting_sec(h, x0, x1, eps, n_max):
    answer, sqrs = [], {}
    h = (x1 - x0) if h == 0 else h
    for i in range(int((x1 - x0) // h)):
        xk_1, xk_2, count = x0 + i * h, x0 + (i + 1) * h, 0
        while fabs(xk_2 - xk_1) > eps:
            if f(xk_2) == 'error' or f(xk_1) == 'error':
                answer += [[(i + 1), x0 + i * h, x0 + (i + 1) * h, '-', '-', count + 1, 4]]
                break
            if (f(xk_2) - f(xk_1)) == 0:
                answer += [[(i + 1), x0 + i * h, x0 + (i + 1) * h, '-', '-', count + 1, 3]]
                break
            xk_2, xk_1 = xk_2 - ((xk_2 - xk_1) / (f(xk_2) - f(xk_1))) * f(xk_2), xk_2
            if count > n_max:
                answer += [[(i + 1), x0 + i * h, x0 + (i + 1) * h, '-', '-', count - 1, 2]]
                break
            count += 1
        else:
            if not (x0 + i * h <= xk_2 <= x0 + (i + 1) * h):
                answer += [[(i + 1), x0 + i * h, x0 + (i + 1) * h, '-', '-', count, 1]]
            else:
                sqrs[xk_2] = f(xk_2)
                answer += [[(i + 1), x0 + i * h, x0 + (i + 1) * h, f'{xk_2:.1f}', f'{f(xk_2):e}', count, 0]]
    return answer, sqrs


def counting(flag=False):
    global table, sqrs
    x0, x1 = check_input_section(entry_a.get(), entry_b.get())
    h = check_input_step(entry_h.get())
    n_max = check_input_count(entry_n_max.get())
    eps = check_input_eps(entry_eps.get())
    if (x0 and x1 or x0 == 0 and x1 or x0 and x1 == 0) and h and n_max and eps and x1 - x0 >= h \
            and check_input_func(entry_func.get(), x0):
        answer, sqrs = counting_sec(h, x0, x1, eps, n_max)
        table_fill(answer)
    if flag:
        return sqrs


def graph():
    global sqrs
    if not sqrs:
        sqrs = counting(flag=True)
    x0, x1 = check_input_section(entry_a.get(), entry_b.get())
    h = check_input_step(entry_h.get())
    n_max = check_input_count(entry_n_max.get())
    eps = check_input_eps(entry_eps.get())
    if ((x0 and x1 or x0 == 0 and x1 or x0 and x1 == 0) and h and n_max and eps and x1 - x0 >= h
            and check_input_func(entry_func.get(), x0)):
        xs = np.arange(x0, x1, 1e-3)
        ys = [f(i) for i in xs]

        extremums, inflections,  derivatives = {}, {}, []

        for i, delta in enumerate(zip(np.diff(ys), np.diff(xs))):
            derivative = delta[0] / delta[1]
            if fabs(derivative) < 1e-2:
                extremums[xs[i]] = ys[i]
            derivatives += [derivative]

        for i, der in enumerate(zip(np.diff(derivatives), np.diff(xs))):
            inflec = der[0] / der[1]
            if i == 0:
                inflec_save = inflec
                continue
            if fabs(inflec) < 1e-3 and ((inflec <= 0 <= inflec_save) or (inflec >= 0 >= inflec_save)):
                inflections[xs[i]] = ys[i]
            inflec_save = inflec

        plt.scatter(x=extremums.keys(), y=extremums.values(), c='orange', s=100, label='Экстремумы') #Экстремумы
        plt.scatter(x=inflections.keys(), y=inflections.values(), c='blue', s=100, marker='X', label='Перегибы') #Перегибы
        plt.scatter(x=sqrs.keys(), y=sqrs.values(), c='red', s=10, label='Корни') #Корни
        plt.plot(xs, ys)
        plt.title(f'График функции {entry_func.get()}', fontsize=10)
        plt.legend(loc="upper left")

        sqrs = False

        plt.show()


def table_fill(answer):
    global table
    for i in table.get_children():
        table.delete(i)
    for sqrs in answer:
        table.insert('', tk.END, values=(sqrs[0], f'{sqrs[1]:.2f} ; {sqrs[2]:.2f}',
                                         sqrs[3], sqrs[4], sqrs[5], sqrs[6]))


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
label_h = tk.Label(window, text='при шаге', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_h.place(x=750, y=60)
entry_h = tk.Entry(fg='white', bg='gray22', width=7, font=('Comic Sans MS', 13, 'bold'), textvariable=message_4)

entry_h.place(x=860, y=65)
label_n_max = tk.Label(window, text='c максимальным количеством итераций', foreground='white', background='gray22',
                       font=('Comic Sans MS', 15, 'bold'))
label_n_max.place(x=10, y=110)
entry_n_max = tk.Entry(fg='white', bg='gray22', width=11, font=('Comic Sans MS', 13, 'bold'), textvariable=message_5)

entry_n_max.place(x=450, y=115)
label_eps = tk.Label(window, text='и точностью', foreground='white', background='gray22',
                     font=('Comic Sans MS', 15, 'bold'))
label_eps.place(x=600, y=110)
entry_eps = tk.Entry(fg='white', bg='gray22', width=13, font=('Comic Sans MS', 13, 'bold'), textvariable=message_6)

entry_eps.place(x=750, y=115)
label_trash = tk.Label(window, text='имеет', foreground='white', background='gray22',
                       font=('Comic Sans MS', 15, 'bold'))

label_trash.place(x=900, y=110)
button_counting = tk.Button(text='Корни', command=counting, activebackground='gray30', activeforeground='gray',
                            bg='gray20', fg='white', font=('Comic Sans MS', 17, 'bold'), relief='raised', bd='17',
                            width=10)
button_counting.place(x=440, y=180)

button_counting = tk.Button(text='Построить график', command=graph, activebackground='gray30', activeforeground='gray',
                            bg='gray20', fg='white', font=('Comic Sans MS', 13, 'bold'), relief='raised', bd='13',
                            width=20)
button_counting.place(x=750, y=180)

tk.Label(window, text='4 код ошибки - Значение функции не определено', foreground='white', background='gray22',
         font=('Comic Sans MS', 10, 'bold')).pack(side='bottom')

tk.Label(window, text='3 код ошибки - Деление на ноль', foreground='white', background='gray22',
         font=('Comic Sans MS', 10, 'bold')).pack(side='bottom')

tk.Label(window, text='2 код ошибки - Превышение максимального кол-ва итераций', foreground='white',
         background='gray22', font=('Comic Sans MS', 10, 'bold')).pack(side='bottom')

tk.Label(window, text='1 код ошибки - Выход за пределы отрезка', foreground='white', background='gray22',
         font=('Comic Sans MS', 10, 'bold')).pack(side='bottom')

tk.Label(window, text='0 код ошибки - Отработало корректно', foreground='white', background='gray22',
         font=('Comic Sans MS', 10, 'bold')).pack(side='bottom')

menu = tk.Menu(window)
window.config(menu=menu)

menu.add_command(label='Очистить все поля', command=clear_all)
menu.add_command(label='Выход', command=window.destroy)

window.bind('Entry', tk.Entry.tk_focusNext(entry_func).focus())

window.mainloop()
