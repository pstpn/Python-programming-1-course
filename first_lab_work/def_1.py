# Информация о программе:
# 
# [ЗАЩИТА ЛАБОРАТОРНОЙ РАБОТЫ]
# 
# Калькулятор, переводящий число из 10 с/с в 3 с/с
# Реализован в рамках курса по "Программированию на Python".
# 
# Автор: Постнов Степан Андреевич, студент МГТУ им. Н.Э.Баумана


import tkinter as tk


window = tk.Tk()
window['bg'] = 'gray22'
window.title('Калькулятор систем счисления')
window.geometry('500x500+100+100')


def counting(a: str):
    answer, part = '', int(a)
    while part > 2:
        answer, part = str(part - (part//3)*3) + answer, part//3
    answer = str(part) + answer
    answer_entry.delete(0.0, 'end')
    answer_entry.insert(0.0, answer)


def calc():
    counting(entry_1.get())


tk.Button(text='Вычислить', command=calc, activebackground='gray30', activeforeground='gray', bg='gray20', fg='white',
          font=('Comic Sans MS', 13, 'bold'), relief='raised').grid(row=2, column=1)

entry_1 = tk.Entry(fg='white', bg='gray22', width=20, font=('Comic Sans MS', 13, 'bold'))
entry_1.grid(row=0, column=1)

answer_entry = tk.Text(width=70, height=2, fg='red', bg='gray22', relief='flat', font=('Comic Sans MS', 13, 'bold'))
answer_entry.grid(row=1, column=1)

window.mainloop()
