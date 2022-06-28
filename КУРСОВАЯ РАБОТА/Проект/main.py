# ------------------------------------ << БИБЛИОТЕКИ >> ------------------------------------- #
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from db import *


# ------------------------------------------------------------------------------------------- #


# ------------------------------------ << РАБОТА С БД >> ------------------------------------ #

# ------------------------------------------------------------------------- #

class Assortment():

    def __init__(self):
        self.db = db   # экземпляр класса DB
        self.variable = []
        self.selected_item = 0
        self.viewRecords()
        #self.funcs()

    # ------------------------ ФУНКЦИИ БД (Ассортимент) ----------------------- #
    def viewRecords(self):
        ''' Вывод данных '''
        self.db.cur.execute(
            '''SELECT * FROM Assortment''')
        self.variable.clear()   # очищаем прошлые данные (чтобы не дублировались)
        [self.variable.append(row) for row in self.db.cur.fetchall()]   # записываем новый результат

    # ------------------------- TKINTER (Ассортимент) ------------------------- #

    def tableAssortment(self):
        ''' Создание таблицу с помощью ttk.Treeview() '''
        # Задаем расположение таблицы
        frame = tk.Frame(root, width=100, height=100)
        frame.place(x=10, y=140)

        # Создаем заголовоки для таблицы
        headers = ['ID', 'Наименование', 'Цена', 'Количество']
        self.table = ttk.Treeview(frame, columns=headers, height=15, show='headings')

        self.table.column('ID', width=50, anchor='center') 
        self.table.column('Наименование', width=200, anchor='center') 
        self.table.column('Цена', width=450, anchor='center')
        self.table.column('Количество', width=100, anchor='center')
        
        for header in headers:  # заполняем заголовоки
            self.table.heading(header, text=header)
            
        for i in self.variable: # заполняем значения
            self.table.insert('', tk.END, values=i)

        # Создаем скролл для таблицы
        scroll = ttk.Scrollbar(frame, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
 
    def editAssortment(self):
        ''' Редактирование таблицы '''
        def closeFunc():
            z.destroy() # закрываем окно

        # Создаем новое окно
        z = Toplevel()
        z.geometry('225x200')
        z.title('Edit')
        z.resizable(False, False)

        # Получаем данные строки по клику
        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, option='values')

        # Заносим данные строки в переменные
        id = values[0]
        Name = values[1]
        Price = values[2]
        Quantity = values[3]

        # Создаем метки и их расположение
        Name_label = Label(z, text='Наименование').place(x=10, y=10, width=90, height=30)
        Price_label = Label(z, text='Цена').place(x=10, y=60, width=70, height=30)
        Quantity_label = Label(z, text='Количество').place(x=10, y=100, width=70, height=30)

        # Переменные для ввода значений
        Name_1 = StringVar()
        Price_2 = StringVar()
        Quantity_3 = StringVar()

        # Строки для ввода значений
        Name_entry = Entry(z, width=50, textvariable=Name_1)
        Price_entry = Entry(z, width=50, textvariable=Price_2)
        Quantity_entry = Entry(z, width=50, textvariable=Quantity_3)

        # Записываем значения из строк ввода
        Name_entry.insert(0, str(Name))
        Price_entry.insert(0, str(Price))
        Quantity_entry.insert(0, str(Quantity))

        # Задаем расположение строк ввода
        Name_entry.place(x=100, y=10, width=110, height=30)
        Price_entry.place(x=100, y=60, width=110, height=30)
        Quantity_entry.place(x=100, y=100, width=110, height=30)

        # Создаем кнопку "Редактировать"
        edit_button = Button(z, text='Редактировать', command=lambda:
                             (self.db.updateRecord1(Name_1.get(), Price_2.get(), Quantity_3.get(), id), self.viewRecords(), self.tableAssortment()))
        edit_button.place(x=10, y=160, width=100, height=30)

        # Создаем кнопку "Закрыть"
        close_button = Button(z, text='Закрыть', command=closeFunc)
        close_button.place(x=115, y=160, width=100, height=30)

    def idgive(self):
        '''  Выбор строки по id из БД '''
        self.selected_item = self.table.selection()[0]  # получаем строку
        values = self.table.item(self.selected_item, option='values')   # получаем значения строки
        give_id = values[0]   # получаем id строки
        self.db.addcart(give_id)   # добавляем строку по полученному id
        
    def linegive(self):
        self.db.selected_item   # добавляем полученную строку

              
    def idDelete(self):
        ''' Удаление строки по id из БД '''
        self.selected_item = self.table.selection()[0]  # получаем строку
        values = self.table.item(self.selected_item, option='values')   # получаем значения строки
        delete_id = values[0]   # получаем id строки
        self.db.deleteRecords1(delete_id)   # удаляем строку по полученному id
        
    def lineDelete(self):
        ''' Удаление выбранной строки из таблицы tkinter '''
        self.table.delete(self.selected_item)   # удаляем полученную строку

