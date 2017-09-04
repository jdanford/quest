from flask import Blueprint, abort, jsonify, request

from . import db
from .models import Feature


blueprint = Blueprint("api", __name__)


@blueprint.route("/features", methods=["GET"])
def get_features():
    features = Feature.query.order_by(Feature.priority).all()
    return jsonify({"features": features})


@blueprint.route("/features", methods=["POST"])
def create_feature():
    if not request.json:
        abort(400)

    feature = Feature.from_json(request.json)
    Feature.update_priorities(feature.client, feature)
    db.session.add(feature)
    db.session.commit()

    return jsonify({"id": feature.id}), 201


@blueprint.route("/features/<int:feature_id>", methods=["DELETE"])
def delete_feature(feature_id):
    feature = Feature.query.filter(Feature.id == feature_id).one_or_none()
    if not feature:
        abort(404)

    db.session.delete(feature)
    Feature.update_priorities(feature.client)
    db.session.commit()

    return ""
