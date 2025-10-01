import requests
import os
import random
from datetime import datetime
import json
from credentials import PEXELS_API_KEY  # keep this import

def get_daily_image():
    # ====================== CONFIG ======================
    # REMOVE this line ↓↓↓ (it causes the error)
    # PEXELS_API_KEY = PEXELS_API_KEY

    CATEGORY = "tech"
    SAVE_DIR = r"C:\Users\hende\pexels_im"
    NUM_RESULTS = 10
    # ====================================================

    os.makedirs(SAVE_DIR, exist_ok=True)

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}  # use the imported constant
    params = {"query": CATEGORY, "per_page": NUM_RESULTS, "orientation": "landscape"}

    response = requests.get(url, headers=headers, params=params, timeout=15)
    if response.status_code != 200:
        print(f"Error: Pexels API returned status code {response.status_code}")
        return  # avoid exit() so the scheduler keeps running

    data = response.json()
    photos = data.get('photos', [])
    if not photos:
        print("No photos found for this category.")
        return

    photo = random.choice(photos)
    image_url = photo['src']['large2x']
    photo_id = photo['id']
    photographer = photo['photographer']
    photographer_url = photo['photographer_url']
    photo_page_url = photo['url']

    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{CATEGORY}_{today}_{photo_id}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    # delete old files
    for old_file in os.listdir(SAVE_DIR):
        fp = os.path.join(SAVE_DIR, old_file)
        try:
            if os.path.isfile(fp):
                os.remove(fp)
        except Exception as e:
            print(f"Error deleting {fp}: {e}")

    # download
    image_data = requests.get(image_url, timeout=30).content
    with open(filepath, 'wb') as f:
        f.write(image_data)
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
    with open(meta_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"📄 Metadata saved: {meta_filepath}")