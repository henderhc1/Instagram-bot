from bot.post import post_image
from bot.profile import update_profile_picture
from bot.hashtag import like_posts_from_hashtag
from bot.auth import save_session
from bot.scheduler import schedule_tasks
import argparse

def main():
    parser = argparse.ArgumentParser(description="Instagram Bot to automate actions like posting, liking, profile updates, etc.")
    parser.add_argument("action", help="Action to perform", choices=["post", "like", "update_profile", "schedule", "save_session"])
    parser.add_argument("--image", help="Path to the image for posting")
    parser.add_argument("--caption", help="Caption for the post")
    parser.add_argument("--hashtag", help="Hashtag to like posts from")
    parser.add_argument("--profile_pic", help="Path to the profile picture")

    args = parser.parse_args()

    if args.action == "post":
        if args.image and args.caption:
            post_image(args.image, args.caption)
        else:
            print("Error: --image and --caption are required for posting.")
    
    elif args.action == "like":
        if args.hashtag:
            like_posts_from_hashtag(args.hashtag)
        else:
            print("Error: --hashtag is required for liking posts.")
    
    elif args.action == "update_profile":
        if args.profile_pic:
            update_profile_picture(args.profile_pic)
        else:
            print("Error: --profile_pic is required for updating profile picture.")

    elif args.action == "schedule":
        schedule_tasks()

    elif args.action == "save_session":
        save_session()

if __name__ == "__main__":
    main()