# ------------------------------  Корзина покупок  ------------------------------ #
# ----------------------------------------------------------------------- #
 
class Shopping_cart():

    def __init__(self):
        self.db = db   # экземпляр класса DB
        self.variable = []
        self.selected_item = 0
        self.viewRecords()

    # ------------------------- ФУНКЦИИ БД (Корзина покупок) ------------------------ #

    def viewRecords(self):
        ''' Вывод данных '''
        self.db.cur.execute(
            '''SELECT * FROM Shopping_cart''')
        self.variable.clear()   # очищаем прошлые данные (чтобы не дублировались)
        [self.variable.append(row) for row in self.db.cur.fetchall()]   # записываем новый результат

    # -------------------------- TKINTER (Корзина покупок) -------------------------- #

    def tableShopping_cart(self):
        ''' Создание таблицу с помощью ttk.Treeview() '''
        # Задаем расположение таблицы
        frame = tk.Frame(root, width=100, height=100)
        frame.place(x=10, y=140)

        # Создаем заголовоки для таблицы
        headers = ['ID', 'Наименование', 'Цена', 'Количество']
        self.table = ttk.Treeview(frame, columns=headers, height=15, show='headings')
        
        self.table.column('ID', width=50, anchor='center')
        self.table.column('Наименование', width=240, anchor='center') 
        self.table.column('Цена', width=255, anchor='center')
        self.table.column('Количество', width=255, anchor='center')

        
        for header in headers:  # заполняем заголовоки
            self.table.heading(header, text=header)
            
        for i in self.variable: # заполняем значения
            self.table.insert('', tk.END, values=i)

        # Создаем скролл для таблицы
        scroll = ttk.Scrollbar(frame, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
  
    def editShopping_cart(self):
        ''' Редактирование таблицы '''
        def closeFunc():
            z.destroy() # закрываем окно

        # Создаем новое окно
        z = Toplevel()
        z.geometry('270x100')
        z.title('Edit')
        z.resizable(False, False)

        # Получаем данные строки по клику
        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, option='values')

        # Заносим данные строки в переменные
        id = values[0]
        Quantity = values[3]


        # Создаем метки и их расположение
        Quantity_label = Label(z, text='Количество').place(x=10, y=10, width=80, height=30)


        # Переменные для ввода значений
        Quantity_3 = StringVar()

        # Строки для ввода значений
        Quantity_entry = Entry(z, width=50, textvariable=Quantity_3)

        # Записываем значения из строк ввода
        Quantity_entry.insert(0, str(Quantity))

        # Задаем расположение строк ввода
        Quantity_entry.place(x=130, y=10, width=130, height=30)

        # Создаем кнопку "Редактировать"
        edit_button = Button(z, text='Редактировать', command=lambda:
                             (self.db.updateRecord2(Quantity_3.get(), id), self.viewRecords(), self.tableShopping_cart()))
        edit_button.place(x=10, y=50, width=100, height=30)

        # Создаем кнопку "Закрыть"
        close_button = Button(z, text='Закрыть', command=closeFunc)
        close_button.place(x=115, y=50, width=100, height=30)
        
    def idDelete(self):
        ''' Удаление строки по id из БД '''
        self.selected_item = self.table.selection()[0]  # получаем строку
        values = self.table.item(self.selected_item, option='values')   # получаем значения строки
        delete_id = values[0]   # получаем id строки
        self.db.deleteRecords2(delete_id)   # удаляем строку по полученному id
        
    def lineDelete(self):
        ''' Удаление выбранной строки из таблицы tkinter '''
        self.table.delete(self.selected_item)   # удаляем полученную строку


# ------------------------------ Работники ------------------------------ #
# -------------------------------------------------------------------- #

