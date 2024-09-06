
from flask import Blueprint, request, jsonify
from ..services.user_service import register_user, update_user_preferences

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status

@bp.route('/update_preferences', methods=['POST'])
def update_preferences():
    data = request.json
    response, status = update_user_preferences(data)
    return jsonify(response), status
