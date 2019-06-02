import telebot
import requests
import const
import random
from telebot import types

bot = telebot.TeleBot(const.token_bot)

respPop = requests.get(
    'https://api.themoviedb.org/3/movie/popular?api_key=' + const.token_tmdb
    + '&language=ru-RU&page=1')
arrayId = [respPop.json()['results'][0]['id'], respPop.json()['results'][1]['id'],
           respPop.json()['results'][2]['id'], respPop.json()['results'][3]['id'],
           respPop.json()['results'][4]['id']]
arrayTitle = [respPop.json()['results'][0]['title'], respPop.json()['results'][1]['title'],
              respPop.json()['results'][2]['title'], respPop.json()['results'][3]['title'],
              respPop.json()['results'][4]['title']]

keyboardPopularFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardPopularFilms.row(str(arrayTitle[0]));
keyboardPopularFilms.row(str(arrayTitle[1]));
keyboardPopularFilms.row(str(arrayTitle[2]));
keyboardPopularFilms.row(str(arrayTitle[3]));
keyboardPopularFilms.row(str(arrayTitle[4]));

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
    poster = 'https://image.tmdb.org/t/p/w440_and_h660_face' + str(resp.json()['poster_path'])
    trailer = 'https://www.themoviedb.org/video/play?key=&width=961&height=540&_=1559510769896&key=' + str(resp.json()['videos']['results'][0]['key'])
    mess3 = str(title) + '\n' + str(company) + ', ' + str(country) + '\nПремьера: ' + str(release) \
            + '\nВ ролях: ' + actor1 + ', ' + actor2 + ', ' + actor3 + ' и др.' + '\n\nОписание\n' + str(overview) + \
            '\nПостер: ' + poster + '\nТрейлер: ' + trailer
    return (mess3)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Привет! Как настроение?')

@bot.message_handler(commands=['help'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Никто тебе не поможет, человечишко! \nХА-ХА-ХАА-ХААААА!!!\n\nЛадно, шучу) Погнали искать фильмы!')

@bot.message_handler(commands=['popular'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Сегодня в программе:', reply_markup=keyboardPopularFilms)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() in ['хорошо', 'отлично', 'нормально', 'шикарно', 'чудесно', 'ок', 'норм']:
        bot.send_message(message.chat.id, 'Бомбяу! Может посмотрим какой-нибудь фильмец сегодня?',
                         reply_markup=keyboardPopularFilms)

    elif message.text.lower() in ['плохо', 'хуже некуда', 'не ок', 'даже не спрашивай', 'нет настроения']:
        bot.send_message(message.chat.id,
                         'Хорошие фильмы всегда поднимают настроение и дают позитивный настрой! Так что вперед, выбирай фильм',
                         reply_markup=keyboardPopularFilms)

    elif message.text == 'ДА!':
        bot.send_sticker(message.chat.id, random.choice(likeStickers))

    elif message.text == 'НЕТ!':
        bot.send_sticker(message.chat.id, random.choice(dislikeStkers))
        bot.send_message(message.chat.id, 'Давай поищем еще?',
                     reply_markup=keyboardPopularFilms)

    elif message.text in arrayTitle:
            i = arrayTitle.index(message.text)
            filmId = arrayId[i]
            bot.send_message(message.chat.id, return_message(str(filmId)))
            bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    else:
        bot.send_message(message.chat.id, 'Хм, похоже сегодня неподходящее настроение для просмотра фильмов')

bot.polling()
