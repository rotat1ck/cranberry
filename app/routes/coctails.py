from flask import Blueprint, jsonify, request
from app.utils.jwtdec import token_required
from app.models import db, User, Ingridient, CustomCoctail, Coctail
from app.utils.coctails import getCoctailPrice, getCoctailContent, getCoctailDegree
import json

coctails_bp = Blueprint("/api/coctails", __name__)

@coctails_bp.route('/getmenu', methods=['GET'])
def getMenu():
    coctails = Coctail.query.all()
    return jsonify([{"id": coctail.id, "name": coctail.name, "glass": coctail.glass,
                    "description": coctail.description, "price": coctail.price,
                    "content": coctail.content, "degrees": round(coctail.degrees, 2)} for coctail in coctails])

@coctails_bp.route('/getcoctails', methods=['GET'])
@token_required
def getCoctails(user):
    userCoctails = CustomCoctail.query.filter_by(owner=user.id)
    return jsonify([{"id": coctail.id, "name": coctail.name, "glass": coctail.glass,
                    "description": coctail.description, "price": coctail.price,
                    "content": coctail.content, "degrees": round(coctail.degrees, 2)} for coctail in userCoctails])

@coctails_bp.route('/getingridients', methods=['GET'])
def getIngridients():
    ingridients = Ingridient.query.all()
    return jsonify([{"id": ingridient.id, "name": ingridient.name, "price": ingridient.price, "degrees": ingridient.degrees} for ingridient in ingridients])

@coctails_bp.route("/addcoctail", methods=['POST'])
@token_required
def createCoctail(user):
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    glass = request.json.get('glass')
    if not glass:
        return jsonify({"error": "Glass type is required"}), 400
    
    description = request.json.get('description')
    if not description:
        return jsonify({"error": "Description is required"}), 400
    
    contentReceived = request.json.get('content')
    if not contentReceived:
        return jsonify({"error": "Content is required"}), 400
    
    content = contentReceived['ingridients']
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
    ​
2
    degreesResult = getCoctailDegree(content)
3
    if isinstance(degreesResult, tuple) and degreesResult[0].is_json:
4
        return degreesResult
5
    
6
    coctail = CustomCoctail(name=name, owner=user.id, glass=glass, description=description, price=priceResult
7
                    , content=contentResult, degrees=degreesResult)
8
    db.session.add(coctail)
9
    db.session.commit()
10
    
11
    return jsonify({"id": coctail.id, "name": coctail.name, "glass": coctail.glass,
12
                    "description": coctail.description, "price": coctail.price,
13
                    "content": coctail.content, "degrees": coctail.degrees}), 200
14
​
15
@coctails_bp.route('/deletecoctail/<int:coctailId>', methods=['DELETE'])    
16
@token_required
17
def deleteCoctail(user, coctailId):
18
    userCoctails = CustomCoctail.query.filter_by(id=coctailId).first()
19
    if not userCoctails:
20
        return jsonify({"error": "Coctail not found"}), 404
21
    
22
    db.session.delete(userCoctails)
23
    db.session.commit()
24
    return jsonify({"message": f"Coctail {userCoctails.name} deleted"}),
    coctail = CustomCoctail(name=name, owner=user.id, glass=glass, description=description, price=priceResult
                    , content=contentResult, degrees=degreesResult)
    db.session.add(coctail)
    db.session.commit()
    
    return jsonify({"id": coctail.id, "name": coctail.name, "glass": coctail.glass,
                    "description": coctail.description, "price": coctail.price,
                    "content": coctail.content, "degrees": coctail.degrees}), 200

@coctails_bp.route('/deletecoctail/<int:coctailId>', methods=['DELETE'])    
@token_required
def deleteCoctail(user, coctailId):
    userCoctails = CustomCoctail.query.filter_by(id=coctailId).first()
    if not userCoctails:
        return jsonify({"error": "Coctail not found"}), 404
    
    db.session.delete(userCoctails)
    db.session.commit()
    return jsonify({"message": f"Coctail {userCoctails.name} deleted"}),