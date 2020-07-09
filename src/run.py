import os
import sys

# PROJECT_ROOT_DIR variable is set in Makefile
sys.path.append(os.environ['PROJECT_ROOT_DIR'])

# pylint: disable=wrong-import-position
from src.app import app  # noqa: E402
from src.lib.configuration.app_configuration import AppConfiguration  # noqa: E402
from src.lib.configuration.utils import load_configuration_from_yaml_file  # noqa: E402


# pylint: disable=invalid-name
app_config: AppConfiguration = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])


app.run(port=app_config.ServerPort, debug=app_config.Debug)
