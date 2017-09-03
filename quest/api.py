from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from . import db
from .models import Feature


blueprint = Blueprint("api", __name__)


@blueprint.route("/features", methods=["GET"])
def get_features():
    features = Feature.query.all()
    return jsonify({"features": features})


@blueprint.route("/features", methods=["POST"])
def create_feature():
    if not request.json:
        abort(400)

    params = request.json
    priority = int(params.priority)
    target_date = datetime.strptime(params.target_date, "%Y-%m-%d")
    feature = Feature(name=params.name, description=params.description, client=params.client,
                      priority=priority, target_date=target_date, product_area=params.product_area)

    db.session.add(feature)
    db.session.commit()

    return jsonify({"id": feature.id}), 201
