import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister

from resources.user import UserList, User

from security import authenticate, identify
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') 
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

api = Api(app)
db.init_app(app)

jwt = JWT(app, authenticate, identify)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(User, '/users/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5002)