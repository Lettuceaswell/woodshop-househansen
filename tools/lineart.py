"""Photo -> pixel-aligned line drawing via the local ComfyUI LineArt preprocessor.

    python3 tools/lineart.py assets/img/shop.webp art/lines/shop.png [--coarse]

ComfyUI must be up (systemctl --user start comfyui). Output is black lines on white at the
photo's own size, ready for tools/trace.py --lines.
"""
import json, sys, time, uuid, urllib.parse, urllib.request
from pathlib import Path

HOST = "http://127.0.0.1:8188"
src, out = Path(sys.argv[1]), Path(sys.argv[2])
coarse = "enable" if "--coarse" in sys.argv else "disable"

def post(path, data, headers):
    return json.load(urllib.request.urlopen(urllib.request.Request(HOST + path, data=data, headers=headers)))

b = uuid.uuid4().hex
body = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{src.stem}.png\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n").encode() + src.read_bytes() + f"\r\n--{b}--\r\n".encode()
name = post("/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={b}"})["name"]
g = {"1": {"class_type": "LoadImage", "inputs": {"image": name}},
     "2": {"class_type": "LineArtPreprocessor", "inputs": {"image": ["1", 0], "coarse": coarse, "resolution": 1536}},
     "3": {"class_type": "SaveImage", "inputs": {"images": ["2", 0], "filename_prefix": "woodshop/lines"}}}
pid = post("/prompt", json.dumps({"prompt": g}).encode(), {"Content-Type": "application/json"})["prompt_id"]
while True:
    h = json.load(urllib.request.urlopen(f"{HOST}/history/{pid}"))
    if pid in h:
        im = h[pid]["outputs"]["3"]["images"][0]
        q = "&".join(f"{k}={urllib.parse.quote(im[k])}" for k in ("filename", "subfolder", "type"))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(urllib.request.urlopen(f"{HOST}/view?{q}").read())
        print(out)
        break
    time.sleep(0.5)
