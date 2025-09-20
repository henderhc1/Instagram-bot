from bot.auth import login_with_session

def update_profile_picture(image_path):
    client = login_with_session()

    try:
        client.account_change_picture(image_path)
        print("Profile picture updated!")
    except Exception as e:
        print(f"Error updating profile picture: {e}")
    finally:
        client.logout()
