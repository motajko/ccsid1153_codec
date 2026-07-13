"""
CCSID 1153 Codec Package Initializer.
Automatically hooks into Python's native codecs registry upon import.
"""

from .codec import register_codec

# Run registration automatically when any component imports this package
register_codec()

__all__ = ["register_codec"]
