# bot/auth.py
import os
import time
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
)
from requests.exceptions import RetryError
import urllib3

import credentials as credentials  # expects IG_USERNAME, IG_PASSWORD

# Store session.json at the project root (…/mediabot/session.json)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SETTINGS_PATH = os.path.join(PROJECT_ROOT, "session.json")


def _retry(fn, tries: int = 5, start_delay: float = 2.0, factor: float = 2.0):
    """
    Retry helper for flaky IG endpoints (500s/challenge).
    Retries on common transient errors with exponential backoff.
    """
    delay = start_delay
    last_exc = None
    for attempt in range(1, tries + 1):
        try:
            return fn()
        except (RetryError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ResponseError) as e:
            last_exc = e
            print(f"[auth] Temporary IG error {e.__class__.__name__} (attempt {attempt}/{tries}). "
                  f"Retrying in {delay:.0f}s…")
            time.sleep(delay)
            delay *= factor
    if last_exc:
        raise last_exc


def _build_client() -> Client:
    """
    Create an Instagrapi client, attach a challenge handler, and
    load saved settings (device fingerprint + cookies) if present.
    """
    cl = Client()

    # Load existing settings to reduce security flags
    if os.path.exists(SETTINGS_PATH):
        try:
            cl.load_settings(SETTINGS_PATH)
            print(f"[auth] Loaded settings from {SETTINGS_PATH}")
        except Exception as e:
            print(f"[auth] Failed to load settings (starting fresh): {e}")

    # Code handler for EMAIL/SMS challenges
    def code_handler(username: str, choice: str) -> str:
        print(f"[auth] Enter the 6-digit security code sent via {choice}: ", end="", flush=True)
        return input().strip()

    cl.challenge_code_handler = code_handler

    # Optional: tweak timeouts a bit (helps avoid hangs)
    cl.request_timeout = 30
    return cl


def _full_login_flow(cl: Client) -> Client:
    """
    Full login flow with support for 2FA/challenge and transient 500s.
    Persists a fresh session to SETTINGS_PATH on success.
    """
    try:
        # First attempt login (wrapped in retry for transient 5xx)
        _retry(lambda: cl.login(credentials.IG_USERNAME, credentials.IG_PASSWORD))
    except TwoFactorRequired:
        code = input("[auth] 2FA required. Enter your 2FA code: ").strip()
        _retry(lambda: cl.two_factor_login(code))
    except ChallengeRequired:
        print("[auth] Challenge required; handling…")

        # Some versions expose challenge_resolve() (no args). If not available, we just proceed.
        def try_resolve():
            try:
                return cl.challenge_resolve()
            except TypeError:
                # Not supported in this version – ok to ignore
                return None

        try:
            _retry(try_resolve)
        except Exception as e:
            # Not fatal; code handler during login() will still prompt for the code
            print(f"[auth] challenge_resolve notice: {e}")

        # Retry login – your challenge_code_handler will prompt for the EMAIL/SMS code
        _retry(lambda: cl.login(credentials.IG_USERNAME, credentials.IG_PASSWORD))

    # Final sanity check: we’re authenticated
    try:
        cl.get_timeline_feed()
    except LoginRequired:
        raise RuntimeError("[auth] Login failed after challenge/2FA.")

    # Persist refreshed cookies/settings for future runs
    cl.dump_settings(SETTINGS_PATH)
    print(f"[auth] Session saved to {SETTINGS_PATH}")
    return cl


def login_with_session() -> Client:
    """
    Preferred entry point:
      1) Use existing session if valid
      2) Otherwise, do the full login + persist (with backoff)
    """
    cl = _build_client()

    try:
        # If cookies are valid, this will succeed without re-login
        cl.get_timeline_feed()
        print("[auth] Existing session looks valid.")
        return cl
    except (LoginRequired, ChallengeRequired):
        print("[auth] Session invalid or challenged; performing fresh login…")

    return _full_login_flow(cl)


if __name__ == "__main__":
    # Manual one-time login helper:
    #   python -m bot.auth
    client = login_with_session()
    print("[auth] Logged in and session persisted.")