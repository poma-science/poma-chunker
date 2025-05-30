from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import EXTENSION_SUFFIXES
import os

def _load_native(name):
    # On Windows, extension modules use .pyd instead of .so
    suffix = f"{name}{EXTENSION_SUFFIXES[0]}"
    path = os.path.join(os.path.dirname(__file__), suffix)
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_chunker = _load_native("chunker_core")
process = _chunker.process
__all__ = ["process"]