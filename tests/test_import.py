"""
Simple test to verify that the package can be imported and the native extensions are working.
"""

def test_import():
    """Test that the package can be imported."""
    import poma_chunker
    assert hasattr(poma_chunker, "__version__")
    assert hasattr(poma_chunker, "process")
    assert hasattr(poma_chunker, "get_relevant_chunks")
    assert hasattr(poma_chunker, "generate_cheatsheet")
    print(f"Successfully imported poma_chunker version {poma_chunker.__version__}")

if __name__ == "__main__":
    test_import()
