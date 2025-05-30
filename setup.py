from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
import sys
import platform

# Determine platform-specific compiler flags
compile_args = []
link_args = []

# Detect if we're in a CI environment
in_ci = os.environ.get('CI', 'false').lower() == 'true'

# Use simpler flags in CI to maximize compatibility
if in_ci:
    if platform.system() == "Windows":
        compile_args = ["/O2"]
    else:  # Unix-like (Linux, macOS)
        compile_args = ["-O3"]
        
        # Only add minimal necessary flags for CI
        if platform.system() == "Linux":
            # Basic Linux flags
            pass
else:
    # More optimized flags for local development
    if platform.system() == "Windows":
        compile_args = ["/O2", "/W3", "/MD"]
    else:  # Unix-like (Linux, macOS)
        compile_args = ["-O3", "-Wall"]
        if platform.system() == "Darwin":  # macOS
            # Add macOS-specific flags if OpenMP is available
            try:
                # Check if OpenMP is installed
                if os.path.exists("/usr/local/opt/libomp") or os.path.exists("/opt/homebrew/opt/libomp"):
                    compile_args.extend(["-Xpreprocessor", "-fopenmp"])
                    link_args.extend(["-lomp"])
            except:
                # If any error occurs, skip OpenMP
                pass
        elif platform.system() == "Linux":
            # Add Linux-specific flags
            compile_args.append("-fopenmp")
            link_args.append("-fopenmp")

# Define extensions - ensure sources exist and are not empty
extensions = []

# Check for chunker_core.pyx
chunker_pyx_path = "src/poma_chunker/chunker_core.pyx"
if os.path.exists(chunker_pyx_path) and os.path.getsize(chunker_pyx_path) > 0:
    extensions.append(
        Extension(
            name="poma_chunker.chunker_core",
            sources=[chunker_pyx_path],
            extra_compile_args=compile_args,
            extra_link_args=link_args,
            language="c",  # Explicitly specify C to avoid C++ issues
        )
    )
    print(f"Found chunker_core.pyx: {os.path.getsize(chunker_pyx_path)} bytes")
else:
    print(f"Warning: chunker_core.pyx not found or empty at {chunker_pyx_path}")

# Check for retrieval_core.pyx
retrieval_pyx_path = "src/poma_chunker/retrieval_core.pyx"
if os.path.exists(retrieval_pyx_path) and os.path.getsize(retrieval_pyx_path) > 0:
    extensions.append(
        Extension(
            name="poma_chunker.retrieval_core",
            sources=[retrieval_pyx_path],
            extra_compile_args=compile_args,
            extra_link_args=link_args,
            language="c",  # Explicitly specify C to avoid C++ issues
        )
    )
    print(f"Found retrieval_core.pyx: {os.path.getsize(retrieval_pyx_path)} bytes")
else:
    print(f"Warning: retrieval_core.pyx not found or empty at {retrieval_pyx_path}")

# Check if we have valid extensions
has_extensions = len(extensions) > 0

# Only include extensions if we have valid extensions
if has_extensions:
    # Force platform-specific wheel by ensuring we have at least one extension
    print(f"Building with {len(extensions)} Cython extensions")
    ext_modules = cythonize(
        extensions,
        compiler_directives={
            "language_level": 3,
            "binding": False,
            "embedsignature": False,
            "emit_code_comments": False,
        },
    )
else:
    # If we don't have extensions, create a dummy extension to force a platform wheel
    print("No valid .pyx files found, creating dummy extension to force platform wheel")
    dummy_ext = Extension(
        name="poma_chunker._dummy",
        sources=["src/poma_chunker/_dummy.c"],
        language="c",
    )
    
    # Create a minimal C file if it doesn't exist
    dummy_c_path = "src/poma_chunker/_dummy.c"
    if not os.path.exists(dummy_c_path):
        os.makedirs(os.path.dirname(dummy_c_path), exist_ok=True)
        with open(dummy_c_path, "w") as f:
            f.write("/* Dummy C file to force platform wheel */\n")
            f.write("#include <Python.h>\n")
            f.write("static PyMethodDef methods[] = {\n")
            f.write("    {NULL, NULL, 0, NULL}\n");
            f.write("};\n")
            f.write("static struct PyModuleDef module = {\n")
            f.write("    PyModuleDef_HEAD_INIT, \"_dummy\", NULL, -1, methods\n");
            f.write("};\n")
            f.write("PyMODINIT_FUNC PyInit__dummy(void) {\n")
            f.write("    return PyModule_Create(&module);\n")
            f.write("}\n")
        print(f"Created dummy C file at {dummy_c_path}")
    
    ext_modules = [dummy_ext]

# Get package data - ensure we include all necessary files
package_data = {
    "poma_chunker": [
        "*.pyx",                 # Include Cython source files
        "*.so",                  # Unix shared libraries
        "*.pyd",                 # Windows shared libraries
        "*.cpython-*-*.so",      # Platform-specific Unix libraries
        "*.cpython-*-*.pyd",     # Platform-specific Windows libraries
    ],
}

setup(
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    ext_modules=ext_modules,
    include_package_data=True,
    package_data=package_data,
    # Ensure proper binary distribution
    zip_safe=False,
)
