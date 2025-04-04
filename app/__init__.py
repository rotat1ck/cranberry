from flask import Flask
from .config import initConfig # <= файл конфигурации, создает базу данных и вытаскивает параметры среды
# параметры среды определяются в файле .env, его нет на гитхабе в целях безопастности сервера
from .routes import default_bp
from .routes.health import health_bp
from .routes.users import users_bp


def startApp():
    app = Flask(__name__, template_folder='front/templates', static_folder='front/static') # создание переменной приложения
    initConfig(app) # запуск файла конфигурации config.py

    app.register_blueprint(default_bp)
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(users_bp, url_prefix='/api/users') # <= обозначение префикса /api/users


    return app # возвращаем объект приложения в main.py для запуска