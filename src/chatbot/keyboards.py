import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def main_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('📝 Мой wish-list!', 'positive')],
            [get_button('🎱 Мой номер!', 'positive')],
            [get_button('🆘 Помощь', 'primary')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def wishlist_keyboard():

    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('✏ Редактировать wish-list', 'positive')],
            [get_button('💫 Оформи желание!', 'positive')],
            [get_button('💬 Оформи ссылку!', 'positive')],
            [get_button('⛔ Отменить действие', 'negative')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def number_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('✏ Редактировать номер', 'positive')],
            [get_button("🎲 Придумай мне другой номер!", 'positive')],
            [get_button('⛔ Отменить действие', 'negative')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def cancel_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('⛔ Отменить действие', 'negative')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def empty_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": []
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard
