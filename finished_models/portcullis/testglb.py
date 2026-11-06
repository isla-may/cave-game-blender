
import json
import struct
import sys

path = sys.argv[1]

json_data = None
binary_data = None

with open(path, "rb") as f:
    magic, version, length = struct.unpack("<4sII", f.read(12))

    print("GLB:", magic, "Version:", version)
    print("File size:", length)

    while f.tell() < length:
        chunk_length, chunk_type = struct.unpack("<II", f.read(8))
        chunk = f.read(chunk_length)

        if chunk_type == 0x4E4F534A:
            json_data = json.loads(chunk)

        elif chunk_type == 0x004E4942:
            binary_data = chunk

if json_data is None:
    raise Exception("No JSON chunk found")

if binary_data is None:
    raise Exception("No binary chunk found")

print("\nMaterials:")
print(json.dumps(json_data.get("materials", []), indent=2))

print("\nTextures:")
print(json.dumps(json_data.get("textures", []), indent=2))

print("\nImages:")
print(json.dumps(json_data.get("images", []), indent=2))

print("\nMeshes:")
print(json.dumps(json_data.get("meshes", []), indent=2))

# Extract embedded images
for i, image in enumerate(json_data.get("images", [])):
    view = json_data["bufferViews"][image["bufferView"]]

    start = view.get("byteOffset", 0)
    end = start + view["byteLength"]

    image_bytes = binary_data[start:end]

    filename = f"extracted_texture_{i}.png"

    with open(filename, "wb") as out:
        out.write(image_bytes)

    print(f"\nExtracted {filename}: {len(image_bytes)} bytes")
