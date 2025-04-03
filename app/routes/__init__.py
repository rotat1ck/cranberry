from flask import Blueprint, request, jsonify, render_template

default_bp = Blueprint('/', __name__)

@default_bp.route('/', methods=['GET'])
def indexPage():
    return render_template('index.html')