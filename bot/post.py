from bot.auth import login_with_session

def post_image(image_path, caption):
    client = login_with_session()

    try:
        client.photo_upload(image_path, caption)
        print("Successfully posted the image!")
    except Exception as e:
        print(f"Error while posting the image: {e}")
    finally:
        client.logout()