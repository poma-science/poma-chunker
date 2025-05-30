# poma-chunker

[![PyPI version](https://img.shields.io/pypi/v/poma-chunker.svg)](https://pypi.org/project/poma-chunker/)  
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-blue.svg)](LICENSE.txt)

> **Part of the POMA toolkit.** For the complete documentation, see the [organization README](https://github.com/poma-science/.github).

A high-performance, compiled chunking & context-extraction engine for `.poma` archives outputting chunksets.

> **A chunkset** is the entire path from the document root to a leaf sentence. This keeps full context.

---

## 🚀 Installation

**From GitHub Releases**

```bash
pip install https://github.com/poma-science/poma-chunker/releases/latest
```

---

## 🏁 Basic Usage

```python
from poma_chunker import process, get_relevant_chunks, generate_cheatsheet

# 1. Chunk your .poma archive
result = process("doc.poma", { ...chunker config... })
chunks, chunksets = result["chunks"], result["chunksets"]

# 2. Pick some IDs (e.g. via vector search)
ids = chunksets[0]["chunks"]

# 3. Enrich & format
relevant = get_relevant_chunks(ids, chunks)
print(generate_cheatsheet(relevant))
```

## 📄 API

```python
process(archive_path: str, config: dict) -> dict
get_relevant_chunks(chunk_ids: list, chunks: list) -> list
generate_cheatsheet(relevant_chunks: list) -> str
```

* `process()` - Process a .poma archive to generate structure-aware chunks and chunksets
* `get_relevant_chunks()` - Enrich chunk IDs with their full context
* `generate_cheatsheet()` - Create a compact, deduplicated, context-rich summary

---

## 🔗 See Also

All configuration details & end-to-end examples live in the **org-level README**:
🔗 [https://github.com/poma-science/.github](https://github.com/poma-science/.github)

Check out a complete example workflow:
🔗 [Example Workflow](https://github.com/poma-science/.github/blob/main/example/flow.py)

---

## 🛠 Tests

```bash
pytest
```

---

## 📜 License

Proprietary — see [LICENSE.txt](LICENSE.txt)

Free for non-commercial and evaluation use. Commercial use is currently free but [registration is encouraged](https://poma.science/register) and subject to future licensing terms. Patents pending.

---

## 🧑‍🔬 Acknowledgments

This package uses the following open source libraries at runtime:

- [litellm](https://github.com/BerriAI/litellm) (MIT)
- [pandas](https://github.com/pandas-dev/pandas) (BSD-3)
- [tiktoken](https://github.com/openai/tiktoken) (MIT)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) (MIT)
- [chardet](https://github.com/chardet/chardet) (LGPL)
- [transformers](https://github.com/huggingface/transformers) (Apache 2.0)
- [pytest](https://docs.pytest.org/) (MIT)
