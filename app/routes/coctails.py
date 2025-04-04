from flask import Blueprint, jsonify, request
from app.utils.jwtdec import token_required
from app.models import db, User, Ingridient, CustomCoctail
from app.utils.coctails import getCoctailPrice, getCoctailContent, getCoctailDegree
import json

coctails_bp = Blueprint("/api/coctails", __name__)

@coctails_bp.route('/getcoctails', methods=['GET'])
@token_required
def getCoctails(user):
    userCoctails = CustomCoctail.query.filter_by(owner=user.id)
    return jsonify([{"id": coctail.id, "name": coctail.name, "glass": coctail.glass,
                    "description": coctail.description, "price": coctail.price,
                    "content": coctail.content, "degrees": coctail.degrees} for coctail in userCoctails])

@coctails_bp.route("/addcoctail", methods=['POST'])
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
    
    degreesResult = getCoctailDegree(content)
    if isinstance(degreesResult, tuple) and degreesResult[0].is_json:
        return degreesResult
    
    coctail = CustomCoctail(name=name, owner=user.id, glass=glass, description=description, price=priceResult
                    , content=contentResult, degrees=degreesResult)
    db.session.add(coctail)
    db.session.commit()
    
    return jsonify({"message": f"Coctail {name} created"}), 200

@coctails_bp.route('/deletecoctail/<int:coctailId>', methods=['DELETE'])    
@token_required
def deleteCoctail(user, coctailId):
    