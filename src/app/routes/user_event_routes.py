from flask import Blueprint, request, jsonify
from ..services.user_event_service import log_user_event

bp = Blueprint('user_events', __name__, url_prefix='/user_events')

@bp.route('/log', methods=['POST'])
def log_event():
    """
    API endpoint to log a user event.
    """
    data = request.json
    user_id = data.get('user_id')
    paper_id = data.get('paper_id')
    event_type = data.get('event_type')

    if not user_id or not paper_id or not event_type:
        return jsonify({"message": "Missing required fields"}), 400

    try:
        event = log_user_event(user_id, paper_id, event_type)
        return jsonify(event.to_dict()), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500