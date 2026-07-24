from pathlib import Path
import yaml


def load_config() -> dict:
    """
    Load the project configuration file.

    Returns
    -------
    dict
        Configuration dictionary.
    """

    config_path = Path("config/config.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config