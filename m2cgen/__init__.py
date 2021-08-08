from pathlib import Path

from m2cgen.exporters import (
    export_to_c,
    export_to_c_sharp,
    export_to_dart,
    export_to_elixir,
    export_to_f_sharp,
    export_to_go,
    export_to_haskell,
    export_to_java,
    export_to_javascript,
    export_to_php,
    export_to_powershell,
    export_to_python,
    export_to_r,
    export_to_ruby,
    export_to_rust,
    export_to_visual_basic
)

__all__ = [
    export_to_c,
    export_to_go,
    export_to_java,
    export_to_python,
    export_to_javascript,
    export_to_visual_basic,
    export_to_c_sharp,
    export_to_powershell,
    export_to_r,
    export_to_php,
    export_to_dart,
    export_to_haskell,
    export_to_ruby,
    export_to_f_sharp,
    export_to_rust,
    export_to_elixir,
]

__version__ = (Path(__file__).absolute().parent / "VERSION.txt").read_text(encoding="utf-8").strip()
