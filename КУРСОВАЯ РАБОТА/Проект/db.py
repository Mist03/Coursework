import sqlite3


class DB1:
    
    def __init__(self):
        # Создаем подключение к БД
        self.conn = sqlite3.connect('Sports_store_customer.db')
        self.cur = self.conn.cursor()
        self.selected_item = 0

        # Создаем таблицу Assortment(Ассортимент)
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS Assortment (ID_1 integer primary key AUTOINCREMENT NULL, 'Наименование' text, 'Цена' text, 'Количество' INT DEFAULT 1)''')
        
        # Создаем таблицу Shopping_cart(Корзина покупок)
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS Shopping_cart (ID_2 integer primary key AUTOINCREMENT NULL, 'Наименование' text, 'Цена' text, 'Количество' INT )''')
        
        # Создаем таблицу Workers(Работники)
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS Workers (ID_3 integer primary key AUTOINCREMENT NULL, 'Фамилия' text, 'Имя' text, 'Должность' text)''')
        self.conn.commit()

    def insertDataAssortment(self, Name, Price, Quantity):
        ''' Добавление данных для Assortment '''
        self.cur.execute(
            '''INSERT INTO Assortment('Наименование', 'Цена', 'Количество') VALUES (?, ?, ?)''', (Name, Price, Quantity))
        self.conn.commit()

        
    def insertDataWorkers(self, Surname, Name, Post):
        ''' Добавление данных для Workers '''
        self.cur.execute(
            '''INSERT INTO Workers('Фамилия', 'Имя', 'Должность') VALUES (?, ?, ?)''', (Surname, Name, Post))
        self.conn.commit()

    #Функции DB (Ассортимент)
    def records1(self, Name, Price, Quantity):
        ''' Ввод новых данных '''
        self.insertDataAssortment(Name, Price, Quantity)

    def updateRecord1(self, Name, Price, Quantity, ID_1):
        ''' Редактирование данных '''
        self.cur.execute(
            '''UPDATE Assortment SET 'Наименование'=?, 'Цена'=?, 'Количество'=? WHERE ID_1=?''', (Name, Price, Quantity, ID_1))
        self.conn.commit()

    def deleteRecords1(self, ID_1):
        ''' Удаление результата '''
        self.cur.execute(
            '''DELETE FROM Assortment WHERE ID_1=?''', (ID_1,))
        self.conn.commit()
    
    def addcart(self, ID_1):
        ''' Добавление товара в корзину '''
        self.cur.execute(f'''INSERT INTO Shopping_cart SELECT NULL, Наименование, Цена, Количество FROM Assortment WHERE ID_1=?''', (ID_1,))
        #[self.variable.append(row) for row in self.db.cur.fetchall()]   # записываем новый результат
        self.conn.commit()

    #Функции DB (Корзина покупок)
    def records2(self, Name, Price, Quantity):
        ''' Ввод новых данных '''
        self.insertDataShopping_cart(Name, Price, Quantity)

    def updateRecord2(self, Quantity, ID_2):
        ''' Редактирование данных '''
        self.cur.execute(
            '''UPDATE Shopping_cart SET 'Количество'=?  WHERE ID_2=?''', (Quantity, ID_2))
        self.conn.commit()

    def deleteRecords2(self, ID_2):
        ''' Удаление результата '''
        self.cur.execute(
            '''DELETE FROM Shopping_cart WHERE ID_2=?''', (ID_2,))
        self.conn.commit()
        
    #Функции DB (Работники)
    def records3(self, Surname, Name, Post):
        ''' Ввод новых данных '''
        self.insertDataWorkers(Surname, Name, Post)

    def updateRecord3(self, Surname, Name, Post, ID_3):
        ''' Редактирование данных '''
        self.cur.execute(
            '''UPDATE Workers SET 'Фамилия'=?, 'Имя'=?, 'Должность'=? WHERE ID_3=?''', (Surname, Name, Post, ID_3))
        self.conn.commit()

    def deleteRecords3(self, ID_3):
        ''' Удаление результата '''
        self.cur.execute(
            '''DELETE FROM Workers WHERE ID_3=?''', (ID_3,))
        self.conn.commit()

        
