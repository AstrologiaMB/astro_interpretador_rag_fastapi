
with open("data/2 - el sol_ la identidad.md", "rb") as f:
    content = f.read()

# Find the specific byte sequence for the header
pattern = b"sol sextil o tr"
index = content.find(pattern)

if index != -1:
    # Print surrounding bytes
    start = max(0, index - 10)
    end = min(len(content), index + 50)
    chunk = content[start:end]
    print(f"Found at {index}")
    print(f"Raw bytes: {chunk}")
    print(f"Decoded repr: {chunk.decode('utf-8', errors='replace')!r}")
else:
    print("Pattern not found in bytes")
