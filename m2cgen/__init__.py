import os

from .exporters import (
    export_to_c,
    export_to_go,
    export_to_java,
    export_to_python,
    export_to_javascript,
    export_to_visual_basic,
)

__all__ = [
    export_to_java,
    export_to_python,
    export_to_c,
    export_to_go,
    export_to_javascript,
    export_to_visual_basic,
]

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       "VERSION.txt")) as version_file:
    __version__ = version_file.read().strip()
