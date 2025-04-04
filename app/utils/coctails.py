from flask import current_app, request, jsonify
from app.models import Ingridient, Coctail

def getCoctailPrice(content):
    price = 0
    for ingridient in content:
        try:
            ingr = Ingridient.query.filter_by(name=ingridient['name']).first()
            print(ingr.name + " " + ingridient['volume'])
            if not ingr:
                return jsonify({"error": f"Ingridient {ingridient['name']} not found"}), 400
            if not ingridient['volume']:
                return jsonify({"error": f"Ingridient {ingridient['name']} volume is required"}), 400
            
            price += ingr.price * float(ingridient['volume'])
        except Exception as e:
            # удалить позже
            return jsonify({"error": f"Error parsing ingridients: {e}"}), 500
        
    return price

def getCoctailDegree(content):
    pass