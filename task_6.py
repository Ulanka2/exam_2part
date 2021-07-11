import psycopg2

def executor(method):
    def wrapper(*args, **kwargs):
        args[0].cursor = args[0].connection.cursor()
        rec = method(*args, **kwargs)
        args[0].cursor.close()
        return rec
    return wrapper

class User:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname='titanic', user='myuser', password='1234')
            self.connection.autocommit = True
            self.create_table()
        except Exception as e:
            print(f"Cannot connect to database, plese check {e} error")

    @executor
    def create_table(self):
        try:
            create_table_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR (50) UNIQUE, name varchar(100), surname varchar(100), age integer NOT NULL)"
            self.cursor.execute(create_table_command)
        except Exception as e:
            print(f"table creation failed because {e}")

    
    @executor
    def insert_record(self, username, name, surname, age): #для заполнения таблицы
        new_record = (username, name, surname, age)
        insert_command = "INSERT INTO users(username, name, surname, age) VALUES('" + new_record[0] + "','" + new_record[1] + "','" + new_record[2] + "','" + new_record[3] + "') "
        self.cursor.execute(insert_command)

    @executor
    def find_record(self, username):
        search_record = (username)
        search_command = "SELECT * FROM users WHERE id = '" + search_record + "'"
        self.cursor.execute(search_command)
        found_record = self.cursor.fetchall()
        return found_record
    

    @executor
    def query_all(self, username):
        search_record = (username)
        query_all =  search_record 
        self.cursor.execute(query_all)
        users = self.cursor.fetchall()
        return users

class Post:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname='titanic', user='myuser', password='1234')
            self.connection.autocommit = True
            self.create_table()
        except Exception as e:
            print(f"Cannot connect to database, plese check {e} error")

    @executor
    def create_table(self):
        try:
            create_table_command = "CREATE TABLE IF NOT EXISTS posty(id serial PRIMARY KEY, postname VARCHAR (255) NOT NULL, posting_date DATE NOT NULL DEFAULT CURRENT_DATE)"
            self.cursor.execute(create_table_command)
        except Exception as e:
            print(f"table creation failed because {e}")

    
    @executor
    def insert_record(self, postname):
        new_record = (postname)
        insert_command = "INSERT INTO posty(postname) VALUES('" + new_record + "') "
        self.cursor.execute(insert_command)

    @executor
    def find_posty(self, posty):
        search_record = (posty)
        search_command = "SELECT * FROM posty WHERE id = '" + search_record + "'"
        self.cursor.execute(search_command)
        found_record = self.cursor.fetchall()
        return found_record

    @executor
    def quer_all(self, username):
        search_record = (username)
        quer_all =  search_record 
        self.cursor.execute(quer_all)
        users = self.cursor.fetchall()
        return users

class Blog():
    users = User()
    posty = Post()

    def show(self):
        print(self.users.query_all("SELECT * FROM users"),self.posty.quer_all("SELECT * FROM posty"))

    def get_user(self):
        return self.users.find_record('1')

    def get_posty(self):
        return self.posty.find_posty('1')
    

b = Blog()
b.show() #1.all()получает все записи таблицы
print(b.get_user())#2.get(id=1) получает конкретную запись по 1 параметру
print(b.get_posty())#2.get(id=1) получает конкретную запись по 1 параметру
print(b.get_user(),b.get_posty())#3.select_related("user").get(id=1)** конкретную запись блога для определенного пользователя
#не получилос сделать #filter(“поле”) возвращает отсортированные записи по одному из полей указанных в скобках 

# db = User()
# db.create_table()
# db.insert_record("nikname", "ukuk", "satinbaev", "25")
# ps = Post()
# ps.create_table()
# ps.insert_record("его пост")
