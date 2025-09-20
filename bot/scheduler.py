import schedule
import time
from bot.post import post_image
from bot.profile import update_profile_picture
from bot.hashtag import like_posts_from_hashtag

def schedule_tasks():
    
    # Schedule tasks to run every certain interval
    schedule.every(1).hour.do(like_posts_from_hashtag, "programming", 5)
    schedule.every(3).hours.do(post_image, "C:/path_to_image.jpg", "Scheduled post from bot!")
    schedule.every(6).hours.do(update_profile_picture, "C:/path_to_profile_pic.jpg")

    # Keep running the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)