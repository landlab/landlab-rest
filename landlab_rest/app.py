"""Create the Flask app for *landlab-rest*."""
import importlib

from flask import Blueprint, Flask, jsonify, url_for
from flask_cors import CORS


def register_blueprints(app):
    """Register the *landlab_rest* API."""
    rv = []

    for name in ["graphs"]:
        m = importlib.import_module(f".api.{name}", package="landlab_rest")
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item, url_prefix="/" + item.name)
            rv.append(item)

    return rv


def create_app():
    """Create the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.route("/")
    def site_map():
        COLLECTIONS = ["graphs"]

        map = {"@type": "api", "href": url_for(".site_map")}
        links = []
        for rel in COLLECTIONS:
            href = url_for(".".join([rel, "show"]))
            links.append({"rel": rel, "href": href})
        map["links"] = links
        return jsonify(map)

    register_blueprints(app)

    return app
