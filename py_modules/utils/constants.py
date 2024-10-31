import os

ASUSTRAY_FOLDER = os.path.expanduser('~/.asustray')
os.makedirs(ASUSTRAY_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(ASUSTRAY_FOLDER, "asustray.log")
LAST_PROFILE = os.path.join(ASUSTRAY_FOLDER, "lastProfile")

ICON_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ICON_PATH = os.path.join(ICON_BASE_PATH, "rog-logo.svg")