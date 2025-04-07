from flask import Blueprint, request, jsonify
from app.extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed_pw})

    return jsonify({"message": "User registered successfully"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200
