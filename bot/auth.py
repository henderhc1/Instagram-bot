from instagrapi import Client
import credentials

def login():
    client = Client()
    try:
        client.login(credentials.IG_USERNAME, credentials.IG_PASSWORD)
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")
        # Handle 2FA or challenges
        if "challenge" in str(e):
            print("2FA or challenge detected! Please manually verify your login.")
            client.challenge_login(credentials.IG_USERNAME)
            print("Verification successful, logged in.")
    return client

def save_session():
    client = Client()
    try:
        client.login(credentials.IG_USERNAME, credentials.IG_PASSWORD)
        client.dump_settings("session.json")  # Save session to file
        print("Session saved successfully.")
    except Exception as e:
        print(f"Login failed: {e}")
    finally:
        client.logout()
        
def login_with_session():
    client = Client()
    try:
        client.load_settings("session.json")  # Load saved session
        client.login(credentials.IG_USERNAME, credentials.IG_PASSWORD)  # Use credentials if needed
        print("Logged in with session!")
    except Exception as e:
        print(f"Login failed: {e}")
        # Retry login using credentials if session load fails
        client.login(credentials.IG_USERNAME, credentials.IG_PASSWORD)
        client.dump_settings("session.json")  # Save session for next use
        print("Session saved successfully.")
    return client