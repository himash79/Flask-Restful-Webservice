from dataclasses import dataclass

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort, reqparse
import json
from marshmallow import fields
import marshmallow as ma
from sqlalchemy.ext import serializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[USERNAME]:[PASSWORD]@localhost:5432/[DATANASE]'
UPLOAD_FOLDER = 'static/resources'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)


@dataclass
class Users_user(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    image = db.Column(db.String(200))
    status = db.Column(db.String(1))

    def toJson(self):
        return jsonify(
            {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "image": self.image,
                "status": self.status
            }
        )


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id', type=str, required=True, help="id is required parameter !")
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('image', type=str)
parser.add_argument('status', type=str)


@app.route('/users', methods=['GET', 'POST'])
def users_func_01():
    if request.method == "GET":
        try:
            users = Users_user.query.order_by(Users_user.id).all()
            return [Users_user.toJson(user).json for user in users]
        except Exception as e:
            print(e)
            return "Users fetch failed !"
    elif request.method == "POST":
        try:
            args = parser.parse_args()
            new_user = Users_user(id=args['id'], name=args['name'], email=args['email'], image=args['image'],
                                  status=args['status'])
            db.session.add(new_user)
            db.session.commit()
            print("User added success !")
            return Users_user.toJson(new_user), 201
        except Exception as e:
            print(e)
            return "Users added failed !"


@app.route('/users/<string:id>', methods=['DELETE', 'PUT'])
def users_func_02(id):
    if request.method == "DELETE":
        try:
            record = Users_user.query.filter_by(id=id).first_or_404(
                description='Record with id={} is not available'.format(id))
            db.session.delete(record)
            db.session.commit()
            print("User deleted success !")
            return "User deleted success ! ", 204
        except Exception as e:
            print(e)
            return "Users deleted failed !"
    elif request.method == "PUT":
        try:
            args = parser.parse_args()
            record = Users_user.query.filter_by(id=id).first_or_404(description='Record with id={} is not available'.format(id))
            record.name = args['name']
            record.email = args['email']
            record.image = args['image']
            record.status = args['status']
            db.session.commit()
            return "User updated success ! ", 200
        except Exception as e:
            print(e)
            return "Users updated failed !"


if __name__ == '__main__':
    app.run()
