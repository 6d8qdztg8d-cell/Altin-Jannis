import os, sys, json, time, requests

def create_task(api_key, prompt_str, aspect_ratio="4:3", image_input=None):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt_str,
            "aspect_ratio": aspect_ratio,
            "resolution": "2K",
            "output_format": "jpg"
        }
    }
    if image_input:
        payload["input"]["image_input"] = image_input
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    task_id = r.json()["data"]["taskId"]
    print(f"  Task: {task_id}")
    return task_id

def poll_task(api_key, task_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    for i in range(60):
        time.sleep(5)
        r = requests.get("https://api.kie.ai/api/v1/jobs/recordInfo", headers=headers, params={"taskId": task_id}, timeout=15)
        data = r.json().get("data", {})
        state = data.get("state")
        print(f"  Poll {i+1}: {state}")
        if state in ("success", "completed"):
            urls = json.loads(data.get("resultJson", "{}")).get("resultUrls", [])
            return urls[0] if urls else None
        if state in ("failed", "error"):
            raise RuntimeError("Task failed")
    raise RuntimeError("Timeout")

def download(url, path):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"  Saved: {path}")

def load_api_key():
    env = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env) as f:
        for line in f:
            if line.startswith("KIE_API_KEY="):
                return line.strip().split("=", 1)[1].strip("\"'")
    raise RuntimeError("No KIE_API_KEY in .env")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: generate_pair.py <vorher_out> <nachher_out> <vorher_prompt> <nachher_prompt> [aspect_ratio]")
        sys.exit(1)

    vorher_out  = sys.argv[1]
    nachher_out = sys.argv[2]
    vorher_p    = sys.argv[3]
    nachher_p   = sys.argv[4]
    ratio       = sys.argv[5] if len(sys.argv) > 5 else "4:3"

    api_key = load_api_key()

    # Step 1: generate Vorher
    print("=== VORHER ===")
    tid = create_task(api_key, vorher_p, ratio)
    vorher_url = poll_task(api_key, tid)
    download(vorher_url, vorher_out)

    # Step 2: generate Nachher using Vorher image as reference
    print("=== NACHHER ===")
    nachher_full = nachher_p + " Use the reference image as the same garden and location — same house, same fence, same garden boundaries, but photograph from a slightly different angle or standing position (e.g. a step to the left or slightly lower). Weather is noticeably nicer: bright warm sunshine, deep blue sky, a few white clouds, golden light on the garden. The garden condition is now clean and well-maintained."
    tid2 = create_task(api_key, nachher_full, ratio, image_input=[vorher_url])
    nachher_url = poll_task(api_key, tid2)
    download(nachher_url, nachher_out)

    print("PAIR DONE")
