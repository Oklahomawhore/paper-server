from flask import Blueprint, request, jsonify


bp = Blueprint('papers', __name__, url_prefix='/papers')

@bp.route('/recommend', methods=['GET'])
def recommend_paper():
    """
    Recommend papers for a given user.
    """
    query = request.args.get('uid')
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    #TODO: a paginized personal recommendation list, if cold start, use item-CF
    papers = []
    return jsonify([paper.to_dict() for paper in papers]), 200