from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.constants import OFFSET, LIMIT
from app.decorators import group_required
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route("/", methods=["GET"])
@jwt_required()
@group_required('admin')
def get_users():
    offset = request.args.get("offset", OFFSET)
    limit = request.args.get("limit", LIMIT)
    name = request.args.get("name")

    if name:
        users = User.find_by_name(name, offset, limit)
    else:
        users = User.list(offset, limit)
    return jsonify([user.to_dict() for user in users])


@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
@group_required('admin')
def get_user(user_id):
    user = User.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user.to_dict())

@users_bp.route("/<user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    birthday = request.json.get("birthday")
    name = request.json.get("name")
    address = request.json.get("address")
    username = request.json.get("username")
    email = request.json.get("address")
    password = request.json.get("password")

    user = User.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if birthday:
        user.birthday = birthday
    if name:
        user.name = name
    if address:
        user.address = address
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.hashed_password = User.generate_hash(password)
    user.save()
    return jsonify(user.to_dict())


