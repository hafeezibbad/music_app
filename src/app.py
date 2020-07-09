import os
import time

from flask import Flask, g, request

from src.database.db import initialize_db
from src.lib.configuration.utils import load_configuration_from_yaml_file
from src.lib.flask.http_header_helper import FlaskHttpHeaderHelper
from src.lib.logging.utils import get_flask_details_for_log, setup_logging, LOGGING
from src.routes.songs_api import songs_api, SONGS_API_PREFIX
from src.routes.status_api import status_api, STATUS_API_PREFIX


# pylint: disable=invalid-name
app_config = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])
app = Flask(__name__)
app.config.update(
    MAIL_USERNAME=app_config.MailUsername,
    MAIL_PASSWORD=app_config.MailPassword,
    MONGODB_SETTINGS={
        'host': 'mongodb://{db_host}/{db_name}'.format(db_host=app_config.DbHost, db_name=app_config.DbName),
        'port': app_config.DbPort
    }
)

# Initialize app and database
initialize_db(app)

# Register blueprints
app.register_blueprint(songs_api, url_prefix=SONGS_API_PREFIX)
app.register_blueprint(status_api, url_prefix=STATUS_API_PREFIX)


@app.before_request
def before_request():       # pylint: disable=inconsistent-return-statements
    g.start_time = time.time()
    setup_logging()
    LOGGING.handlers = []
    LOGGING.propagate = False

    flask_details = get_flask_details_for_log()
    http_helper = FlaskHttpHeaderHelper()
    g.request_id = http_helper.get_request_id(request)
    tx_details = {'request_id': g.request_id}
    initial_values = {**flask_details, **tx_details}
    LOGGING.new(**initial_values)


@app.after_request
def after_request(response):
    LOGGING.info('REQUEST_EXECUTION_TIME', execution_time=time.time() - g.start_time)
    response.headers['X-Request-Id'] = g.request_id

    return response
