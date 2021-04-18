from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://myk_user:fwQH-totF8Pv@localhost:3306/lab6'
DB = SQLAlchemy(APP)
MA = Marshmallow(APP)


class Fish(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    weight_in_kg = DB.Column(DB.Float)
    thermoregulation = DB.Column(DB.String(15))
    lifetime_years = DB.Column(DB.Float)
    animal_type = DB.Column(DB.String(50))
    required_aquarium_capacity_liters = DB.Column(DB.Float)
    required_temperature = DB.Column(DB.Integer)
    required_lighting_level = DB.Column(DB.String(20))

    def __init__(
            self, weight_in_kg, thermoregulation, lifetime_years, animal_type,
            required_aquarium_capacity_liters, required_temperature, required_lighting_level
    ):
        self.weight_in_kg = weight_in_kg
        self.thermoregulation = thermoregulation
        self.lifetime_years = lifetime_years
        self.animal_type = animal_type
        self.required_aquarium_capacity_liters = required_aquarium_capacity_liters
        self.required_temperature = required_temperature
        self.required_lighting_level = required_lighting_level


class FishSchema(MA.Schema):
    id = fields.Int()
    weight_in_kg = fields.Float()
    thermoregulation = fields.String()
    lifetime_years = fields.Float()
    animal_type = fields.String()
    required_aquarium_capacity_liters = fields.Integer()
    required_temperature = fields.Integer()
    required_lighting_level = fields.String()


FISH_SCHEMA = FishSchema(exclude=["id"])
FISH_LIST_SCHEMA = FishSchema(only=["id", "animal_type", "lifetime_years"], many=True)


@APP.route('/')
def welcome_page():
    return 'Welcome to the zoo aquariums!'


@APP.route('/fish', methods=['GET'])
def get_all_fish():
    all_fish_list = Fish.query.all()
    return FISH_LIST_SCHEMA.jsonify(all_fish_list)


@APP.route('/fish/<id>', methods=['GET'])
def get_fish(id):
    searched_fish = Fish.query.get(id)
    if not searched_fish:
        return abort(404)
    return FISH_SCHEMA.jsonify(searched_fish)


@APP.route('/fish', methods=['POST'])
def add_fish():
    try:
        received_deserialized_values = FISH_SCHEMA.load(request.json)
    except ValidationError:
        return abort(400)
    new_incoming_fish = Fish(**received_deserialized_values)
    DB.session.add(new_incoming_fish)
    DB.session.commit()
    return FISH_SCHEMA.jsonify(new_incoming_fish), 201


@APP.route('/fish/<id>', methods=['PUT'])
def update_fish(id):
    changed_fish = Fish.query.get(id)
    if not changed_fish:
        return abort(404)
    try:
        new_deserialized_values = FISH_SCHEMA.load(request.json)
    except ValidationError:
        return abort(400)
    for fish_obj_updated_field, incoming_deserialized_value in new_deserialized_values.items():
        setattr(changed_fish, fish_obj_updated_field, incoming_deserialized_value)
    DB.session.commit()
    return FISH_SCHEMA.jsonify(changed_fish)


@APP.route('/fish/<id>', methods=['DELETE'])
def delete_fish(id):
    fish_to_delete = Fish.query.get(id)
    if not fish_to_delete:
        return abort(404)
    DB.session.delete(fish_to_delete)
    DB.session.commit()
    return FISH_SCHEMA.jsonify(fish_to_delete), 204


if __name__ == "__main__":
    APP.run(debug=True)
