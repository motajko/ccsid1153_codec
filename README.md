# CCSID 1153 Codec Package

A pure Python package providing native support for the IBM-1153 EBCDIC (Latin-2) code page layout.

## Installation

```bash
pip install .
```

## Usage

```python
import ccsid1153_codec

# Use natively with standard string and byte methods
ebcdic_bytes = "ľščťžýáíéúäôň {} €".encode("ibm-1153")
print(ebcdic_bytes)
```
