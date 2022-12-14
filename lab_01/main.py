import tkinter as tk
from secure import secure_five

window = tk.Tk()
window['bg'] = 'gray22'
window.title('Калькулятор систем счисления')
window.geometry('1024x500+100+200')


def resize():
    window.update_idletasks()
    window.geometry('1024x810+0+0')


def active(event):
    global active_entry
    active_entry = event.widget


def entry(event):
    active_entry.insert('end', event.widget['text'])


def clear():
    active_entry.delete(0, 'end')


def clear_all():
    entry_1.delete(0, 'end')
    entry_2.delete(0, 'end')
    entry_3.delete(0, 'end')


def del_last():
    text = active_entry.get()
    active_entry.delete(0, 'end')
    active_entry.insert(0, text[:-1])


def max_length(a, b):
    if len(a[:a.index('.')]) > len(b[:b.index('.')]):
        max_int = len(a[:a.index('.')])
    else:
        max_int = len(b[:b.index('.')])
    if len(a[a.index('.') + 1:]) > len(b[b.index('.') + 1:]):
        max_float = len(a[a.index('.') + 1:])
    else:
        max_float = len(b[b.index('.') + 1:])
    return max_int, max_float


def add_zero(string: str, max_int, max_float):
    while len(string[:string.index('.')]) < max_int:
        string = '0' + string
    while len(string[string.index('.') + 1:]) < max_float:
        string += '0'
    return string


def counting(sym, term_1, term_2):
    max_int, max_float = max_length(str(term_1), str(term_2))
    flag = False
    if str(term_1)[0] == '-' and str(term_2)[0] == '-':
        if sym == '+':
            term_1, term_2, flag, sym = abs(term_1), abs(term_2), True, '+'
        elif term_1 >= term_2:
            term_1, term_2 = abs(term_2), abs(term_1)
        else:
            term_1, term_2, flag = abs(term_1), abs(term_2), True
    elif str(term_1)[0] == '-':
        if sym == '-':
            term_1, term_2, flag, sym = abs(term_1), abs(term_2), True, '+'
        elif abs(term_1) >= term_2:
            term_1, flag, sym = abs(term_1), True, '-'
        else:
            term_1, term_2, sym = term_2, abs(term_1), '-'
    elif str(term_2)[0] == '-':
        if sym == '-':
            term_2 = abs(term_2)
        elif abs(term_2) >= term_1:
            term_1, term_2, flag, sym = abs(term_2), term_1, True, '-'
        else:
            term_2, sym = abs(term_2), '-'
    term_1, term_2 = add_zero(str(term_1), max_int, max_float), add_zero(str(term_2), max_int, max_float)
    if float(term_2) > float(term_1) and sym == '-':
        term_2, term_1 = term_1, term_2
        flag = True
    total, rem = '', 0
    for i in range(len(term_1) - 1, -1, -1):
        if term_1[i] == '.':
            total = '.' + total
        else:
            if sym == '+':
                if int(term_1[i]) + int(term_2[i]) + rem > 4:
                    total = str(int(term_1[i]) + int(term_2[i]) - 5 + rem) + total
                    rem = 1
                else:
                    total = str(int(term_1[i]) + int(term_2[i]) + rem) + total
                    rem = 0
            elif sym == '-':
                if int(term_1[i]) - int(term_2[i]) < 0:
                    total = str(5 + int(term_1[i]) - int(term_2[i])) + total
                    j = i - 1 if term_1[i - 1] != '.' else i - 2
                    while term_1[j] == '0':
                        term_1 = term_1[:j] + '4' + term_1[j + 1:]
                        j -= 2 if term_1[j - 1] == '.' else 1
                    term_1 = term_1[:j] + str(int(term_1[j]) - 1) + term_1[j + 1:]
                else:
                    total = str(int(term_1[i]) - int(term_2[i])) + total
    if rem == 1:
        total = '1' + total
    for i in range(len(total)):
        if total[i] != '0':
            break
    if flag:
        return '-' + total[i:]
    else:
        return total[i:] if total.count('0') != len(total) - 1 else '0'


def calc(sym=None):
    if sym:
        term_1, symbol, term_2 = message_1.get(), sym, message_3.get()
    else:
        term_1, symbol, term_2 = message_1.get(), message_2.get(), message_3.get()
    if secure_five(term_1) and secure_five(term_2):
        term_1, term_2 = str(float(term_1)), str(float(term_2))
        if symbol in ['+', '-']:
            calc_answer = counting(symbol, float(term_1), float(term_2))
        else:
            calc_answer = 'Некорректные данные'
    else:
        calc_answer = 'Некорректные данные'
    answer.delete(0.0, 'end')
    answer.insert(0.0, f'Полученный ответ: {str(calc_answer)}')


def plus():
    entry_2.delete(0, 'end')
    entry_2.insert(0, '+')
    calc(sym='+')


def diff():
    entry_2.delete(0, 'end')
    entry_2.insert(0, '-')
    calc(sym='-')


tk.Label(text='Здравствуй, пользователь!', foreground='white', background='gray22',
         font=('Comic Sans MS', 20, 'bold')).pack()

button_size = tk.Button(text='Виртуальная клавиатура', command=resize, activebackground='gray30',
                        activeforeground='gray', bg='gray20', fg='white', font=('Comic Sans MS', 10, 'bold'),
                        relief='raised')
button_size.pack(side='bottom')

button_clear = tk.Button(text='Очистить все поля', command=clear_all, activebackground='gray30',
                         activeforeground='gray', bg='gray20', fg='white', font=('Comic Sans MS', 10, 'bold'),
                         relief='raised')
button_clear.pack(side='top')

labelframe = tk.LabelFrame(window, text='Поля ввода', foreground='white', background='gray22', borderwidth=0,
                           font=('Comic Sans MS', 15, 'bold'))
