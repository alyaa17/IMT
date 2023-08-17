import tkinter as tk
from tkinter import ttk
import re

# создание главного окна
root = tk.Tk()
root.configure(bg='#fff')
root.geometry('800x600+300+50')
root.title('Программа расчета Индекса Массы Тела')
icon = tk.PhotoImage(file='weight-scale.png')
root.iconphoto(False, icon)
root.resizable(False, False)


def is_valid(value):  # проверка корректности введённых данных (валидация Entry)
    return re.match(r"[0123456789.]{0,5}$", value) is not None


check = (root.register(is_valid), "%P")


def change_lang():  # выбор языка
    if root.nametowidget('lang')['text'] == 'рус':
        root.nametowidget('lang')['text'] = 'en'
        root.nametowidget('weight_text')['text'] = 'Enter weight (in kg):'
        root.nametowidget('height_text')['text'] = 'Enter height (in cm):'
        root.nametowidget('calc')['text'] = 'Calculate BMI'
    else:
        root.nametowidget('lang')['text'] = 'рус'
        root.nametowidget('weight_text')['text'] = 'Введите вес (в кг):'
        root.nametowidget('height_text')['text'] = 'Введите рост (в см):'
        root.nametowidget('calc')['text'] = 'Рассчитать ИМТ'


def close_win(win):  # закрытие дочернего окна
    root_lang = root.nametowidget('lang')['text']
    win_lang = win.nametowidget('win_lang')['text']
    if root_lang != win_lang:  # совпадение языка на главном и дочернем окне
        change_lang()
    win.destroy()


def new_win(IMT, IMT_designation):  # функция дочернего окна (с результатами ИМТ)

    def win_change_lang(IMT_lang, IMT_designation_lang):  # выбор языка на дочернем окне
        if win.nametowidget('win_lang')['text'] == 'рус':
            win.nametowidget('win_lang')['text'] = 'en'
            table.place_forget()
            table_en.place(x=0, y=80, relwidth=1)
            win.nametowidget('again')['text'] = 'Calculate again'
            for i in range(len(data)):
                if data[i][1] == IMT_designation_lang:
                    IMT_designation_lang = data_en[i][1]
            win.nametowidget('label_result')['text'] = f'Your BMI {IMT_lang} - {IMT_designation_lang}'
        else:
            win.nametowidget('win_lang')['text'] = 'рус'
            table_en.place_forget()
            table.place(x=0, y=80, relwidth=1)
            win.nametowidget('again')['text'] = 'Рассчитать снова'
            for i in range(len(data_en)):
                if data_en[i][1] == IMT_designation_lang:
                    IMT_designation_lang = data[i][1]
            win.nametowidget('label_result')['text'] = f'Your BMI {IMT_lang} - {IMT_designation_lang}'

    # создание окна
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.configure(bg='#fff')
    win.geometry('800x600+308+81')
    win.title('Программа расчета Индекса Массы Тела')
    win_icon = tk.PhotoImage(file='weight-scale.png')
    win.iconphoto(False, win_icon)
    win.resizable(False, False)

    win_btn_lang = tk.Button(win,
                             text='рус',
                             name='win_lang',
                             relief='groove',
                             bg='#fff',
                             font=('Comic Sans MS', 15),
                             command=lambda IMT_func=IMT, IMT_designation_func=IMT_designation: win_change_lang
                             (IMT_func, IMT_designation_func)
                             )
    win_btn_lang.place(x=20, y=10, width=100, height=40)

    data = [('16 и менее', 'Выраженный дефицит \n массы тела'), ('16—18,5', 'Недостаточная (дефицит) \n масса тела'),
            ('18,5—25', 'Норма'), ('25—30', 'Избыточная масса \n тела (предожирение)'),
            ('30—35', 'Ожирение 1 степени'), ('35—40', 'Ожирение 2 степени'), ('40 и более', 'Ожирение 3 степени')]
    data_en = [('16 and under', 'Severe underweight'), ('16—18,5', 'Insufficient (deficit) \n body weight'),
               ('18,5—25', 'Norm'), ('25—30', 'Overweight (pre-obesity)'),
               ('30—35', 'Obesity 1 degree'), ('35—40', 'Obesity 2 degree'), ('40 or more', 'Obesity 3 degree')]

    # создание таблицы соответствия между массой и ростом (вариант на русском)
    columns = ['IMT', 'designation']
    table = ttk.Treeview(win, columns=columns, show="headings", padding=20)
    table.heading('IMT', text='Индекс массы тела')
    table.heading('designation', text='Соответствие между массой человека и его ростом')
    for elem in data:
        table.insert("", tk.END, values=elem)
    table.place(x=0, y=80, relwidth=1)  # изначально выводится русский вариант
    # создание таблицы соответствия между массой и ростом (вариант на английском)
    table_en = ttk.Treeview(win, columns=columns, show="headings", padding=20)
    table_en.heading('IMT', text='Body mass index')
    table_en.heading('designation', text='Correspondence between the mass of a person and his height')
    for elem in data_en:
        table_en.insert("", tk.END, values=elem)

    # меняем цвет в зависимости от результата расчёта
    if IMT_designation == data[0][1] or IMT_designation == data[1][1]:
        font_color = '#fc6b03'
    elif IMT_designation == data[2][1]:
        font_color = '#4ce01b'
    elif IMT_designation == data[3][1] or IMT_designation == data[4][1]:
        font_color = '#d8de26'
    else:
        font_color = '#fc120a'

    label_result = tk.Label(win,
                            text=f'Ваш ИМТ {IMT} - {IMT_designation}',
                            name='label_result',
                            font=('Comic Sans MS', 25),
                            fg=font_color,
                            bg='#fff')
    label_result.place(x=50, y=400)

    btn_close_win = tk.Button(win,
                              text='Рассчитать снова',
                              name='again',
                              bg='#93fa89',
                              relief='groove',
                              font=('Comic Sans MS', 15),
                              command=lambda win_func=win: close_win(win_func))
    btn_close_win.place(x=500, y=10)

    # меняем язык на англ., если он стоял на главном окне
    current_lang = root.nametowidget(btn_lang)['text']
    if current_lang == 'en':
        win_change_lang(IMT, IMT_designation)


