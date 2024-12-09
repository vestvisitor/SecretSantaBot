import requests

from src.chatbot.methods import get_session, send_message, send_message_with_keyboard, get_short_link
from src.database.crud import UserManager
from src.chatbot.keyboards import *
from src.config import settings
from src.utils import get_random_number, parse_item


def bot_loop():
    session = get_session()
    user_manager = UserManager()

    while True:
        response = requests.get(
            '{server}?act=a_check&key={key}&ts={ts}&wait=90'.format(
                server=session.get('response').get('server'),
                key=session.get('response').get('key'),
                ts=session.get('response').get('ts'))
        ).json()
        try:
            updates = response['updates']
        except KeyError:
            session = get_session()
            continue

        if updates:
            for element in updates:
                if element.get('type') == "message_new":
                    message_sender = element.get("object").get('message').get('from_id')
                    user_state = user_manager.read_user_state(message_sender)
                    message_text = element.get("object").get('message').get('text')

                    if user_state != 11:
                        message_text = message_text.lower()

                    if user_state != 0 and message_text.lower() == '⛔ отменить действие':
                        send_message_with_keyboard(
                            message_sender,
                            '⛔ Возвращаю в главное меню',
                            main_keyboard()
                        )
                        user_manager.update_user_state(message_sender, 0)

                    elif user_state == 0:

                        if message_text == '📝 мой wish-list!':
                            wishlist = user_manager.read_user_wishlist(message_sender)
                            send_message_with_keyboard(
                                message_sender,
                                f'📋 Вот твой wish-list:\n{wishlist}',
                                wishlist_keyboard()
                            )
                            user_manager.update_user_state(message_sender, 1)

                        elif message_text == '🎱 мой номер!':
                            user_number = user_manager.read_user_number(message_sender)
                            send_message_with_keyboard(
                                message_sender,
                                f'📋 Вот твой номер: {user_number}',
                                number_keyboard()
                            )
                            user_manager.update_user_state(message_sender, 2)

                        elif message_text == '🆘 помощь':
                            send_message_with_keyboard(
                                message_sender,
                                '📄 Напоминаю, как им со мной можно поделиться:\n'
                                 '1) Нажимаешь на кнопку "📝 Мой wish-list!"\n'
                                 '2) Я присылаю тебе твой текущий wish-list (если он есть)\n'
                                 '3) Не устраивает\хочешь изменить - нажимаешь на кнопку "✏ Редактировать wish-list"\n'
                                 '4) Получаешь от меня сообщение о том, что я слушаю и готов записывать\n'
                                 '5) Затем ОДНИМ сообщением присылаешь свой wish-list!\n'
                                 '\n'
                                 'Если захочешь что-то в нём изменить - следуй тем же шагам, что и указаны в инструкции ☝\n'
                                 '\n'
                                 '❗ В этом году, прошу тебя оформить свой список желаний, согласно следующему образцу - это крайне важно!!!\n'
                                 '1) Название товара, ссылка, артикул (если есть), маркетплейс или сайт\n'
                                 '2) Название товара, ссылка, артикул (если есть), маркетплейс или сайт\n'
                                 '3) И так далее...\n'
                                 '\n'
                                 '😎 Благодаря такому виду у всех участников будут одинаковые по стилю списки - поэтому угадать чей это список будет чуточку сложнее!\n'
                                 '🤝 Я могу помочь тебе с оформлением такого списка, если твои желания из маркетплейсов: Ozon, Wildberries, Aliexpress. Для этого:\n'
                                 '1) Нажимаешь на кнопку "📝 Мой wish-list!"\n'
                                 '2) Я присылаю тебе твой текущий wish-list (если он есть)\n'
                                 '3) Нажимаешь на кнопку "💫 Оформи желание!"\n'
                                 '4) Получаешь сообщение о том, что я жду ссылку\n'
                                 '5) Присылаешь мне ссылку с Ozon, Wildberries, Aliexpress\n'
                                 '5) Ждешь! Если все получится, я пришлю тебе оформленное желание!\n'
                                 '\n'
                                 '🙏 В остальных случаях, могу лишь только попросить тебя следовать указанном примеру!\n'
                                 '\n'
                                 '🤖 Еще, я могу помочь тебе получить короткую версию ссылки на любой товар с любого сайта или маркетплейса. Для этого:\n'
                                 '1) Нажимаешь на кнопку "📝 Мой wish-list!"\n'
                                 '2) Я присылаю тебе твой текущий wish-list (если он есть)\n'
                                 '3) Нажимаешь на кнопку "💬 Оформи ссылку!"\n'
                                 '4) Получаешь сообщение о том, что я жду ссылку\n'
                                 '5) Присылаешь мне любую ссылку\n'
                                 '5) Если все получится, я пришлю тебе оформленную ссылку!\n'
                                 '\n'
                                 f'🔮 Также в этом году я заранее позаботился о твоем уникальном номере.\n'
                                 '⚠ Но если вдруг ты захочешь изменить его, то делается это так:\n'
                                 '1) Нажимаешь на кнопку "🎱 Мой номер!"\n'
                                 '2) Далее придумываешь или просишь моей помощи\n'
                                 '\n'
                                 '☝ Этот номер твой Тайный Санта напишет на твоём подарке - это необходимо для того, чтобы каждый подарок нашел своего получателя!',
                                main_keyboard()
                            )

                    elif user_state == 1:

                        if message_text == '✏ редактировать wish-list':
                            message = "🤓 Внимательно слушаю!"
                            state = 11
                            keyboard = cancel_keyboard()

                        elif message_text == '💫 оформи желание!':
                            message = "🤖 Жду ссылку!"
                            state = 111
                            keyboard = cancel_keyboard()

                        elif message_text == '💬 оформи ссылку!':
                            message = "🤖 Жду ссылку!"
                            state = 1111
                            keyboard = cancel_keyboard()

                        else:
                            message = "😒 Не понимаю тебя..."
                            state = 1
                            keyboard = wishlist_keyboard()

                        send_message_with_keyboard(
                            message_sender,
                            message,
                            keyboard
                        )
                        user_manager.update_user_state(message_sender, state)

                    elif user_state == 11:
                        user_manager.update_user_wishlist(message_sender,message_text)

                        send_message_with_keyboard(
                            message_sender,
                            '👌 Все понял, записал!',
                            main_keyboard()
                        )

                        user_manager.update_user_state(message_sender, 0)

                        if user_manager.read_user_active(message_sender) != 1:
                            user_manager.update_user_active(message_sender)

                    elif user_state == 111:
                        send_message(
                            message_sender,
                            "😎 Сейчас посмотрю чего вы там загадали..."
                        )
                        try:
                            result = parse_item.delay(message_text)
                            name, link, code, marketplace = result.get()
                        except Exception:
                            message = "😒 Что-то у меня не получается, попробуй еще раз..."
                            state = 111
                            keyboard = cancel_keyboard()
                        else:
                            message = f"👀 Вот что у меня получилось!\n{name}, {get_short_link(link)}, {code}, {marketplace}"
                            state = 0
                            keyboard = main_keyboard()

                        send_message_with_keyboard(
                            message_sender,
                            message,
                            keyboard
                        )
                        user_manager.update_user_state(message_sender, state)

                    elif user_state == 1111:
                        short_link = get_short_link(message_text)
                        if short_link:
                            message = f'✉ Вот твоя ссылка: {short_link} (❗ Обязательно перепроверь!)'
                            state = 0
                            keyboard = main_keyboard()
                        else:
                            message = "😒 Что-то у меня не получается, попробуй еще раз..."
                            state = 1111
                            keyboard = cancel_keyboard()
                        send_message_with_keyboard(
                                message_sender,
                                message,
                                keyboard
                            )
                        user_manager.update_user_state(message_sender, state)

                    elif user_state == 2:
                        if message_text == "✏ редактировать номер":
                            message = "🤓 Внимательно слушаю!"
                            state = 22
                            keyboard = cancel_keyboard()

                        elif message_text == "🎲 придумай мне другой номер!":
                            random_number = get_random_number()
                            user_manager.update_user_number(message_sender, random_number)

                            message = f'🧐 Хм, дай мне подумать...\nХорошо, твой уникальный номер будет: {random_number}'
                            state = 0
                            keyboard = main_keyboard()
                        else:
                            message = "😒 Не понимаю тебя..."
                            state = 2
                            keyboard = number_keyboard()

                        send_message_with_keyboard(
                            message_sender,
                            message,
                            keyboard
                        )
                        user_manager.update_user_state(message_sender, state)

                    elif user_state == 22:
                        message = "😒 Что-то не похоже это на четырехзначный номер..."
                        state = 22
                        keyboard = cancel_keyboard()

                        if len(message_text) == 4:
                            try:
                                number = int(message_text)
                            except ValueError:
                                pass
                            else:
                                taken_numbers = user_manager.read_users_numbers() + settings.RESTRICTED_NUMBERS

                                if number == user_manager.read_user_number(message_sender):
                                    message = "🙄 Это итак уже твой номер..."

                                elif number not in taken_numbers:
                                    user_manager.update_user_number(message_sender, number)
                                    message = "👌 Все понял, записал!"
                                    state = 0
                                    keyboard = main_keyboard()
                                else:
                                    message = "😒 Упс, кажется такой номер уже занят, либо его использовали в том году..."

                        send_message_with_keyboard(
                            message_sender,
                            message,
                            keyboard
                        )
                        user_manager.update_user_state(message_sender, state)

        session['response']['ts'] = response['ts']
