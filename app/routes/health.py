from flask import Blueprint, jsonify, request 
# Blueprint: создание префикса для конечной точки
# jsonify: преобразование данных в JSON
# request: доступ к данным запроса
from app.utils.jwtdec import token_required
# token_required: декоратор ограничивающий конечную точку только для авторизированных пользователей
# create_token: функция генерации токена

health_bp = Blueprint("/api/health", __name__)

@health_bp.route("/checkserver", methods=["GET"])
def checkServer():
    return jsonify({"message": "Server is active"}), 200


@health_bp.route("/checktoken", methods=['GET'])
@token_required
def checkToken(user):
    return jsonify({"message": "Valid token"}), 200