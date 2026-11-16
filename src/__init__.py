import datetime
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import requests


def init_logger(child_name: str = None) -> logging.Logger:
    _logger = logging.getLogger("report-failed-services")
    if child_name is not None:
        _logger = _logger.getChild(child_name)
    dt = datetime.datetime.now().date()
    date_time = dt.strftime("%Y-%m-%d")

    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    rotatedHandler = TimedRotatingFileHandler(
        filename="logs/%s.log" % date_time,
        encoding="UTF-8",
        when="MIDNIGHT",
        backupCount=30
    )
    rotatedHandler.setLevel(logging.INFO)
    rotatedHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(rotatedHandler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(streamHandler)

    return _logger


logger = init_logger()

DISCORD_TIMEOUT = (5, 15)  # (connect, read) seconds


def send_to_discord(token, channelId, message, embed=None, files=None):
    headers = {
        "Authorization": "Bot {token}".format(token=token),
        "User-Agent": "Bot"
    }
    payload = {"content": message, "embeds": [embed] if embed is not None else []}
    url = "https://discord.com/api/channels/{channelId}/messages".format(channelId=channelId)
    if files:
        response = requests.post(url, headers=headers, data={"payload_json": json.dumps(payload)}, files=files, timeout=DISCORD_TIMEOUT)
    else:
        response = requests.post(url, headers=headers, json=payload, timeout=DISCORD_TIMEOUT)
    response.raise_for_status()


def load_notified_ids() -> list:
    logger.debug("load_notified_ids()")
    notified_ids = []
    if os.path.exists("notified_ids.json"):
        with open("notified_ids.json", "r") as f:
            notified_ids = json.load(f)
    return notified_ids


def add_notified_id(notified_id):
    notified_ids = load_notified_ids()
    notified_ids.append(notified_id)
    save_notified_ids(notified_ids)


def remove_notified_id(notified_id):
    notified_ids = load_notified_ids()
    if notified_id in notified_ids:
        notified_ids.remove(notified_id)
    save_notified_ids(notified_ids)


def save_notified_ids(notified_ids: list):
    logger.debug("save_notified_ids()")
    with open("notified_ids.json", "w") as f:
        f.write(json.dumps(notified_ids))


def get_ignore_services() -> list:
    logger.debug("load_ignore_services()")
    ignore_services = []
    if os.path.exists("ignore_services.json"):
        with open("ignore_services.json", "r") as f:
            ignore_services = json.load(f)
    return ignore_services
