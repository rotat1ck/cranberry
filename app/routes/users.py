from flask import Blueprint, jsonify, request 
# Blueprint: создание префикса для конечной точки
# jsonify: преобразование данных в JSON
# request: доступ к данным запроса
from app.models import db, User
# db: объект базы данных
# User: модель пользователя
from app.utils.jwtdec import token_required, create_token
# token_required: декоратор ограничивающий конечную точку только для авторизированных пользователей
# create_token: функция генерации токена


users_bp = Blueprint("/api/users", __name__) # <= префикс для конечной точки
# /api/users/ и так записан в __init__.py но можно дублировать для улучшения читаемости

# user_bp.route это декоратор для выполнения функции
# он примает параметр конечной точки, в данном случае /login
# и http метод(ы) какие можно использовать совершая запрос
# в сумме получиться что функция usersLogin будет вызываться при запросе на
# grape.rotatick.ru/api/users/login с http методом GET

@users_bp.route("/login", methods=["GET"])
def usersLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username: # проверка наличия имени пользователя в запросе
        return jsonify({"error": "Username is required"}), 400
    
    if not password: # проверка наличия пароля в запросе
        return jsonify({"error": "Password is required"}), 400
    
    user = User.query.filter_by(username = username).first() # ищем по имени пользователя
    if not user or user.hash != password: # проверка пользователя по имени
            return jsonify({"error": "Invalid username or password"}), 401
    
    # пользователь найден и пароль совпал
    return jsonify({"token": create_token(user.username)}), 200 # возвращаем токен пользователю

@users_bp.route('/register', methods=['POST'])
def usersRegister():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username: # проверка наличия имени пользователя в запросе
        return jsonify({"error": "Username is required"}), 400
    if not password: # проверка наличия пароля в запросе
        return jsonify({"error": "Password is required"}), 400
    
    user = User.query.filter_by(username = username).first() # ищем по имени пользователя
    if user: # проверка пользователя по имени
        return jsonify({"error": "Account with this username already exists"}), 400
    
    new = User(username = username, hash = password) # создаем нового пользователя
    db.session.add(new) # добавляем пользователя в базу данных
    db.session.commit() # сохраняем изменения в базе данных

    return jsonify({"token": create_token(username)}), 200 # возвращаем токен пользователю