class Workers():

    def __init__(self):
        self.db = db   # экземпляр класса DB
        self.variable = []
        self.selected_item = 0
        self.viewRecords()

    # -------------------------- ФУНКЦИИ БД (Работники) -------------------------- #
    def viewRecords(self):
        ''' Вывод данных '''
        self.db.cur.execute(
            '''SELECT * FROM Workers''')
        self.variable.clear()   # очищаем прошлые данные (чтобы не дублировались)
        [self.variable.append(row) for row in self.db.cur.fetchall()]   # записываем новый результат

    # ---------------------------- TKINTER (Работники) --------------------------- #

    def tableWorkers(self):
        ''' Создание таблицу с помощью ttk.Treeview() '''
        # Задаем расположение таблицы
        frame = tk.Frame(root, width=100, height=100)
        frame.place(x=10, y=140)

        # Создаем заголовоки для таблицы
        headers = ['ID', 'Фамилия', 'Имя','Должность']
        self.table = ttk.Treeview(frame, columns=headers, height=15, show='headings')
        
        self.table.column('ID', width=50, anchor='center')
        self.table.column('Фамилия', width=250, anchor='center') 
        self.table.column('Имя', width=250, anchor='center')
        self.table.column('Должность', width=250, anchor='center')

        
        for header in headers:  # заполняем заголовоки
            self.table.heading(header, text=header)
            
        for i in self.variable: # заполняем значения
            self.table.insert('', tk.END, values=i)

        # Создаем скролл для таблицы
        scroll = ttk.Scrollbar(frame, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
 
    def editWorkers(self):
        ''' Редактирование таблицы '''
        def closeFunc():
            z.destroy() # закрываем окно
            

        # Создаем новое окно
        z = Toplevel()
        z.geometry('260x260')
        z.title('Edit')
        z.resizable(False, False)

        # Получаем данные строки по клику
        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, option='values')

        # Заносим данные строки в переменные
        id = values[0]
        Surname = values[1]
        Name = values[2]
        Post = values[3]


        # Создаем метки и их расположение
        Surname_label = Label(z, text='Фамилия').place(x=20, y=10, width=70, height=30)
        Name_label = Label(z, text='Имя').place(x=20, y=60, width=70, height=30)
        Post_label = Label(z, text='Должность').place(x=20, y=100, width=70, height=30)


        # Переменные для ввода значений
        Surname_1 = StringVar()
        Name_2 = StringVar()
        Post_3 = StringVar()


        # Строки для ввода значений
        Surname_entry = Entry(z, width=50, textvariable=Surname_1)
        Name_entry = Entry(z, width=50, textvariable=Name_2)
        Post_entry = Entry(z, width=50, textvariable=Post_3)


        # Записываем значения из строк ввода
        Surname_entry.insert(0, str(Surname))
        Name_entry.insert(0, str(Name))
        Post_entry.insert(0, str(Post))


        # Задаем расположение строк ввода
        Surname_entry.place(x=100, y=10, width=120, height=30)
        Name_entry.place(x=100, y=60, width=120, height=30)
        Post_entry.place(x=100, y=100, width=120, height=30)


        # Создаем кнопку "Редактировать"
        edit_button = Button(z, text='Редактировать', command=lambda:
                             (self.db.updateRecord3(Surname_1.get(), Name_2.get(), Post_3.get(), id), self.viewRecords(), self.tableWorkers()))
        edit_button.place(x=10, y=220, width=100, height=30)

        # Создаем кнопку "Закрыть"
        close_button = Button(z, text='Закрыть', command=closeFunc)
        close_button.place(x=115, y=220, width=100, height=30)
        
    def idDelete(self):
        ''' Удаление строки по id из БД '''
        self.selected_item = self.table.selection()[0]  # получаем строку
        values = self.table.item(self.selected_item, option='values')   # получаем значения строки
        delete_id = values[0]   # получаем id строки
        self.db.deleteRecords3(delete_id)   # удаляем строку по полученному id
        
    def lineDelete(self):
        ''' Удаление выбранной строки из таблицы tkinter '''
        self.table.delete(self.selected_item)   # удаляем полученную строку




# ------------------------------------- << TKINTER >> --------------------------------------- #



# ----------------------------- Assortment.tk ---------------------------- #
# ------------------------------------------------------------------------- #

