from flask import jsonify, request, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    get_jwt_identity)

from app.models import User, RevokedTokenModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/registration", methods=["POST"])
def register():
    """Method for adding a new user (registration).
       Returns access and refresh tokens.
    """
    if not (request.json and request.json.get("first_name") and request.json.get("password")
            and request.json.get("birthday") and request.json.get("email") and request.json.get("last_name")):
        return jsonify(
            {"message": 'Please, provide "birthday", "first_name", "last_name", "email" and "password" in body.'}), 400

    email = request.json["email"]

    if User.find_by_email(email):
        return {"message": "User already exists"}

    new_user = User(**request.json).save()
    access_token = create_access_token(identity=new_user.id, additional_claims=new_user.additional_claims)
    refresh_token = create_refresh_token(identity=new_user.id, additional_claims=new_user.additional_claims)
    return {
        "message": "User was created",
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.json or not request.json.get("email") or not request.json.get("password"):
        return jsonify({"message": 'Please, provide "email" and "password" in body.'}), 400

    email = request.json["email"]
    password = request.json["password"]
    current_user = User.find_by_email(email)
    if not current_user:
        return {"message": "User with {} doesn't exist".format(email)}

    if not User.verify_hash(password, current_user.hashed_password):
        return {"message": "Wrong password"}, 401

    access_token = create_access_token(identity=current_user.id, additional_claims=current_user.additional_claims)
    refresh_token = create_refresh_token(identity=current_user.id, additional_claims=current_user.additional_claims)
    return {
        "message": "Logged in as {}".format(current_user.first_name),
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def post():
    """Method for refreshing access token. Returns new access token."""
    current_user_identity = get_jwt_identity()
    current_user = User.get(current_user_identity)
    access_token = create_access_token(identity=current_user_identity, additional_claims=current_user.additional_claims)
    return {'access_token': access_token}


@auth_bp.route("/logout-access", methods=["POST"])
@jwt_required()
def logout_access():
    jti = get_jwt()['jti']
    try:
        RevokedTokenModel(jti=jti).save()
        return {'message': 'Access token has been revoked'}
    except Exception as e:
        return {
                   "message": "Something went wrong while revoking token",
                   "error": repr(e)
               }, 500


@auth_bp.route("/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()['jti']  # id of a jwt accessing this post method
    try:
        RevokedTokenModel(jti=jti).save()
        return {"message": "Refresh token has been revoked"}
    except Exception:
        return {"message": "Something went wrong while revoking token"}, 500
