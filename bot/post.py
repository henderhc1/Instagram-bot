# bot/post.py
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes
from bot.auth import login_with_session


def post_image(image_path: str, caption: str):
    """
    Upload a photo with a caption using a persisted/validated session.
    Retries once on LoginRequired; surfaces rate-limit clearly.
    """
    cl = login_with_session()
    try:
        media = cl.photo_upload(image_path, caption)
        print("✅ Posted to Instagram.")
        return media

    except LoginRequired:
        print("[post] LoginRequired during upload; retrying with fresh login...")
        cl = login_with_session()
        media = cl.photo_upload(image_path, caption)
        print("✅ Posted to Instagram (after relogin).")
        return media

    except PleaseWaitFewMinutes as e:
        raise RuntimeError("Instagram is rate-limiting this account. Try again later.") from e