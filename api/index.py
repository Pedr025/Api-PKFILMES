from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

def load_data():
    json_path = os.path.join(os.getcwd(), 'movies_data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/all', methods=['GET'])
def get_all():
    all_data = load_data()
    simplified_data = []
    for item in all_data:
        simplified_data.append({
            "id": item.get("id"),
            "titulo": item.get("titulo"),
            "capa": item.get("capa"),
            "trailer_id": item.get("trailer_id"),
            "generos": item.get("generos")
        })
    return jsonify(simplified_data)

@app.route('/details/<string:item_id>', methods=['GET'])
def get_details(item_id):
    all_data = load_data()
    item = next((item for item in all_data if str(item.get("id")) == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item não encontrado"}), 404

@app.route('/genre/<string:genre_name>', methods=['GET'])
def get_by_genre(genre_name):
    all_data = load_data()
    genre_name_lower = genre_name.casefold()
    filtered_items = [
        item for item in all_data 
        if genre_name_lower in (g.strip().casefold() for g in item.get("generos", "").split(','))
    ]
    return jsonify(filtered_items)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "API de Filmes e Séries no ar!",
        "endpoints": {
            "/all": "Lista simplificada de todos os itens.",
            "/details/<id>": "Detalhes completos de um item.",
            "/genre/<genero>": "Filtra itens por gênero."
        }
    })