def calc_imt():  # Расчёт ИМТ
    m = input_weight.get()
    h = input_height.get()
    if m.count('.') <= 1 and h.count('.') <= 1 and len(m) != 0 and len(h) != 0 and (m[0] != '0' or m[1] == '.') \
            and h[0] != '0' and m[0] != '.' and h[0] != '.' and float(h) > 0:  # доп. проверка на корректность
        # введённых пользователем данных
        if m[-1] == '.':
            m = m[:-1]
        if h[-1] == '.':
            h = h[:-1]
        m = round(float(m), 1)
        h = float(h)
        h_meters = round((h / 100) ** 2, 4)
        ans = round(m / h_meters, 2)  # Результат, полученный по формуле Адольфа Кетле
        if ans <= 16:
            ans_designation = 'Выраженный дефицит \n массы тела'
        elif 16 < ans <= 18.5:
            ans_designation = 'Недостаточная (дефицит) \n масса тела'
        elif 18.5 < ans <= 25:
            ans_designation = 'Норма'
        elif 25 < ans <= 30:
            ans_designation = 'Избыточная масса \n тела (предожирение)'
        elif 30 < ans <= 35:
            ans_designation = 'Ожирение 1 степени'
        elif 35 < ans < 40:
            ans_designation = 'Ожирение 2 степени'
        else:
            ans_designation = 'Ожирение 3 степени'
        new_win(ans, ans_designation)


btn_lang = tk.Button(root,
                     text='рус',
                     name='lang',
                     relief='groove',
                     bg='#fff',
                     font=('Comic Sans MS', 15),
                     command=change_lang
                     )
btn_lang.place(x=20, y=10, width=100, height=40)

label_weight = tk.Label(root,
                        name='weight_text',
                        text='Введите вес (в кг):',
                        bg='#fff',
                        font=('Comic Sans MS', 20),
                        )

label_weight.place(x=150, y=160)

label_height = tk.Label(root,
                        text='Введите рост (в см):',
                        name='height_text',
                        bg='#fff',
                        font=('Comic Sans MS', 20)
                        )

label_height.place(x=150, y=260)

input_weight = tk.Entry(root,
                        bg='#fff',
                        font=('Comic Sans MS', 20),
                        width=10,
                        fg='#93fa89',
                        validate="key",  # валидация введённых данных
                        validatecommand=check
                        )

input_weight.place(x=500, y=160)

input_height = tk.Entry(root,
                        bg='#fff',
                        font=('Comic Sans MS', 20),
                        width=10,
                        fg='#93fa89',
                        validate="key",
                        validatecommand=check
                        )
input_height.place(x=500, y=260)


btn_calc = tk.Button(root,
                     text='Рассчитать ИМТ',
                     name='calc',
                     bg='#93fa89',
                     relief='groove',
                     font=('Comic Sans MS', 20),
                     command=calc_imt
                     )
btn_calc.place(x=280, y=360)

root.mainloop()
