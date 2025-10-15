# runners/post_daily.py
from datetime import datetime
import json
from pathlib import Path

# 1) get a fresh image (and sidecar metadata)
from image_getter import get_daily_image  # returns (image_path, meta_path)
# 2) get a fresh quote caption
from quote_getter import get_daily_quote
# 3) upload via your bot
from post import post_image

def main():
    try:
        image_path, meta_path = get_daily_image()  # downloads today’s image
        if not image_path:
            print("[runner] No image downloaded. Exiting.")
            return

        # Build caption: quote + optional credit from sidecar JSON
        caption = get_daily_quote()  # "<quote> — <author>"
        try:
            data = json.loads(Path(meta_path).read_text(encoding="utf-8"))
            who = (data.get("photographer") or "").strip()
            if who:
                caption = f"{caption}\n\n📸 {who} • via Pexels"
        except Exception as e:
            print(f"[runner] Could not read metadata: {e}")

        # Post it
        post_image(image_path, caption)
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Posted {Path(image_path).name}")

    except Exception as e:
        print(f"[runner] Failed: {e}")

if __name__ == "__main__":
    main()
