import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Токен вашего бота (замените на свой)
BOT_TOKEN = "8007767378:AAGK0ifS-oMWsgmPUvlrIMf4qMgVcQxr4KU"

# Путь к файлу с ссылками
GIFT_FILE = "gift_links.txt"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Функция для получения информации о количестве ссылок
def get_links_info(links):
    categories = {
        "EternalRose": "EternalRose",
        "ScaredCat": "ScaredCat",
        "SignetRing": "SignetRing",
        "VintageCigar": "VintageCigar",
        "GenieLamp": "GenieLamp",
        "TopHat": "TopHat",
        "DiamondRing": "DiamondRing",
        "SwissWatch": "SwissWatch"
    }

    info = "Количество оставшихся ссылок:\n\n"
    for category, name in categories.items():
        count = len(filter_links_by_category(links, category))
        info += f"{name}: {count}\n"

    return info

# Функция для чтения всех ссылок из файла
def read_gift_links():
    try:
        with open(GIFT_FILE, "r", encoding="utf-8") as file:
            links = file.read().splitlines()
        return links
    except FileNotFoundError:
        return []

# Функция для записи ссылок обратно в файл
def write_gift_links(links):
    with open(GIFT_FILE, "w", encoding="utf-8") as file:
        for link in links:
            file.write(f"{link}\n")

# Функция для фильтрации ссылок по категории
def filter_links_by_category(links, category):
    return [link for link in links if category in link]

# Создаем клавиатуру с командами
def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    # Первый ряд: одна кнопка /rnd
    keyboard.add(KeyboardButton("/rnd"))

    # Второй ряд: две кнопки /rndro и /rndca
    keyboard.row(
        KeyboardButton("/rndro"),  # EternalRose
        KeyboardButton("/rndca")   # ScaredCat
    )

    # Третий ряд: две кнопки /rndri и /rndci
    keyboard.row(
        KeyboardButton("/rndri"),  # SignetRing
        KeyboardButton("/rndci")   # VintageCigar
    )

    # Четвертый ряд: две кнопки /rndge и /rndto
    keyboard.row(
        KeyboardButton("/rndge"),  # GenieLamp
        KeyboardButton("/rndto")   # TopHat
    )

    # Пятый ряд: две кнопки /rnddi и /rndsw
    keyboard.row(
        KeyboardButton("/rnddi"),  # DiamondRing
        KeyboardButton("/rndsw")   # SwissWatch
    )

    return keyboard

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard = create_keyboard()
    await message.reply(
        "Привет! Этот бот отправляет случайные ссылки на Telegram-подарки.\n"
        "Выберите команду из клавиатуры ниже (или введи /info для обзора всех доступных комманд):",
        reply_markup=keyboard
    )

# Обработчик команды /info
@dp.message_handler(commands=["info"])
async def info_command(message: types.Message):
    links = read_gift_links()
    if not links:
        await message.reply("Список ссылок пуст. Добавьте больше ссылок в файл.")
        return

    # Подсчет общего количества ссылок
    total_links = len(links)

    commands_info = (
        "Доступные команды:\n"
        "/rnd - случайная ссылка из всех категорий\n"
        "/rndro - случайная ссылка EternalRose\n"
        "/rndca - случайная ссылка ScaredCat\n"
        "/rndri - случайная ссылка SignetRing\n"
        "/rndci - случайная ссылка VintageCigar\n"
        "/rndge - случайная ссылка GenieLamp\n"
        "/rndto - случайная ссылка TopHat\n"
        "/rnddi - случайная ссылка DiamondRing\n"
        "/rndsw - случайная ссылка SwissWatch\n"
        "/ro X - конкретная ссылка EternalRose-X\n"
        "/ca X - конкретная ссылка ScaredCat-X\n"
        "/ri X - конкретная ссылка SignetRing-X\n"
        "/ci X - конкретная ссылка VintageCigar-X\n"
        "/ge X - конкретная ссылка GenieLamp-X\n"
        "/to X - конкретная ссылка TopHat-X\n"
        "/di X - конкретная ссылка DiamondRing-X\n"
        "/sw X - конкретная ссылка SwissWatch-X\n"
    )

    links_info = get_links_info(links)

    # Формирование итогового сообщения с общим количеством ссылок
    await message.reply(
        f"{commands_info}\n{links_info}\n\nОбщее количество оставшихся ссылок: {total_links}"
    )

