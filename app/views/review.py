from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app.constants import OFFSET, LIMIT

from app.decorators import group_required
from app.models import Post, User

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route("/", methods=["GET"])
@jwt_required()
@group_required('reader', 'writer')
def get_posts():
    offset = request.args.get("offset", OFFSET)
    limit = request.args.get("limit", LIMIT)
    name = request.args.get("name")

    if name:
        posts = Post.find_by_name(name, offset, limit)
    else:
        posts = Post.list(offset, limit)
    return jsonify([post.to_dict() for post in posts])


@posts_bp.route("/<post_id>", methods=["GET"])
@jwt_required()
@group_required('reader', 'writer')
def get_post(post_id):
    post = Post.get(post_id)
    if not post:
        return jsonify({"message": "Post not found."}), 404

    return jsonify(post.to_dict())


@posts_bp.route("/", methods=["POST"])
@jwt_required()
@group_required('writer')
def create_post():
    if not request.json:
        return jsonify({"message": 'Please, specify "name", "text".'}), 400

    name = request.json.get("name")
    text = request.json.get("text")

    user_id = get_jwt()['sub']

    if not name or not text:
        return jsonify({"message": 'Please, specify "name", "text".'}), 400

    post = Post(name=name, text=text, user_id=user_id).save()
    return jsonify(post.to_dict()), 201


@posts_bp.route("/<post_id>", methods=["PUT"])
@jwt_required()
@group_required('writer')
def update_post(post_id):
    name = request.json.get("name")
    text = request.json.get("text")
    user_id = request.json.get("user_id")

    post = Post.get(post_id)
    if not post:
        return jsonify({"message": "User not found."}), 404

    if name:
        post.name = name
    if text:
        post.text = text
    if user_id:
        post.user_id = user_id
    post.save()
    return jsonify(post.to_dict())


@posts_bp.route("/<post_id>", methods=["DELETE"])
@jwt_required()
@group_required('writer')
def delete_post(post_id):
    count = Post.delete(post_id)
    if count:
        return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404
