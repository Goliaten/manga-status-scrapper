from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/example")
def example():
    pass
