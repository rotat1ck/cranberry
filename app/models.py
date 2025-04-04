from .config import db # импортируем базу данных из config.py

# этот класс нужен для создания таблицы в базе по его свойствам
# т.е. такие же столбцы будут созданы в базе, на основе находящихся классов в этом файле
class User(db.Model):
    __tablename__ = 'users' # название таблицы
    id = db.Column(db.Integer, primary_key=True) # id пользователя
    username = db.Column(db.String(80), unique=True, nullable=False) # имя пользователя
    hash = db.Column(db.String(120), nullable=False) # захэшированный пароль

class Ingridient(db.Model):
    __tablename__ = 'ingridients' # название таблицы
    id = db.Column(db.Integer, primary_key=True) # id ингридиента
    name = db.Column(db.String(80), unique=True, nullable=False) # название инг
    price = db.Column(db.Float, nullable=False) # цена ингридиента
    degrees = db.Column(db.Integer, nullable=False)

class Coctail(db.Model):
    __tablename__ = 'coctails' # название таблицы
    id = db.Column(db.Integer, primary_key=True) # id коктейля
    name = db.Column(db.String(80), nullable=False) # название кок
    glass = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False) # описание кок
    price = db.Column(db.Float, nullable=False) # цена кок
    content = db.Column(db.String(300), nullable=False)
    degrees = db.Column(db.Integer, nullable=False)

class CustomCoctail(db.Model):
    __tablename__ = 'custom_coctails' # название таблицы
    id = db.Column(db.Integer, primary_key=True) # id коктейля
    owner = db.Column(db.Integer, db.ForeignKey('users.id')) # id пользователя, который создал коктейль
    name = db.Column(db.String(80), nullable=False) # название кок
    glass = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False) # описание кок
    price = db.Column(db.Float, nullable=False) # цена кок
    content = db.Column(db.String(300), nullable=False)
    degrees = db.Column(db.Integer, nullable=False)