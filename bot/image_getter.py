import requests
import os
import random
from datetime import datetime
import json
from credentials import PEXELS_API_KEY  # keep this import

def get_daily_image():
    # ====================== CONFIG ======================
    CATEGORY = "tech"
    SAVE_DIR = r"C:\Users\Hender\pexels_im"  # <-- fixed username
    NUM_RESULTS = 10
    # ====================================================

    os.makedirs(SAVE_DIR, exist_ok=True)

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": CATEGORY, "per_page": NUM_RESULTS, "orientation": "landscape"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"[Pexels] HTTP {response.status_code}")
    except Exception as e:
        print(f"[Pexels] Request error: {e}")
        return None, None

    if response.status_code != 200:
        print(f"[Pexels] Error: status {response.status_code}")
        print(response.text[:300])
        return None, None

    data = response.json()
    photos = data.get('photos', [])
    if not photos:
        print("[Pexels] No photos found for this category.")
        return None, None

    photo = random.choice(photos)
    image_url = photo['src']['large2x']
    photo_id = photo['id']
    photographer = photo['photographer']
    photographer_url = photo['photographer_url']
    photo_page_url = photo['url']

    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{CATEGORY}_{today}_{photo_id}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    # delete old files (keep directory clean)
    for old_file in os.listdir(SAVE_DIR):
        fp = os.path.join(SAVE_DIR, old_file)
        try:
            if os.path.isfile(fp):
                os.remove(fp)
        except Exception as e:
            print(f"[Pexels] Error deleting {fp}: {e}")

    try:
        img_resp = requests.get(image_url, timeout=30)
        img_resp.raise_for_status()
    except Exception as e:
        print(f"[Pexels] Download error: {e}")
        return None, None

    with open(filepath, 'wb') as f:
        f.write(img_resp.content)
    print(f"✅ Image downloaded: {filepath}")

    metadata = {
        "photographer": photographer,
        "photographer_url": photographer_url,
        "photo_page_url": photo_page_url,
        "downloaded_from": image_url,
        "category": CATEGORY,
        "date_downloaded": today,
        "photo_id": photo_id,
    }
    meta_filepath = os.path.join(SAVE_DIR, filename.replace('.jpg', '.json'))
    with open(meta_filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"📄 Metadata saved: {meta_filepath}")

    # IMPORTANT: return the paths so the runner can use them
    return filepath, meta_filepath