labelframe.columnconfigure(0, weight=1, minsize=50)
labelframe.columnconfigure(1, weight=1, minsize=50)
labelframe.columnconfigure(2, weight=1, minsize=50)

message_1, message_2, message_3 = tk.StringVar(), tk.StringVar(), tk.StringVar()

label_1 = tk.Label(labelframe, text='Первое число:', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_1.grid(row=1, column=0, padx=1, pady=5)
entry_1 = tk.Entry(labelframe, fg='white', bg='gray22', width=60, font=('Comic Sans MS', 13, 'bold'),
                   textvariable=message_1)
entry_1.bind('<FocusIn>', active)
entry_1.grid(row=2, column=0, padx=1, pady=5)
active_entry = entry_1

labelframe.bind('Entry', tk.Entry.tk_focusNext(active_entry).focus())

label_2 = tk.Label(labelframe, text='Знак:', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_2.grid(row=1, column=1, padx=1, pady=5)
entry_2 = tk.Entry(labelframe, fg='white', bg='gray22', width=4, font=('Comic Sans MS', 13, 'bold'),
                   textvariable=message_2)
entry_2.bind('<FocusIn>', active)
entry_2.grid(row=2, column=1, padx=1, pady=5)

label_3 = tk.Label(labelframe, text='Второе число:', foreground='white', background='gray22',
                   font=('Comic Sans MS', 15, 'bold'))
label_3.grid(row=1, column=2, padx=1, pady=5)
entry_3 = tk.Entry(labelframe, fg='white', bg='gray22', width=60, font=('Comic Sans MS', 13, 'bold'),
                   textvariable=message_3)
entry_3.bind('<FocusIn>', active)
entry_3.grid(row=2, column=2, padx=1, pady=5)

answer = tk.Text(labelframe, width=70, height=2, fg='red', bg='gray22', relief='flat',
                 font=('Comic Sans MS', 13, 'bold'))
answer.grid(row=3, column=1)

button_calc = tk.Button(labelframe, text='Вычислить', command=calc, activebackground='gray30', activeforeground='gray',
                        bg='gray20', fg='white', font=('Comic Sans MS', 13, 'bold'), relief='raised')
button_calc.grid(row=4, column=1)

labelframe.pack(fill='both', expand=True, side='top', pady=87, padx=60)

keyboard = tk.LabelFrame(text='Клавиатура', foreground='white', background='gray22', borderwidth=0,
                         font=('Comic Sans MS', 15, 'bold'))
btn_1 = tk.Button(keyboard, text='1', activebackground='gray30', activeforeground='gray', bg='gray20', fg='white',
                  font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34)
btn_1.bind('<Button-1>', entry)
btn_1.grid(row=0, column=0)
for i in range(1, 9):
    btn = tk.Button(keyboard, text=f'{i + 1}', activebackground='gray30', activeforeground='gray', bg='gray20',
                    fg='white', font=('Comic Sans MS', 14, 'bold'),  width=34, relief='raised', bd='20')
    btn.bind('<Button-1>', entry)
    btn.grid(row=int(i/3), column=int(i % 3))

btn = tk.Button(keyboard, text='0', activebackground='gray30', activeforeground='gray', bg='gray20', fg='white',
                font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34)
btn.bind('<Button-1>', entry)
btn.grid(row=4, column=0)

btn = tk.Button(keyboard, text='+', activebackground='gray30', activeforeground='gray', bg='gray20',
                fg='white', font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34)
btn.bind('<Button-1>', entry)
btn.grid(row=4, column=1)

btn = tk.Button(keyboard, text='-', activebackground='gray30', activeforeground='gray', bg='gray20', fg='white',
                font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34)
btn.bind('<Button-1>', entry)
btn.grid(row=4, column=2)

btn = tk.Button(keyboard, text='.', activebackground='gray30', activeforeground='gray', bg='gray20', fg='white',
                font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34)
btn.bind('<Button-1>', entry)
btn.grid(row=5, column=0)

tk.Button(keyboard, text='=', activebackground='gray30', command=calc, activeforeground='gray', bg='gray20', fg='white',
          font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34).grid(row=5, column=1)

tk.Button(keyboard, text='C', activebackground='gray30', command=clear, activeforeground='gray', bg='gray20',
          fg='white', font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=34).grid(row=5, column=2)

tk.Button(keyboard, text='<--', activebackground='gray30', command=del_last, activeforeground='gray', bg='gray20',
          fg='white', font=('Comic Sans MS', 14, 'bold'), relief='raised', bd='20', width=5).grid(row=0, column=4)

keyboard.rowconfigure(0, weight=1, minsize=0)
keyboard.rowconfigure(2, weight=1, minsize=0)
keyboard.rowconfigure(1, weight=1, minsize=0)
keyboard.rowconfigure(3, weight=1, minsize=0)
keyboard.rowconfigure(4, weight=1, minsize=0)
keyboard.rowconfigure(5, weight=1, minsize=0)
keyboard.columnconfigure(0, weight=1, minsize=0)
keyboard.columnconfigure(1, weight=1, minsize=0)
keyboard.columnconfigure(2, weight=1, minsize=0)

keyboard.pack(fill='both', expand=True, side='bottom', pady=0, padx=250)

menu = tk.Menu(window)
window.config(menu=menu)
motion_menu = tk.Menu(menu, tearoff=0)
motion_menu.add_command(label='Сложение', command=plus)
motion_menu.add_command(label='Вычитание', command=diff)
motion_menu.add_command(label='Очистить все поля', command=clear_all)

menu.add_cascade(label='Заданные действия', menu=motion_menu)
menu.add_command(label='Выход', command=window.destroy)

window.mainloop()
