"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    response_body = User.query.all()
    return jsonify(list(map(lambda x:x.serialize(), response_body ))), 200

@app.route('/user', methods=['POST'])
def add_user():
    body_request = request.get_json()

    name = body_request.get("name", None)
    email = body_request.get("email", None)
    password = body_request.get("password", None)
    last_name = body_request.get("last_name", None)

    
    new_user = User(
        name = name,
        email = email,
        password = password,
        last_name = last_name)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg":  "Usuario creado exitosamente"}), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    response_body = Characters.query.all()
    character_list=[]
    return jsonify({"character_list":list(map(lambda x:x.serialize(), response_body))}), 200

@app.route('/characters', methods=['POST'])
def add_character():
    body_request = request.get_json()

    name = body_request.get("name", None)
    gender = body_request.get("gender", None)
    height = body_request.get("height", None)

    
    new_character = Characters(
        name = name,
        gender = gender,
        height = height,
        )

    db.session.add(new_character)
    db.session.commit()

    return jsonify({"msg":  "Personaje creado exitosamente"}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    response_body = Planets.query.all()

    return jsonify({"planet_list" : list(map(lambda x:x.serialize(), response_body))}), 200

@app.route('/planets', methods=['POST'])
def add_planets():
    body_request = request.get_json()

    name = body_request.get("name", None)
    climate = body_request.get("climate", None)
    population = body_request.get("population", None)

    
    new_planet = Planets(
        name = name,
        climate = climate,
        population = population,
        )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg":  "Planeta creado exitosamente"}), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    body = request.get_json()
    single_character = Characters.query.get(character_id)
    return jsonify(single_character.serialize()), 200    

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    body = request.get_json()
    single_planet = Planets.query.get(planet_id)
    return jsonify(single_planet.serialize()), 200

   # Favorites -------------------------------------------------------------

@app.route('/favorites', methods=['GET'])
def get_favorites():
    response_body = Characters.query.all()
    characters_list = []

    return jsonify({"characters_list" : list(map(lambda x:x.serialize(), req))}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