class tkAssortment():

    def __init__(self):
        self.sale = sale   # экземпляр класса Assortment()
        self.db = db
    def AssortmentButton(self):
        ''' Кнопка для открытия таблицы и её функций '''
        def unionFunc():
            ''' Компонует все кнопки функции выше '''
            def addWindow():
                ''' Создание нового окна для кнопки <Добавить> '''
                def closeFunc():
                    s.destroy() # закрываем окно

                # Создаем новое окно
                s = Toplevel()
                s.geometry('250x200')
                s.title('Add')
                s.resizable(False, False)

                Name_label = Label(s, text='Наименование').place(x=10, y=10, width=85, height=30)
                Price_label = Label(s, text='Цена').place(x=10, y=60, width=80, height=30)
                Quantity_label = Label(s, text='Количество').place(x=10, y=100, width=80, height=30)
                
                name_1 = StringVar()
                name_2 = StringVar()
                name_3 = StringVar()

                Name_entry = Entry(s, width=50, textvariable=name_1).place(x=130, y=10, width=100, height=30)
                Price_entry = Entry(s, width=50, textvariable=name_2).place(x=130, y=60, width=100, height=30)
                Quantity_entry = Entry(s, width=50, textvariable=name_3).place(x=130, y=100, width=100, height=30)
                
                add_button = Button(s, text='Добавить', command=lambda: 
                                    (self.db.records1(name_1.get(), name_2.get(), name_3.get()), self.sale.viewRecords(), self.sale.tableAssortment()))
                add_button.place(x=10, y=160, width=115, height=30)

                close_button = Button(s, text='Закрыть', command=closeFunc)
                close_button.place(x=130, y=160, width=80, height=30)

            self.add_image = tk.PhotoImage(file='pictures/add.png')
            Assortment_add_button = Button(root, text='Добавить', image=self.add_image, compound='top', command=addWindow)
            Assortment_add_button.place(x=10, y=50, width=100, height=80)

            self.edit_image = tk.PhotoImage(file='pictures/edit.png')
            Assortment_edit_button = Button(root, text='Редактировать', image=self.edit_image, compound='top', command=lambda:
                                             self.sale.editAssortment())
            Assortment_edit_button.place(x=120, y=50, width=100, height=80)
            
            self.delete_image = tk.PhotoImage(file='pictures/delete.png')    
            Assortment_edit_button = Button(root, text='Удалить', image=self.delete_image, compound='top', command=lambda:
                                             (self.sale.idDelete(), self.sale.lineDelete()))
            Assortment_edit_button.place(x=230, y=50, width=100, height=80)

            self.give_image = tk.PhotoImage(file='pictures/give.png')
            Assortment_addcarts_button = Button(root, text='Добавление в корзину', image=self.give_image, compound='top', command=lambda:
                                             (self.sale.idgive(), self.sale.linegive()))
            Assortment_addcarts_button.place(x=400, y=50, width=140, height=80)
            

            
        Assortment_button = Button(root, text='Assortment', command=lambda:
                                    (unionFunc(), self.sale.viewRecords(), self.sale.tableAssortment()))
        Assortment_button.place(x=10, y=10, width=100, height=30)

# ------------------------------ Shopping_cart.tk ----------------------------- #
# ------------------------------------------------------------------------- #

class tkShopping_cart():

    def __init__(self):
        self.cust = cust   # экземпляр класса Shopping_cart()
        self.db = db
    def Shopping_cartButton(self):
        ''' Кнопка для открытия таблицы и её функций '''
        def unionFunc():
            ''' Компонует все кнопки функции выше '''
            def addWindow():
                ''' Создание нового окна для кнопки <Добавить> '''
                def closeFunc():
                    s.destroy() # закрываем окно

                # Создаем новое окно
                s = Toplevel()
                s.geometry('370x150')
                s.title('Add')
                s.resizable(False, False)

                Quantity_label = Label(s, text='Добавлять в корзину можно только в таблице ассортимента').place(x=10, y=10, width=350, height=30)

                close_button = Button(s, text='Закрыть', command=closeFunc)
                close_button.place(x=60, y=100, width=250, height=30)

            self.add_image = tk.PhotoImage(file='pictures/add.png')
            Shopping_cart_add_button = Button(root, text='Добавить', image=self.add_image, compound='top', command=addWindow)
            Shopping_cart_add_button.place(x=10, y=50, width=100, height=80)

            self.edit_image = tk.PhotoImage(file='pictures/edit.png')
            Shopping_cart_edit_button = Button(root, text='Редактировать', image=self.edit_image, compound='top', command=lambda:
                                             self.cust.editShopping_cart())
            Shopping_cart_edit_button.place(x=120, y=50, width=100, height=80)
            
            self.delete_image = tk.PhotoImage(file='pictures/delete.png')    
            Shopping_cart_edit_button = Button(root, text='Удалить', image=self.delete_image, compound='top', command=lambda:
                                             (self.cust.idDelete(), self.cust.lineDelete()))
            Shopping_cart_edit_button.place(x=230, y=50, width=100, height=80)
            
            self.give_image = tk.PhotoImage(file='pictures/give.png')
            Shopping_cart_addcarts_button = Button(root, text='В этой таблице нельзя!', image=self.give_image, compound='top', command=lambda:
                                             ())
            Shopping_cart_addcarts_button.place(x=400, y=50, width=140, height=80)
               
        Shopping_cart_button = Button(root, text='Shopping_cart', command=lambda:
                                  (unionFunc(), self.cust.viewRecords(), self.cust.tableShopping_cart()))
        Shopping_cart_button.place(x=120, y=10, width=100, height=30)



