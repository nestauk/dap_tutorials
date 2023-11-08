"""quarto_demo."""
from pathlib import Path
from typing import Optional

import yaml


def get_yaml_config(file_path: Path) -> Optional[dict]:
    """Fetch yaml config and return as dict if it exists."""
    if file_path.exists():
        with open(file_path, "rt") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)


# Define project base directory
PROJECT_DIR = Path(__file__).resolve().parents[0]

# base/global config
_base_config_path = Path(__file__).parent.resolve() / "config/base.yaml"
config = get_yaml_config(_base_config_path)

# IoD config
_iod_config_path = Path(__file__).parent.resolve() / "config/iod.yaml"
iod_config = get_yaml_config(_iod_config_path)
