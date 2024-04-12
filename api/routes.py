import os
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.models import db, User, Food
import re
from utils.utils import Helpers
from config.config import Config

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/')
def index():
    return "Welcome to the Food Allergy API"
@api_blueprint.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    # Check if fullname, email, and password are in the data
    if not data.get('fullname') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Fullname, email, and password are required', 'code': 'BAD_REQUEST'}), 400

    # Email validation regex pattern
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data.get('email', '')):
        return jsonify({'message': 'Please provide a valid email', 'code': 'BAD_REQUEST'}), 400

    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists', 'code': 'BAD_REQUEST'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        fullname=data['fullname'],
        email=data['email'],
        password=hashed_password,
        allergies=data.get('allergies', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message': 'New user created',
        'code': 'SUCCESS'
    }), 201

@api_blueprint.route('/update_allergies', methods=['PUT'])
@jwt_required()
def update_allergies():
    data = request.get_json()
    current_user = get_jwt_identity()

    # Check if allergies field is provided
    if 'allergies' not in data or len(data.get('allergies')) == 0:
        return jsonify({'message': 'Allergies field is required', 'code': 'BAD_REQUEST'}), 400

    # Check if the user with the given id exists
    user = User.query.get(current_user[1])
    if not user:
        return jsonify({'message': 'User not found', 'code': 'NOT_FOUND'}), 404

    # Update the user's allergies
    user.allergies = data['allergies']
    db.session.commit()

    return jsonify({'message': 'User allergies updated successfully', 'code': 'SUCCESS'}), 200


@api_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=[data['email'],user.id], expires_delta=timedelta(hours=1))

        # Prepare user details for the response, excluding the password
        user_details = {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "allergies": user.allergies,
            "date_created": user.date_created.isoformat(),
            "date_updated": user.date_updated.isoformat()
        }

        return jsonify({
            "code": 'SUCCESS',
            "message": 'Logged in successfully',
            "user": user_details,
            "access_token": access_token
        }), 200
    else:
        return jsonify({'message': 'Invalid username or password', 'code': 'FAILED'}), 401

@api_blueprint.route('/check_food', methods=['POST'])
@jwt_required()
def check_food():
    image = request.files['image']
    if image.filename != '':
        if image and Helpers.allowed_image_format(image.filename) and len(image.read()) < Config.MAX_UPLOAD_FILE_SIZE:
            image.seek(0)
            filename = secure_filename(image.filename)
            save_image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image.save(save_image_path)
            helper_instance = Helpers()
            label_index = helper_instance.prepare_image(save_image_path)
            food = Food.query.filter_by(label_index=label_index).first()
            print(food)
            if food:
                found_food = {
                    "name": food.name,
                    "ingredients": food.ingredients
                }
                return jsonify({
                    'message': 'Food recognized',
                    'code': 'SUCCESS',
                    'recognised_food': found_food
                }), 200
            return jsonify({'message': 'No food found with the label_index of '+ label_index, 'code': 'FAILED'}), 404