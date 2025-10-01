# bot/scheduler.py
import os
import time
import schedule
from datetime import datetime, timedelta

from bot.post import post_image
from bot.profile import update_profile_picture
from bot.hashtag import like_posts_from_hashtag
from bot.image_getter import get_daily_image
from bot.quote_getter import get_daily_quote

IMAGE_DIR = r"C:\Users\hende\pexels_im"

def get_latest_image() -> str | None:
    if not os.path.isdir(IMAGE_DIR):
        print(f"[scheduler] Folder not found: {IMAGE_DIR}")
        return None
    jpgs = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(".jpg")]
    if not jpgs:
        print("[scheduler] No .jpg images found.")
        return None
    latest = max(jpgs, key=lambda f: os.path.getmtime(os.path.join(IMAGE_DIR, f)))
    return os.path.join(IMAGE_DIR, latest)


def post_daily_image_with_quote():
    # 1) get a new image (your getter purges old files)
    get_daily_image()

    # 2) locate that image
    img_path = get_latest_image()
    if not img_path:
        print("[scheduler] Skipping post: no image available.")
        return

    # 3) caption (ZenQuotes)
    caption = get_daily_quote()
    print(f"[scheduler] Ready to post:\n  image: {img_path}\n  caption: {caption}")

    # --- REAL ACTION (kept commented for test) ---
    post_image(img_path, caption)

def _run_once_job():
    """Wrap job so we can auto-cancel after the first run."""
    post_daily_image_with_quote()
    return schedule.CancelJob  # <- ensures this is a one-off run

def schedule_tasks(test_at: str | None = None):
    """
    If test_at is provided (e.g., '16:06'), schedule a one-off run at that time today.
    Otherwise, define your normal recurring schedules (kept commented).
    """
    schedule.clear()

    if test_at:
        print(f"[scheduler] One-off test scheduled for {test_at} (local time). "
              f"Now: {datetime.now().strftime('%H:%M:%S')}")
        schedule.every().day.at(test_at).do(_run_once_job)
    else:
        # --- your real schedules (kept commented) ---
        # schedule.every().day.at("09:00").do(post_daily_image_with_quote)
        # schedule.every(24).hours.do(like_posts_from_hashtag, "programming", 5)
        # schedule.every(7).days.at("08:00").do(update_profile_picture, r"C:\path_to_profile_pic.jpg")
        pass

    # scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    from datetime import datetime, timedelta

    MINUTES_AHEAD = 1  # set to 2 if you're close to the next minute
    test_time = (datetime.now() + timedelta(minutes=MINUTES_AHEAD)).strftime("%H:%M")

    schedule_tasks(test_time)  # one-off run at the computed HH:MM today
