from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
import datetime

from models.user import UserModel
from models.auth import Auth

def parse_date(data):
    y, m, d = data['date_of_birth'].split('-') # Convert date request to a python date object
    return datetime.datetime(int(y), int(m), int(d))

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Enter your username. This field cannot be left blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Enter your account password."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if Auth.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 409
        user = Auth(**data)
        try:
            user.save_to_db()
        except:
            return {'message': 'Something went wrong.'}
        return {'message': 'User created successfully.'}, 201

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'firstname', 
        type=str,
        required=True,
        help="Enter user's first name."

    )
    parser.add_argument(
        'lastname',
        type=str,
        required=True,
        help="Enter user's last name."
    )
    parser.add_argument(
        'gender',
        type=str,
        required=True,
        help="Enter user's gender."
    )
    parser.add_argument(
        'date_of_birth',
        type=str,
        required=True,
        help="Enter user's date of birth."
    )

    @jwt_required()
    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json(), 200
        return {'message': f'User not found'}, 404
    
    @jwt_required()
    def put(self, id):
        data = self.parser.parse_args()
        dob = parse_date(data)
        user = UserModel.find_by_id(id)
        if user is None:
            new_user = UserModel(data['firstname'], data['lastname'], data['gender'], dob)
            new_user.save_to_db()
            return new_user.json(), 201 
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.gender = data['gender']
        user.date_of_birth = dob
        user.save_to_db()
        return user.json(), 200
    
    @jwt_required()
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user is None:
            return {'message': 'User does not exist'}, 404
        user.delete_from_db()
        return {'message': 'Deleted successfully.'}, 200


class UserList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'firstname', 
        type=str,
        required=True,
        help="Enter user's first name."

    )
    parser.add_argument(
        'lastname',
        type=str,
        required=True,
        help="Enter user's last name."
    )
    parser.add_argument(
        'gender',
        type=str,
        required=True,
        help="Enter user's gender."
    )
    parser.add_argument(
        'date_of_birth',
        type=str,
        required=True,
        help="Enter user's date of birth."
    )
    
    @jwt_required()
    def get(self):
        args = request.args
        filter_field = args.get('filter_field')
        filter_value = args.get('filter_value')
        sort_field = args.get('sort_field')
        if filter_field:
            return UserModel.filter_by_parameters(filter_field, filter_value, sort_field)
        return {'users': [user.json() for user in UserModel.query.order_by(sort_field).all()]}
        
    @jwt_required()
    def post(self):
        data = UserList.parser.parse_args()
        try:
            dob = parse_date(data)
            user = UserModel(data['firstname'], data['lastname'], data['gender'], dob)
            user.save_to_db()
        except:
            return {'message': 'Something went wrong.'}, 500
        return user.json(), 201