# 📸 Instagram Automation Bot

An automated Instagram bot built in Python using [Instagrapi](https://github.com/adw0rd/instagrapi). It supports posting images, liking posts by hashtag, updating profile pictures, and scheduling interactions.

The program can be set to have random automated images and quotes to be posted using free api's. Setting that up is a bit more complicated but the goal of this project was to ultimately be able to do that once completed.

> ⚠️ This project is for **educational purposes only**. Use at your own risk and comply with Instagram’s terms of service.

---

## 📚 Table of Contents
- [📸 Instagram Automation Bot](#-instagram-automation-bot)
  - [📚 Table of Contents](#-table-of-contents)
  - [📥 Features](#-features)
  - [⚙️ Installation](#️-installation)
  - [▶️ Usage](#️-usage)
  - [⚙️ Configuration](#️-configuration)
  - [🗂️ Project Structure](#️-project-structure)
  - [🧩 Requirements](#-requirements)
  - [Additional optional packages may be required depending on your platform.](#additional-optional-packages-may-be-required-depending-on-your-platform)
  - [🔒 Security \& Privacy](#-security--privacy)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [🧾 Acknowledgements](#-acknowledgements)

---

## 📥 Features
- 🔐 Auto-login with credentials
- 🖼️ Automatically post images to Instagram
- 🏷️ Like posts by hashtags
- 👤 Update profile picture or profile info
- 💬 Optional quotes/captions via a quote getter
- 🕒 Schedule bot actions via `scheduler.py`
- 📜 Logs actions to `logs/bot_actions.log`

---

## ⚙️ Installation

1) Clone the repository:

```powershell
git clone https://github.com/henderhc1/instagram-bot.git
cd "instagram-bot\mediabot"
```

2) (Recommended) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## ▶️ Usage

The project entry point is `main.py`. It exposes several actions via command-line arguments. Below are the supported actions and examples that match the implementation in `main.py`.

- Post an image:

```powershell
python main.py post --image "path\to\image.jpg" --caption "Your caption here"
```

- Like posts from a hashtag:

```powershell
python main.py like --hashtag "nature"
```

- Update profile picture:

```powershell
python main.py update_profile --profile_pic "path\to\profile.jpg"
```

- Run scheduled tasks (uses `scheduler.py`):

```powershell
python main.py schedule
```

- Save a session (useful to persist the login session):

```powershell
python main.py save_session
```

Notes:
- `post` requires both `--image` and `--caption`.
- `like` requires `--hashtag`.
- `update_profile` requires `--profile_pic`.

If an action is invoked without required arguments, the script will print an error message.

---

## ⚙️ Configuration

This project expects a `credentials.py` module in the project root (it is gitignored). It should provide at least the Instagram username and password and any third-party API keys used by helper modules. For example (do not commit real secrets):

```python
# credentials.py (example — keep this file out of version control)
IG_USERNAME = "your_username"
IG_PASSWORD = "your_password"
PEXELS_API_KEY = "your_pexels_api_key"  # optional, used by image_getter
```

Make sure `credentials.py` is present before running the bot.

---

## 🗂️ Project Structure

```
mediabot/
├── bot/
│   ├── auth.py            # Handles login & sessions
│   ├── hashtag.py         # Likes posts from hashtags
│   ├── image_getter.py    # Fetches images to post (PEXELS integration)
│   ├── post.py            # Uploads images to Instagram
│   ├── profile.py         # Updates profile picture/info
│   ├── quote_getter.py    # Gets quotes for captions
│   ├── scheduler.py       # Schedules bot tasks
│   └── __init__.py
├── logs/
│   └── bot_actions.log    # Bot action logs
├── main.py                # Entry point
├── credentials.py         # Login info (gitignored) — create locally
├── requirements.txt       # Dependencies
├── .gitignore             # Ignore rules
└── README.md              # This file
```

---

## 🧩 Requirements

- See `requirements.txt` for direct dependencies (Instagrapi and schedule).

Additional optional packages may be required depending on your platform.
---

## 🔒 Security & Privacy

- Do NOT commit `credentials.py` or any secrets into version control. This repository already includes `.gitignore` to help with that.
- Instagram may detect automated behavior. Use this code only on accounts you own or have permission to operate. Repeated automation can lead to account action or suspension.
- Respect rate limits and avoid aggressive interactions.

---

## 🤝 Contributing

Contributions are welcome. If you'd like to add features or fix bugs:

1. Fork the repo
2. Create a feature branch (git checkout -b feature/my-feature)
3. Make your changes and add tests where appropriate
4. Submit a pull request with a clear description of the change

Please keep changes small and well-scoped. When adding new dependencies, explain why they're needed.

---

## 📄 License

This project is licensed under the MIT License — see the accompanying `LICENSE` file for the full text.

Short disclosure (MIT summary):

- You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software.
- The above copyright notice and this permission notice must be included in all copies or substantial portions of the software.
- The software is provided "as is", without warranty of any kind. The authors are not liable for any claims or damages arising from its use.

If you would like a different license for contributions or distribution, update the `LICENSE` file and the repository documentation accordingly.

---

## 🧾 Acknowledgements

- Built using the `Instagrapi` library — thanks to the maintainers. See their docs for advanced session handling and rate-limiting strategies.

---

If you want, I can also:
- add a `LICENSE` file (MIT suggested)
- add a `setup` script to automate virtualenv + install
- scan the repo for accidental secrets and help rotate them

Happy automating — carefully!