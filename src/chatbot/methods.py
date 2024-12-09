import requests

from src.config import settings


def get_session():

    data = {
        "access_token": settings.BOT_TOKEN,
        "group_id": settings.GROUP_ID,
        "v": 5.199
    }

    response = requests.post(
        "https://api.vk.com/method/groups.getLongPollServer",
        data=data
    )

    response_data = response.json()

    return response_data


def send_message(user_id: int, message: str):
    data = {
        "access_token": settings.BOT_TOKEN,
        "user_id": user_id,
        "random_id": 0,
        "message": message,
        "v": 5.199
    }

    requests.post(
        "https://api.vk.com/method/messages.send",
        data=data
    )


def send_message_with_keyboard(user_id: int, message: str, keyboard):

    data = {
        "access_token": settings.BOT_TOKEN,
        "user_id": user_id,
        "random_id": 0,
        "keyboard": keyboard,
        "message": message,
        "v": 5.199
    }

    requests.post(
        "https://api.vk.com/method/messages.send",
        data=data
    )


def get_short_link(link: str):
    data = {
        "access_token": settings.BOT_TOKEN,
        "url": link,
        "private": 0,
        "v": 5.199
    }

    response = requests.post(
        "https://api.vk.com/method/utils.getShortLink",
        data=data
    )

    try:
        response_data = response.json().get('response').get('short_url')
    except AttributeError:
        return None
    else:
        return response_data