# Общая команда /rnd
@dp.message_handler(commands=["rnd"])
async def send_random_gift(message: types.Message):
    links = read_gift_links()
    if not links:
        await message.reply("Список ссылок пуст. Добавьте больше ссылок в файл.")
        return

    random_link = random.choice(links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка: {random_link}")

# Команда для EternalRose (/rndro)
@dp.message_handler(commands=["rndro"])
async def send_eternal_rose(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "EternalRose")
    if not filtered_links:
        await message.reply("Ссылки для EternalRose закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (EternalRose): {random_link}")

# Команда для ScaredCat (/rndca)
@dp.message_handler(commands=["rndca"])
async def send_scared_cat(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "ScaredCat")
    if not filtered_links:
        await message.reply("Ссылки для ScaredCat закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (ScaredCat): {random_link}")

# Команда для SignetRing (/rndri)
@dp.message_handler(commands=["rndri"])
async def send_signet_ring(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "SignetRing")
    if not filtered_links:
        await message.reply("Ссылки для SignetRing закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (SignetRing): {random_link}")

# Команда для VintageCigar (/rndci)
@dp.message_handler(commands=["rndci"])
async def send_vintage_cigar(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "VintageCigar")
    if not filtered_links:
        await message.reply("Ссылки для VintageCigar закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (VintageCigar): {random_link}")

# Команда для GenieLamp (/rndge)
@dp.message_handler(commands=["rndge"])
async def send_genie_lamp(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "GenieLamp")
    if not filtered_links:
        await message.reply("Ссылки для GenieLamp закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (GenieLamp): {random_link}")

# Команда для TopHat (/rndto)
@dp.message_handler(commands=["rndto"])
async def send_top_hat(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "TopHat")
    if not filtered_links:
        await message.reply("Ссылки для TopHat закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (TopHat): {random_link}")

# Команда для DiamondRing (/rnddi)
@dp.message_handler(commands=["rnddi"])
async def send_diamond_ring(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "DiamondRing")
    if not filtered_links:
        await message.reply("Ссылки для DiamondRing закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (DiamondRing): {random_link}")

# Команда для SwissWatch (/rndsw)
@dp.message_handler(commands=["rndsw"])
async def send_swiss_watch(message: types.Message):
    links = read_gift_links()
    filtered_links = filter_links_by_category(links, "SwissWatch")
    if not filtered_links:
        await message.reply("Ссылки для SwissWatch закончились.")
        return

    random_link = random.choice(filtered_links)
    links.remove(random_link)
    write_gift_links(links)
    await message.reply(f"Ваша случайная ссылка (SwissWatch): {random_link}")

# Обработчик команды /ro X для EternalRose
@dp.message_handler(commands=["ro"])
async def eternal_rose_specific(message: types.Message):
    try:
        # Извлекаем число из команды
        number = int(message.get_args())
        link = f"https://t.me/nft/EternalRose-{number}"
        await message.reply(f"Ваша ссылка (EternalRose): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /ro.")

# Обработчик команды /ca X для ScaredCat
@dp.message_handler(commands=["ca"])
async def scared_cat_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/ScaredCat-{number}"
        await message.reply(f"Ваша ссылка (ScaredCat): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /ca.")

# Обработчик команды /ri X для SignetRing
@dp.message_handler(commands=["ri"])
async def signet_ring_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/SignetRing-{number}"
        await message.reply(f"Ваша ссылка (SignetRing): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /ri.")

# Обработчик команды /ci X для VintageCigar
@dp.message_handler(commands=["ci"])
async def vintage_cigar_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/VintageCigar-{number}"
        await message.reply(f"Ваша ссылка (VintageCigar): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /ci.")

# Обработчик команды /ge X для GenieLamp
@dp.message_handler(commands=["ge"])
async def genie_lamp_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/GenieLamp-{number}"
        await message.reply(f"Ваша ссылка (GenieLamp): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /ge.")

# Обработчик команды /to X для TopHat
@dp.message_handler(commands=["to"])
async def top_hat_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/TopHat-{number}"
        await message.reply(f"Ваша ссылка (TopHat): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /to.")

# Обработчик команды /di X для DiamondRing
@dp.message_handler(commands=["di"])
async def diamond_ring_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/DiamondRing-{number}"
        await message.reply(f"Ваша ссылка (DiamondRing): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /di.")

# Обработчик команды /sw X для SwissWatch
@dp.message_handler(commands=["sw"])
async def swiss_watch_specific(message: types.Message):
    try:
        number = int(message.get_args())
        link = f"https://t.me/nft/SwissWatch-{number}"
        await message.reply(f"Ваша ссылка (SwissWatch): {link}")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректное число после команды /sw.")

if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)