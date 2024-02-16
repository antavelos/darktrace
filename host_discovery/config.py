import yaml
from pkg_resources import resource_filename

CONFIG_FILE = resource_filename(__name__, "config.yml")
_config = None


def get_config(config_file: str) -> dict:
    global _config
    if _config is None:
        with open(config_file, "r") as f:
            _config = yaml.safe_load(f)
            if _config is None:
                _config = {}

    return _config
