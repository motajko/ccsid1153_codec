"""
Core structural translation matrix mapping between IBM-1153 (EBCDIC) and UTF-8.
Includes explicit alias registration hooks for cp1153 and ccsid1153.
"""

import codecs
from typing import Tuple

# The authoritative 256-index positional table map vector
_MAP_1153_CODES = [
    0x0000, 0x0001, 0x0002, 0x0003, 0x009C, 0x0009, 0x0086, 0x007F,
    0x0008, 0x008D, 0x008E, 0x000B, 0x000C, 0x000D, 0x000E, 0x000F,
    0x0010, 0x0011, 0x0012, 0x0013, 0x009D, 0x0085, 0x0008, 0x0087,
    0x0018, 0x0019, 0x0092, 0x008F, 0x001C, 0x001D, 0x001E, 0x001F,
    0x0080, 0x0081, 0x0082, 0x0083, 0x0084, 0x000A, 0x0017, 0x001B,
    0x0088, 0x0089, 0x008A, 0x008B, 0x008C, 0x0005, 0x0006, 0x0007,
    0x0090, 0x0091, 0x0016, 0x0093, 0x0094, 0x0095, 0x0096, 0x0004,
    0x0098, 0x0099, 0x009A, 0x009B, 0x0014, 0x0015, 0x009E, 0x001A,
    0x0020, 0x00A0, 0x00E2, 0x00E4, 0x0163, 0x00E1, 0x0103, 0x010D,  # č at 0x47
    0x00E7, 0x0107, 0x005B, 0x002E, 0x003C, 0x002D, 0x0028, 0x002B,
    0x0026, 0x00E9, 0x0119, 0x00EB, 0x016F, 0x00ED, 0x00EE, 0x013E,  # ľ at 0x57
    0x013A, 0x00DF, 0x005D, 0x0024, 0x002A, 0x0029, 0x003B, 0x005E,
    0x002D, 0x002F, 0x00C2, 0x00C4, 0x02DD, 0x00C1, 0x0102, 0x010C,
    0x00C7, 0x0106, 0x007C, 0x002C, 0x0025, 0x005F, 0x003E, 0x003F,
    0x02C7, 0x00C9, 0x0118, 0x00CB, 0x016E, 0x00CD, 0x00CE, 0x013D,
    0x0139, 0x0060, 0x003A, 0x0023, 0x0040, 0x0027, 0x003D, 0x0022,
    0x02D8, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067,
    0x0068, 0x0069, 0x015B, 0x0148, 0x0111, 0x00FD, 0x0159, 0x015F,
    0x00B0, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F, 0x0070,
    0x0071, 0x0072, 0x0142, 0x0144, 0x0161, 0x00B8, 0x02DB, 0x20AC,  # € at 0x9F
    0x0105, 0x007E, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077, 0x0078,
    0x0079, 0x007A, 0x015A, 0x0147, 0x0110, 0x00DD, 0x0158, 0x015E,
    0x02D9, 0x0104, 0x017C, 0x0162, 0x017B, 0x00A7, 0x017E, 0x017A,
    0x017D, 0x0179, 0x0141, 0x0143, 0x0160, 0x00A8, 0x00B4, 0x00D7,
    0x007B, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047,  # { at 0xC0
    0x0048, 0x0049, 0x00AD, 0x00F4, 0x00F6, 0x0155, 0x00F3, 0x0151,
    0x007D, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, 0x0050,  # } at 0xD0
    0x0051, 0x0052, 0x011A, 0x0171, 0x00FC, 0x0165, 0x00FA, 0x011B,
    0x005C, 0x00F7, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 0x0058,
    0x0059, 0x005A, 0x010F, 0x00D4, 0x00D6, 0x0154, 0x00D3, 0x0150,
    0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
    0x0038, 0x0039, 0x010E, 0x0170, 0x00DC, 0x0164, 0x00DA, 0x009F
]

EBCDIC_TO_UTF8 = {i: chr(cp).encode("utf-8") for i, cp in enumerate(_MAP_1153_CODES)}
UTF8_TO_EBCDIC = {chr(cp).encode("utf-8"): bytes([i]) for i, cp in enumerate(_MAP_1153_CODES)}


class EBCDIC1153ToUTF8Codec(codecs.Codec):
    """Stateless operational codec handling standard IBM-1153 conversion mappings."""

    def encode(self, input_text: str, errors: str = "strict") -> Tuple[bytes, int]:
        text_content = input_text if isinstance(input_text, str) else input_text.decode("utf-8")
        ebcdic_output = bytearray()
        
        for idx, char in enumerate(text_content):
            char_utf8 = char.encode("utf-8")
            if char_utf8 in UTF8_TO_EBCDIC:
                ebcdic_output.extend(UTF8_TO_EBCDIC[char_utf8])
            else:
                if errors == "strict":
                    raise UnicodeEncodeError(
                        "ibm-1153", text_content, idx, idx + 1,
                        f"Character '{char}' cannot be mapped to IBM-1153."
                    )
                elif errors == "replace":
                    ebcdic_output.append(0x3F)
                elif errors == "ignore":
                    continue
                    
        return bytes(ebcdic_output), len(text_content)

    def decode(self, input_ebcdic_bytes: bytes, errors: str = "strict") -> Tuple[str, int]:
        utf8_output_buffer = bytearray()
        
        for idx, byte in enumerate(input_ebcdic_bytes):
            if byte in EBCDIC_TO_UTF8:
                utf8_output_buffer.extend(EBCDIC_TO_UTF8[byte])
            else:
                if errors == "strict":
                    raise UnicodeDecodeError(
                        "ibm-1153", bytes([byte]), idx, idx + 1,
                        f"Byte 0x{byte:02X} has no valid mapping assignment."
                    )
                elif errors == "replace":
                    utf8_output_buffer.extend("\uFFFD".encode("utf-8"))
                elif errors == "ignore":
                    continue
                    
        return utf8_output_buffer.decode("utf-8"), len(input_ebcdic_bytes)


def _registry_entry(encoding_name: str) -> codecs.CodecInfo | None:
    # Standardize string format (lowercase, strip hyphens and underscores)
    normalized = encoding_name.lower().replace("-", "").replace("_", "")
    
    # Map valid string identifiers to canonical output forms
    aliases = {
        "ibm1153": "ibm-1153",
        "cp1153": "cp1153",
        "ccsid1153": "ccsid1153"
    }
    
    if normalized in aliases:
        codec_instance = EBCDIC1153ToUTF8Codec()
        return codecs.CodecInfo(
            name=aliases[normalized],  # Dynamically return requested variant flag
            encode=codec_instance.encode,
            decode=codec_instance.decode,
        )
    return None


def register_codec():
    """Explicit wrapper exposing programmatic validation registrations cleanly."""
    codecs.register(_registry_entry)
