from flask_mongoengine import MongoEngine


# pylint: disable=invalid-name
db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
