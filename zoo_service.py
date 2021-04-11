from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://myk_user:fwQH-totF8Pv@localhost:3306/lab6'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight_in_kg = db.Column(db.Float)
    thermoregulation = db.Column(db.String(15))
    lifetime_years = db.Column(db.Float)
    animal_type = db.Column(db.String(50))
    required_aquarium_capacity_liters = db.Column(db.Float)
    required_temperature = db.Column(db.Integer)
    required_lighting_level = db.Column(db.String(20))

    def __init__(self, weight, thermoregulation, lifetime, fish_type, req_aq_capacity, req_temperature, req_lighting_lvl):
        self.weight_in_kg = weight
        self.thermoregulation = thermoregulation
        self.lifetime_years = lifetime
        self.animal_type = fish_type
        self.required_aquarium_capacity_liters = req_aq_capacity
        self.required_temperature = req_temperature
        self.required_lighting_level = req_lighting_lvl


class FishSchema(ma.Schema):
    class Meta:
        fields = (
            'weight_in_kg', 'thermoregulation', 'lifetime_years', 'animal_type',
            'required_aquarium_capacity_liters', 'required_temperature', 'required_lighting_level'
        )


fish_schema = FishSchema()
fishes_schema = FishSchema(many=True)


@app.route('/')
def hello_page():
    return 'Hello to the zoo aquariums!'


@app.route('/fish', methods=['GET'])
def get_all_fish():
    all_fish = Fish.query.all()
    result = fishes_schema.dump(all_fish)
    return jsonify(result)


@app.route('/fish/<id>', methods=['GET'])
def get_fish(id):
    fish = Fish.query.get(id)
    return fish_schema.jsonify(fish)


@app.route('/fish', methods=['POST'])
def add_fish():
    weight = request.json['weight_in_kg']
    thermoregulation = request.json['thermoregulation']
    lifetime = request.json['lifetime_years']
    animal_type = request.json['animal_type']
    required_aq_capacity = request.json['required_aquarium_capacity_liters']
    required_temperature = request.json['required_temperature']
    required_lighting_level = request.json['required_lighting_level']

    new_fish = Fish(
        weight, thermoregulation, lifetime, animal_type,
        required_aq_capacity, required_temperature, required_lighting_level
    )

    db.session.add(new_fish)
    db.session.commit()

    return fish_schema.jsonify(new_fish)


@app.route('/fish/<id>', methods=['PUT'])
def update_fish(id):
    def try_upd(updated_obj, updated_param):
        try:
            new_value = request.json[updated_param]
            setattr(updated_obj, updated_param, new_value)
        except KeyError:
            pass
    fish = Fish.query.get(id)
    try_upd(fish, 'weight_in_kg')
    try_upd(fish, 'thermoregulation')
    try_upd(fish, 'lifetime_years')
    try_upd(fish, 'animal_type')
    try_upd(fish, 'required_aquarium_capacity_liters')
    try_upd(fish, 'required_temperature')
    try_upd(fish, 'required_lighting_level')

    db.session.commit()

    return fish_schema.jsonify(fish)


@app.route('/fish/<id>', methods=['DELETE'])
def delete_fish(id):
    fish = Fish.query.get(id)
    db.session.delete(fish)
    db.session.commit()

    return fish_schema.jsonify(fish)


if __name__ == "__main__":
    app.run(debug=True)