# ------------------------------- Workers.tk ------------------------------- #
# ------------------------------------------------------------------------- #

class tkWorkers():

    def __init__(self):
        self.orde = orde   # экземпляр класса Workers()
        self.db = db
    def WorkersButton(self):
        ''' Кнопка для открытия таблицы и её функций '''
        def unionFunc():
            ''' Компонует все кнопки функции выше '''
            def addWindow():
                ''' Создание нового окна для кнопки <Добавить> '''
                def closeFunc():
                    s.destroy() # закрываем окно



                # Создаем новое окно
                s = Toplevel()
                s.geometry('280x270')
                s.title('Add')
                s.resizable(False, False)


                Surname_label = Label(s, text='Фамилия').place(x=20, y=10, width=70, height=30)
                Name_label = Label(s, text='Имя').place(x=20, y=60, width=70, height=30)
                Post_label = Label(s, text='Должность').place(x=20, y=100, width=70, height=30)

                
                name_1 = StringVar()
                name_2 = StringVar()
                name_3 = StringVar()


                Surname_entry = Entry(s, width=50, textvariable=name_1).place(x=130, y=10, width=120, height=30)
                Name_entry = Entry(s, width=50, textvariable=name_2).place(x=130, y=60, width=120, height=30)
                Post_entry = Entry(s, width=50, textvariable=name_3).place(x=130, y=100, width=120, height=30)

                
                add_button = Button(s, text='Добавить', command=lambda:
                                    (self.db.records3(name_1.get(), name_2.get(), name_3.get()), self.orde.viewRecords(), self.orde.tableWorkers()))
                add_button.place(x=10, y=230, width=100, height=30)

                close_button = Button(s, text='Закрыть', command=closeFunc)
                close_button.place(x=115, y=230, width=100, height=30)

            self.add_image = tk.PhotoImage(file='pictures/add.png')
            Spec_Sections_add_button = Button(root, text='Добавить', image=self.add_image, compound='top', command=addWindow)
            Spec_Sections_add_button.place(x=10, y=50, width=100, height=80)

            self.edit_image = tk.PhotoImage(file='pictures/edit.png')
            Spec_Sections_edit_button = Button(root, text='Редактировать', image=self.edit_image, compound='top', command=lambda:
                                             self.orde.editWorkers())
            Spec_Sections_edit_button.place(x=120, y=50, width=100, height=80)
            
            self.delete_image = tk.PhotoImage(file='pictures/delete.png')    
            Spec_Sections_edit_button = Button(root, text='Удалить', image=self.delete_image, compound='top', command=lambda:
                                             (self.orde.idDelete(), self.orde.lineDelete()))
            Spec_Sections_edit_button.place(x=230, y=50, width=100, height=80)

            self.give_image = tk.PhotoImage(file='pictures/give.png')
            Shopping_cart_addcarts_button = Button(root, text='В этой таблице нельзя!', image=self.give_image, compound='top', command=lambda:
                                             ())
            Shopping_cart_addcarts_button.place(x=400, y=50, width=140, height=80)

            
        Workers_button = Button(root, text='Workers', command=lambda:
                               (unionFunc(), self.orde.viewRecords(), self.orde.tableWorkers()))
        Workers_button.place(x=230, y=10, width=100, height=30)

        
# --------------------------------------- << БД >> ------------------------------------------ #
#ОТДЕЛЬНЫЙ ФАЙЛ "db"
# ------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    
    db = DB1()

    root = tk.Tk()
    root.geometry('830x485')
    root.title('Клиент спортивного магазина')
    root.resizable(False, False)

    sale = Assortment()
    cust = Shopping_cart()
    orde = Workers()

    s = tkAssortment()
    c = tkShopping_cart()
    o = tkWorkers()

    s.AssortmentButton()
    c.Shopping_cartButton()
    o.WorkersButton()


    root.mainloop()

# ------------------------------------------------------------------------------------------- #
