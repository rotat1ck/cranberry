from flask import current_app, request, jsonify
from app.models import Ingridient, Coctail

def getCoctailPrice(content):
    price = 
    for ingridient in content:
        try:
            ingr = Ingridient.query.filter_by(name=ingridient['name']).first()
            if not ingr:
                return jsonify({"error": f"Ingridient {ingridient['name']} not found"}), 400
            if not ingridient['volume']:
                return jsonify({"error": f"Ingridient {ingridient['name']} volume is required"}), 400
            

        except Exception as e:
            # удалить позже
            return jsonify({"error": f"Error parsing ingridients: {e}"}), 500