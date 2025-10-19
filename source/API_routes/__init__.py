from flask import Blueprint
from .example import routes as example_routes

routes = Blueprint("routes", __name__)
routes.register_blueprint(example_routes)


from .example import example
