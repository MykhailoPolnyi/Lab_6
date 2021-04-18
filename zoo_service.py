from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
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


class FishSchema(ma.Schema):
    id = fields.Int()
    weight_in_kg = fields.Float()
    thermoregulation = fields.String()
    lifetime_years = fields.Float()
    animal_type = fields.String()
    required_aquarium_capacity_liters = fields.Integer()
    required_temperature = fields.Integer()
    required_lighting_level = fields.String()


fish_schema = FishSchema(exclude=["id"])
fishes_schema = FishSchema(only=["id", "animal_type", "lifetime_years"], many=True)


@app.route('/')
def hello_page():
    return 'Hello to the zoo aquariums!'


@app.route('/fish', methods=['GET'])
def get_all_fish():
    all_fish = Fish.query.all()
    return fishes_schema.jsonify(all_fish)


@app.route('/fish/<id>', methods=['GET'])
def get_fish(id):
    fish = Fish.query.get(id)
    if not fish:
        return abort(404)
    return fish_schema.jsonify(fish)


@app.route('/fish', methods=['POST'])
def add_fish():
    try:
        params = fish_schema.load(request.json)
        new_fish = Fish(**params)
    except:
        return abort(400)
    db.session.add(new_fish)
    db.session.commit()
    return fish_schema.jsonify(new_fish), 201


@app.route('/fish/<id>', methods=['PUT'])
def update_fish(id):
    fish = Fish.query.get(id)
    if not fish:
        return abort(404)
    try:
        new_params = fish_schema.load(request.json)
    except ValidationError:
        return abort(400)
    for param in new_params:
        setattr(fish, param, request.json[param])
    db.session.commit()
    return fish_schema.jsonify(fish)


@app.route('/fish/<id>', methods=['DELETE'])
def delete_fish(id):
    fish = Fish.query.get(id)
    if not fish:
        return abort(404)
    db.session.delete(fish)
    db.session.commit()
    return fish_schema.jsonify(fish), 204


if __name__ == "__main__":
    app.run(debug=True)
