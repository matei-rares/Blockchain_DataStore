from flask import Blueprint, jsonify, request, g
from flask_cors import CORS

import repo.database_repo as dbc
from security.security_service import hash_password
users_bp = Blueprint('users', __name__)
CORS(users_bp)


@users_bp.route('/', methods=['GET'])
def get_all_users():
    users = dbc.get_all_users()
    print(users)
    dbc.delete_by_ids([3,4])
    obj = []
    for us in users:
        obj.append(
            {"id": us.id, "username": us.username, "name": us.name, "company": us.company, "is_active": us.is_active})
    return jsonify({"success": True, "data": obj}), 200


@users_bp.route('/<int:userid>/status', methods=['PUT'])
def change_status(userid):
    data = request.get_json()
    data = data['status']
    if data not in [0, 1]:
        return jsonify({"success": False, "message": "Invalid state"}), 400
    result = dbc.update_is_active_by_id( userid,data)
    return jsonify({"success": True, "data": result}), 200


@users_bp.route('/user', methods=['PUT'])
def create_user():
    data = request.get_json()
    username = data['username']
    name = data['name']
    password = hash_password(data['password'])
    company = data['company']
    role = "USER"

    try:
        if dbc.get_user_by_username(username):
            return jsonify({"success": False, "message": "Username already exists!"}), 400
        if len(username) <2:
            return jsonify({"success": False, "message": "Username must be at least 2 characters long!"}), 400
        user = dbc.add_user(username, name, password, company, role)
        return jsonify({"success": True, "data": {"id": user.id, "username": user.username, "name": user.name,
                                                  "company": user.company, "role": user.role}}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@users_bp.route('/admin', methods=['PUT'])
def create_manager():
    data = request.get_json()
    username = data['username']
    name = data['name']
    password = hash_password(data['password'])
    company = data['company']
    role = "ADMIN"
    try:
        if dbc.get_user_by_username(username):
            return jsonify({"success": False, "message": "Username already exists!"}), 400
        if len(username) < 2:
            return jsonify({"success": False, "message": "Username must be at least 2 characters long!"}), 400
        user = dbc.add_user(username, name, password, company, role)
        return jsonify({"success": True, "data": {"id": user.id, "username": user.username, "name": user.name,
                                                  "company": user.company, "role": user.role}}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
