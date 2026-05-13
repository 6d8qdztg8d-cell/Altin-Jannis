import os, json, time, requests

def load_key():
    env = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env) as f:
        for line in f:
            if line.startswith("KIE_API_KEY="):
                return line.strip().split("=",1)[1].strip("\"'")

def generate(api_key, prompt, image_url, output_path):
    headers = {"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
    payload = {"model":"nano-banana-2","input":{
        "prompt": prompt,
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "output_format": "jpg",
        "image_input": [image_url]
    }}
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    tid = r.json()["data"]["taskId"]
    print(f"  Task: {tid}")
    for i in range(60):
        time.sleep(5)
        poll = requests.get("https://api.kie.ai/api/v1/jobs/recordInfo", headers=headers, params={"taskId":tid}, timeout=15)
        data = poll.json().get("data", {})
        state = data.get("state")
        print(f"  Poll {i+1}: {state}")
        if state in ("success","completed"):
            url = json.loads(data.get("resultJson","{}")).get("resultUrls",[])[0]
            img = requests.get(url, timeout=30)
            with open(output_path,"wb") as f: f.write(img.content)
            print(f"  Saved: {output_path}")
            return
        if state in ("failed","error"):
            raise RuntimeError("Failed")
    raise RuntimeError("Timeout")

NACHHER_PROMPT = (
    "Use the reference image as the exact scene — same house, same garden layout, same fence, same viewpoint. "
    "The garden is now clean and well-maintained: lawn freshly mowed with visible stripes, hedges trimmed, paths clear, no weeds. "
    "Beautiful sunny Swiss summer day: deep blue sky, a few white clouds, warm golden sunlight on the garden and house. "
    "Realistic documentary photo style."
)

pairs = [
    ("rasen",    "https://files.catbox.moe/awnub3.jpg"),
    ("hecke",    "https://files.catbox.moe/ix76s0.jpg"),
    ("beet",     "https://files.catbox.moe/0pkmbk.jpg"),
    ("platten",  "https://files.catbox.moe/lni46c.jpg"),
    ("aufraeum", "https://files.catbox.moe/j6683o.jpg"),
]

api_key = load_key()
base = os.path.join(os.path.dirname(__file__), "..", "images")

for name, url in pairs:
    print(f"\n=== nachher-{name} ===")
    generate(api_key, NACHHER_PROMPT, url, os.path.join(base, f"nachher-{name}.jpg"))

print("\nALLE FERTIG")
