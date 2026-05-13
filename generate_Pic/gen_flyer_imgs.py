#!/usr/bin/env python3
"""Generate 4 realistic garden images for the flyer."""
import os, json, time, requests

def load_key():
    env = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env) as f:
        for line in f:
            if line.startswith("KIE_API_KEY="):
                return line.strip().split("=", 1)[1].strip("\"'")

def generate(api_key, prompt, output_path):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"model": "nano-banana-2", "input": {
        "prompt": prompt,
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "output_format": "jpg",
    }}
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask",
                      headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    tid = r.json()["data"]["taskId"]
    print(f"  Task: {tid}")
    for i in range(60):
        time.sleep(5)
        poll = requests.get("https://api.kie.ai/api/v1/jobs/recordInfo",
                            headers=headers, params={"taskId": tid}, timeout=15)
        data = poll.json().get("data", {})
        state = data.get("state")
        print(f"  Poll {i+1}: {state}")
        if state in ("success", "completed"):
            url = json.loads(data.get("resultJson", "{}")).get("resultUrls", [])[0]
            img = requests.get(url, timeout=30)
            with open(output_path, "wb") as f:
                f.write(img.content)
            print(f"  Saved: {output_path}")
            return
        if state in ("failed", "error"):
            raise RuntimeError("Generation failed")
    raise RuntimeError("Timeout")

PROMPTS = [
    (
        "flyer-rasen.jpg",
        "Documentary photo of a red Bosch cordless lawn mower on a freshly mowed Swiss residential lawn, "
        "perfectly visible dark and light green mowing stripes, lush green grass, sunny summer afternoon, "
        "warm golden light, white plastered house facade softly visible in background, no people, "
        "Canon 35mm f/4 ISO 200, realistic garden photo."
    ),
    (
        "flyer-hecke.jpg",
        "Documentary photo of a perfectly trimmed tall dark-green garden hedge in a Swiss residential garden, "
        "clean straight geometric lines, bright sunny summer day, deep blue sky above, "
        "small section of neat gravel path at base, no people, Canon 50mm f/5.6 ISO 200, realistic."
    ),
    (
        "flyer-platten.jpg",
        "Documentary photo of a clean modern garden terrace with grey granite stone slabs, "
        "Swiss residential garden, well-maintained green lawn border, summer sunlight casting soft shadows, "
        "a few potted plants at edge, no people, Canon 35mm f/4 ISO 200, realistic garden photo."
    ),
    (
        "flyer-garten.jpg",
        "Wide documentary photo of a beautifully maintained Swiss residential garden, modern white Einfamilienhaus, "
        "perfectly mowed striped lawn, trimmed hedges, tidy flower beds, sunny summer day, "
        "deep blue sky with a few small white clouds, no people, Canon 24mm f/5.6 ISO 200, realistic."
    ),
]

api_key = load_key()
base = os.path.join(os.path.dirname(__file__), "..", "images")

for fname, prompt in PROMPTS:
    out = os.path.join(base, fname)
    print(f"\n=== {fname} ===")
    generate(api_key, prompt, out)

print("\nALLE FERTIG")
