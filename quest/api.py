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

    feature = Feature.from_json(request.json)
    db.session.add(feature)
    db.session.commit()

    return jsonify({"id": feature.id}), 201
