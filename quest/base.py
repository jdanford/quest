from datetime import datetime

from flask import Blueprint, render_template


blueprint = Blueprint("base", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html", now=datetime.now())
