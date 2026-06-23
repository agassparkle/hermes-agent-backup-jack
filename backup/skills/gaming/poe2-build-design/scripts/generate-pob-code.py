#!/usr/bin/env python3
"""Generate POB2 import code from XML file.
Usage: python3 generate-pob-code.py build.xml > build.pob

Uses standard zlib compression (NOT raw deflate).
Verified working with POB Community PoE2 as of 2026-06-22.
"""
import sys, zlib, base64

def generate(xml_path):
    with open(xml_path, 'rb') as f:
        xml = f.read()
    
    # Standard zlib compress — this is what POB actually accepts
    compressed = zlib.compress(xml, 9)
    code = base64.b64encode(compressed).decode('ascii')
    # POB substitutions
    code = code.replace('+', '-').replace('/', '_').rstrip('=')
    
    # Verify round-trip
    restored = code.replace('-', '+').replace('_', '/') + '=='
    decoded = zlib.decompress(base64.b64decode(restored))
    assert decoded == xml, f"Round-trip FAILED: {len(decoded)} != {len(xml)}"
    
    return code

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate-pob-code.py <build.xml>", file=sys.stderr)
        sys.exit(1)
    print(generate(sys.argv[1]))
