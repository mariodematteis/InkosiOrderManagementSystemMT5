from importlib.metadata import version
from pathlib import Path

__project_name__ = "Inkosi"
__version__ = version(__project_name__)
__package_dir__ = Path(__file__).absolute().parent
