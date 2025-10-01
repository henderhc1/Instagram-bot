from bot.auth import login_with_session
from instagrapi.exceptions import LoginRequired

def like_posts_from_hashtag(hashtag, count=10):
    client = login()

    try:
        medias = client.hashtag_medias_recent(hashtag, count)
        for i, media in enumerate(medias):
            client.media_like(media.id)
            print(f"Liked post #{i+1} from #{hashtag}")
    except LoginRequired:
        print("Login required.")
    finally:
        client.logout()