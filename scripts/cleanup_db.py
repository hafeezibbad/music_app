# pylint: disable=invalid-name
import os
import sys

from flask import Flask

# PROJECT_ROOT_DIR is set in Makefile
sys.path.append(os.environ['PROJECT_ROOT_DIR'])

# pylint: disable=wrong-import-position
from src.database.db import initialize_db  # noqa: E402
from src.database.models import SongRecord  # noqa: E402
from src.lib.configuration.app_configuration import AppConfiguration  # noqa: E402
from src.lib.configuration.utils import load_configuration_from_yaml_file  # noqa: E402


# pylint: disable=invalid-name, E1101
app_config: AppConfiguration = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])
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
# remove all items in collection
items_deleted = SongRecord.objects.delete()
print('{} items deleted from SongRecord collection'.format(items_deleted))
