from src.lib.configuration.app_configuration import AppConfiguration
from src.lib.configuration.manager import ConfigurationManager


def load_configuration_from_yaml_file(config_file_path: str = None) -> AppConfiguration:
    configuration_manager = ConfigurationManager(configuration_type=AppConfiguration)
    configuration_object = configuration_manager.load_data_from_configuration_file(config_file_path)

    return configuration_object
