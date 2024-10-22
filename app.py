from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku 
from flask_marshmallow import Marshmallow
import os

# my capstone backend
app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dxfeaqxcbaxevu:b03a5b3e9ef19f143d3b8205073db7529d1bc29ffada06de23d30e1176f060a8@ec2-184-73-209-230.compute-1.amazonaws.com:5432/d11r6bgm47hok9'

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Guide(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(19), unique=False)
    lastname = db.Column(db.String(19), unique=False)
    email = db.Column(db.String(25), unique=False)
    phone = db.Column(db.String(14), unique=False)
    notes= db.Column(db.String(150), unique=False)

    def __init__(self, firstname, lastname, email, phone, notes):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.notes= notes


class GuideSchema(ma.Schema):
    class Meta:
        fields = ('firstname', 'lastname', 'email', 'phone', 'notes')


guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)


# *end point/
@app.route('/guide', methods=["POST"])
def add_guide():
    firstname= request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']
    notes = request.json['notes']
    

    new_guide = Guide(firstname, lastname, email, phone, notes)

    db.session.add(new_guide)
    db.session.commit()

    guide = Guide.query.get(new_guide.id)

    return guide_schema.jsonify(guide)


#endpoint query guides
@app.route("/guides", methods=["GET"])
def get_guides():
    all_guides = Guide.query.all()
    result = guides_schema.dump(all_guides)
    return jsonify(result)


# Endpoint for querying a single guide
@app.route("/guide/<id>", methods=["GET"])
def get_guide(id):
    guide = Guide.query.get(id)
    return guide_schema.jsonify(guide)


# Endpoint for updating a guide
@app.route("/guide/<id>", methods=["PUT"])
def guide_update(id):
    guide = Guide.query.get(id)
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']
    notes = request.json['notes']

    guide.firstname = firstname
    guide.lastname = lastname
    guide.email = email
    guide.phone = phone
    guide.notes = notes

    db.session.commit()
    return guide_schema.jsonify(guide)


# Endpoint for deleting a record
@app.route("/guide/<id>", methods=["DELETE"])
def guide_delete(id):
    guide = Guide.query.get(id)
    db.session.delete(guide)
    db.session.commit()

    return guide_schema.jsonify(guide)


if __name__ == '__main__':
    app.run(debug=True)