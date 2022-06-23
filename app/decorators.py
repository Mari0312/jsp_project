from functools import wraps

from flask_jwt_extended import get_jwt


def librarian_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt = get_jwt()
        if not jwt.get("is_librarian"):
            return {"message": "Forbidden"}, 403

        result = func(*args, **kwargs)
        return result
    return wrapper
