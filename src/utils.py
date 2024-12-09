import random
import copy
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

from src.database.models import User
from src.config import settings
from src.database.crud import UserManager, DecisionManager
from src.make_celery import app
from src.chatbot.methods import send_message_with_keyboard
from src.chatbot.keyboards import main_keyboard, empty_keyboard

user_manager = UserManager()
decision_manager = DecisionManager()


def get_random_number() -> int:
    taken_numbers = user_manager.read_users_numbers() + settings.RESTRICTED_NUMBERS

    while (number := random.randint(1000, 9999)) in taken_numbers:
        continue

    return number


def fill_db_with_participants():
    for name, vk_id  in settings.PARTICIPANTS.items():
        user_manager.create_user(
            name = name,
            vk_id = vk_id,
            number = get_random_number(),
            wishlist = "1. Название товара, ссылка, артикул (если есть), маркетплейс или сайт\n"
                     "2. Название товара, ссылка, артикул (если есть), маркетплейс или сайт\n"
                     "3. Название товара, ссылка, артикул (если есть), маркетплейс или сайт\n"
        )


def send_welcome_message():
    participants = user_manager.read_all_users()

    for participant in participants:
        send_message_with_keyboard(
            participant.vk_id,
            ('Хо-хо-хо! 🖖\n'
             'Это чат-бот Тайного-Санты. 🎅\n'
             'Сегодня я вновь начинаю свою работу по сбору списоков желаний! ⭐\n'
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
             f'🔮 Также в этом году я заранее позаботился о твоем уникальном номере - это {participant.number}\n'
             '⚠ Но если вдруг ты захочешь изменить его, то делается это так:\n'
             '1) Нажимаешь на кнопку "🎱 Мой номер!"\n'
             '2) Далее придумываешь или просишь моей помощи\n'
             '\n'
             '☝ Этот номер твой Тайный Санта напишет на твоём подарке - это необходимо для того, чтобы каждый подарок нашел своего получателя!'
             ),
            main_keyboard()
        )


def send_decision_message():

    pairs = decision_manager.read_pairs()

    for pair in pairs:

        giver = user_manager.read_user(pair.giver)
        receiver = user_manager.read_user(pair.receiver)

        message = (f"📢 {giver.name}, ты будешь в роли Тайного Санты для №: {receiver.number} (не забудь обязательно написать его на подарке или сделать бирку с ним!)\n"
                   f"🎁 Вот что можно подарить:\n"
                   f"{receiver.wishlist}")

        send_message_with_keyboard(
            giver.vk_id,
            message,
            empty_keyboard()
        )

        user_manager.update_user_state(giver.vk_id, 9)


def _logic():
    participants = user_manager.read_active_users()

    givers = copy.deepcopy(participants)
    receivers = copy.deepcopy(participants)

    decisions = {}

    steps = len(participants)

    fails = 0

    while steps:
        random_giver = random.choice(givers)
        random_receiver = random.choice(receivers)

        if random_giver.name == random_receiver.name:
            fails += 1
        elif random_giver.name == "Миша" and random_receiver.name == "Алина" or random_giver.name == "Алина" and random_receiver.name == "Миша":
            fails += 1
        elif random_giver.name == "Рустам" and random_receiver.name == "Аня" or random_giver.name == "Аня" and random_receiver.name == "Рустам":
            fails += 1
        elif random_giver.name == "Лёня" and random_receiver.name == "Кира" or random_giver.name == "Кира" and random_receiver.name == "Лёня":
            fails += 1
        elif random_giver.name == "Миша" and random_receiver.name == "Рустам" or random_giver.name == "Рустам" and random_receiver.name == "Миша":
            fails += 1
        elif random_giver.name == "Аня" and random_receiver.name == "Алина":
            fails += 1
        elif random_giver.name == "Рустам" and random_receiver.name == "Алина":
            fails += 1
        elif random_giver.name == "Аня" and random_receiver.name == "Миша":
            fails += 1
        else:
            decisions[random_giver.vk_id] = random_receiver.vk_id
            givers.remove(random_giver)
            receivers.remove(random_receiver)
            steps -= 1

        if fails > 10:
            return None

    return decisions


def draw_wishlists():
    while not (result := _logic()):
        continue

    for giver, receiver in result.items():
        decision_manager.create_pair(giver, receiver)


def _get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()

    useragent = UserAgent()

    while "Windows" not in (user_agent := useragent.random):
        continue

    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        options=options
    )

    return driver


@app.task
def parse_item(link: str):
    if "ozon.ru/" in link:
        return _parse_item_from_ozon(link)
    elif "wildberries.ru/" in link:
        return _parse_item_from_wildberries(link)
    else:
        return _parse_item_from_aliexpress(link)


def _parse_item_from_ozon(link: str):
    driver = _get_driver()

    title_class = "tm3_27 tsHeadline550Medium"
    code_class = "m1k_27 km2_27 ga120-a undefined ga120-a5"

    driver.get(link)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'lxml')

    try:
        title = f"{soup.find(class_=title_class).text}".strip()
    except AttributeError:
        title = None

    try:
        code = soup.find(class_=code_class).text.split(" ")[1]
    except AttributeError:
        code = None

    return (title, link, code, "Ozon")


def _parse_item_from_wildberries(link: str):
    driver = _get_driver()

    title_class = "product-page__title"
    code_class = "product-params__cell product-params__cell--copy"

    driver.get(link)
    time.sleep(1)
    driver.refresh()
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'lxml')

    try:
        title = f"{soup.find(class_=title_class).text}".strip()
    except AttributeError:
        title = None

    try:
        code = soup.find(class_=code_class).text.strip()
    except AttributeError:
        code = None

    return (title, link, code, "Wildberries")


def _parse_item_from_aliexpress(link: str):
    title_class = "snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography-Primary__base__1xop0e snow-ali-kit_Typography__strong__1shggo snow-ali-kit_Typography__sizeHeadingL__1shggo HazeProductDescription_HazeProductDescription__name__1fmsi HazeProductDescription_HazeProductDescription__smallText__1fmsi"

    html = requests.get(
        url=link
    ).text

    soup = BeautifulSoup(html, 'lxml')

    try:
        title = f"{soup.find(class_=title_class).text}".strip()
    except AttributeError:
        title = None

    return (title, link, "нету", "Aliexpress")


if __name__ == '__main__':
    pass
