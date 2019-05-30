import telebot
import requests
import const
import random
from telebot import types

bot = telebot.TeleBot(const.token_bot)

keyboardGenre = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardGenre.row('Ужасы', 'Приключения')
keyboardGenre.row('Комедия', 'Боевик')

keyboardHorrorFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardHorrorFilms.row('Кладбище домашних животных')
keyboardHorrorFilms.row('Психо', 'Сияние')

keyboardAdventureFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardAdventureFilms.row('Аладдин', 'Рубеж мира', 'Зеленая книга')

keyboardComedyFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardComedyFilms.row('Назад в будущее')
keyboardComedyFilms.row('Гадкий Я', 'Маска')
keyboardActionFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardActionFilms.row('Джон Уик 3', 'Мстители.Финал', 'Снегоуборщик')

keyboardLike = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardLike.row('ДА!', 'НЕТ!')

likeStickers = ['CAADBQADkQMAAukKyAN2IcIPRrR79QI', 'CAADBQADpgMAAukKyAN5s5AIa4Wx9AI', 'CAADBQADwAMAAukKyAOjljyyS-dv2AI', 'CAADBQADbwMAAukKyAOvzr7ZArpddAI']
dislikeStkers = ['CAADBQADlAMAAukKyAPXbNncxSnLkQI', 'CAADBQADlQMAAukKyAMT47jbKiY5wAI', 'CAADAgAD0QgAAgi3GQJWyfXhxzvR5gI']

def return_message(id):
    resp = requests.get(
        'https://api.themoviedb.org/3/movie/' + id + '?api_key=' + const.token_tmdb
        + '&append_to_response=videos,images,credits&language=ru-RU')
    title = resp.json()['title']
    company = resp.json()['production_companies'][0]['name']
    country = resp.json()['production_countries'][0]['name']
    release = resp.json()['release_date']
    actor1 = resp.json()['credits']['cast'][0]['name']
    actor2 = resp.json()['credits']['cast'][1]['name']
    actor3 = resp.json()['credits']['cast'][2]['name']
    overview = resp.json()['overview']
    mess3 = str(title) + '\n' + str(company) + ', ' + str(country) + '\nПремьера: ' + str(release) \
            + '\nВ ролях: ' + actor1 + ', ' + actor2 + ', ' + actor3 + ' и др.' + '\n\nОписание\n' + str(overview)
    return (mess3)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Привет! Как настроение?')

@bot.message_handler(commands=['help'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Никто тебе не поможет, человечишко! \nХА-ХА-ХАА-ХААААА!!!\n\nЛадно, шучу) Погнали искать фильмы!')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() in ['хорошо', 'отлично', 'нормально', 'шикарно', 'чудесно', 'ок', 'норм']:
        bot.send_message(message.chat.id, 'Бомбяу! Может посмотрим какой-нибудь фильмец сегодня?',
                         reply_markup=keyboardGenre)

    elif message.text.lower() in ['плохо', 'хуже некуда', 'не ок', 'даже не спрашивай', 'нет настроения']:
        bot.send_message(message.chat.id,
                         'Хорошие фильмы всегда поднимают настроение и дают позитивный настрой! Так что вперед, выбирай жанр',
                         reply_markup=keyboardGenre)

    elif message.text == 'Ужасы':
        bot.send_message(message.chat.id, 'Смелый ход. Ну давай! :)', reply_markup=keyboardHorrorFilms)

    elif message.text == 'Приключения':
        bot.send_message(message.chat.id, 'Вперед, Индиана Джонс!', reply_markup=keyboardAdventureFilms)

    elif message.text == 'Комедия':
        bot.send_message(message.chat.id, 'Юхууу! Погнали :)', reply_markup=keyboardComedyFilms)

    elif message.text == 'Боевик':
        bot.send_message(message.chat.id, 'А ты хорош! Выбирай :)', reply_markup=keyboardActionFilms)

    elif message.text == 'ДА!':
        bot.send_sticker(message.chat.id, random.choice(likeStickers))

    elif message.text == 'НЕТ!':
        bot.send_sticker(message.chat.id, random.choice(dislikeStkers))
        bot.send_message(message.chat.id, 'Давай поищем еще?',
                     reply_markup=keyboardGenre)
    elif message.text == 'Кладбище домашних животных':
        img = open('/Users/nina/botPhoto/petSematary.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(157433)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Психо':
        img = open('/Users/nina/botPhoto/psycho.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(539)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Сияние':
        img = open('/Users/nina/botPhoto/theShining.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(694)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Аладдин':
        img = open('/Users/nina/botPhoto/aladdin.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(420817)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Рубеж мира':
        img = open('/Users/nina/botPhoto/rim.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(531306)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Зеленая книга':
        img = open('/Users/nina/botPhoto/greenBook.jpg','rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(490132)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Гадкий Я':
        img = open('/Users/nina/botPhoto/despicableMe.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(20352)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Назад в будущее':
        img = open('/Users/nina/botPhoto/backToTheFuture.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(105)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Маска':
        img = open('/Users/nina/botPhoto/mask.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(854)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Джон Уик 3':
        img = open('/Users/nina/botPhoto/johnwick3.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(458156)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Мстители.Финал':
        img = open('/Users/nina/botPhoto/avengersEndgame.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(299534)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Снегоуборщик':
        img = open('/Users/nina/botPhoto/coldPursuit.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        bot.send_message(message.chat.id, return_message(str(438650)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    else:
        bot.send_message(message.chat.id, 'Хм, похоже сегодня неподходящее настроение для просмотра фильмов')

bot.polling()