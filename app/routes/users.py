from flask import Blueprint, jsonify, request 
# Blueprint: создание префикса для конечной точки
# jsonify: преобразование данных в JSON
# request: доступ к данным запроса
from app.models import db, User, Ingridient
# db: объект базы данных
# User: модель пользователя
from app.utils.jwtdec import token_required, create_token
from app.utils.coctails import getCoctailPrice, getCoctailContent, getCoctailDegree
# token_required: декоратор ограничивающий конечную точку только для авторизированных пользователей
# create_token: функция генерации токена
import json


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


@users_bp.route("/addcoctail", methods=['POST'])
@token_required
def createCoctail(user):
    name = request.form.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    glass = request.form.get('glass')
    if not glass:
        return jsonify({"error": "Glass type is required"}), 400
    
    description = request.form.get('description')
    if not description:
        return jsonify({"error": "Description is required"}), 400
    
    contentReceived = request.form.get('content')
    if not contentReceived:
        return jsonify({"error": "Content is required"}), 400
    
    content = json.loads(contentReceived)['ingridients']
    if not content:
        return jsonify({"error": "Content parse error"}), 400
    
    contentResult = getCoctailContent(content)
    if isinstance(contentResult, tuple) and contentResult[0].is_json:
        return contentResult

    priceResult = getCoctailPrice(content)
    if isinstance(priceResult, tuple) and priceResult[0].is_json:
        return priceResult
    
    print(contentResult)
    print(priceResult)
    return jsonify({"message": f"Coctail {name} created"}), 200