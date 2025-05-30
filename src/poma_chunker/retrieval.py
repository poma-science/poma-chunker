# src/poma_chunker/retrieval.py
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

_retrieval = _load_native("retrieval_core")
generate_cheatsheet = _retrieval.generate_cheatsheet
get_relevant_chunks = _retrieval.get_relevant_chunks
__all__ = ["get_relevant_chunks", "generate_cheatsheet"]
