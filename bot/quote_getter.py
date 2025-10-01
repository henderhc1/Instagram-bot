import requests

_ZEN_TODAY = "https://zenquotes.io/api/today"
_ZEN_RANDOM = "https://zenquotes.io/api/random"

def get_daily_quote() -> str:
    """
    Returns a quote formatted as: "<quote> — <author>".
    Tries /today, then falls back to /random, then a static message.
    """
    try:
        r = requests.get(_ZEN_TODAY, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                q = (data[0].get("q") or "").strip()
                a = (data[0].get("a") or "").strip()
                if q and a:
                    return f"{q} — {a}"
    except Exception as e:
        print(f"[quote_getter] /today failed: {e}")

    try:
        r = requests.get(_ZEN_RANDOM, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                q = (data[0].get("q") or "").strip()
                a = (data[0].get("a") or "").strip()
                if q and a:
                    return f"{q} — {a}"
    except Exception as e:
        print(f"[quote_getter] /random failed: {e}")

    return "Stay positive and keep coding! — ZenQuotes"
