import telebot
import requests
import const
import random
from telebot import types

bot = telebot.TeleBot(const.token_bot)

arrayFilmId = []
arrayFilmTitle = []
selectedFilm = ''
selectedFilmId = 0

keyboardLike = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardLike.row('ДА!', 'НЕТ!')

keyboardGenres = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardGenres.row('Комедия', 'Боевик')
keyboardGenres.row('Ужасы', 'Приключения')

keyboardActions = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboardActions.row('Информация о фильме')
keyboardActions.row('Почитать рецензию')
keyboardActions.row('Вернуться к поиску')

likeStickers = ['CAADBQADkQMAAukKyAN2IcIPRrR79QI', 'CAADBQADpgMAAukKyAN5s5AIa4Wx9AI', 'CAADBQADwAMAAukKyAOjljyyS-dv2AI',
                'CAADBQADbwMAAukKyAOvzr7ZArpddAI']
dislikeStkers = ['CAADBQADlAMAAukKyAPXbNncxSnLkQI', 'CAADBQADlQMAAukKyAMT47jbKiY5wAI',
                 'CAADAgAD0QgAAgi3GQJWyfXhxzvR5gI']

def return_popular_films(genre_id):
    pop_films = requests.get(
        'https://api.themoviedb.org/3/discover/movie?api_key=' + const.token_tmdb +
        '&language=ru-RU&sort_by=popularity.desc&with_genres=' + genre_id)
    global arrayFilmId
    arrayFilmId = [pop_films.json()['results'][0]['id'], pop_films.json()['results'][1]['id'],
                   pop_films.json()['results'][2]['id'], pop_films.json()['results'][3]['id'],
                   pop_films.json()['results'][4]['id'], pop_films.json()['results'][5]['id']]
    global arrayFilmTitle
    arrayFilmTitle = [pop_films.json()['results'][0]['title'], pop_films.json()['results'][1]['title'],
                      pop_films.json()['results'][2]['title'], pop_films.json()['results'][3]['title'],
                      pop_films.json()['results'][4]['title'], pop_films.json()['results'][5]['title']]

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
    trailer = 'https://www.themoviedb.org/video/play?key=&width=961&height=540&_=1559510769896&key=' + \
              str(resp.json()['videos']['results'][0]['key'])
    message = str(title) + '\n' + str(company) + ', ' + str(country) + '\nПремьера: ' + str(release) \
            + '\nВ ролях: ' + actor1 + ', ' + actor2 + ', ' + actor3 + ' и др.' + '\n\nОписание\n' + str(overview) + \
            '\nПостер: ' + poster + '\nТрейлер: ' + trailer
    return (message)

def return_review(id):
    resp = requests.get('https://api.themoviedb.org/3/movie/' + id +
                        '/reviews?api_key=250bab81a74d6e3f09d53fc529498d11&language=en-En')
    count = len(resp.json()['results'])
    if count == 0:
        text = 'Нет рецензий к фильму'
    else:
        i = 0
        text = 'Рецензии:\n\n'
        while i < count:
            text = text + resp.json()['results'][i]['content'] + '\n' + 'Author: ' + \
                   resp.json()['results'][i]['author'] + '\n\n' + '*****************************************' + '\n\n'
            i = i + 1;
    return (text)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Привет! Как настроение?')

@bot.message_handler(commands=['help'])
def send_hello(message):
    bot.send_message(message.chat.id, 'Никто тебе не поможет, человечишко! \nХА-ХА-ХАА-ХААААА!!!\n\nЛадно, шучу) Погнали искать фильмы!')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global selectedFilm
    global selectedFilmId
    global arrayFilmId
    global arrayFilmTitle

    if message.text.lower() in ['хорошо', 'отлично', 'нормально', 'шикарно', 'чудесно', 'ок', 'норм']:
        bot.send_message(message.chat.id, 'Бомбяу! Может посмотрим какой-нибудь фильмец сегодня?',
                         reply_markup=keyboardGenres)

    elif message.text.lower() in ['плохо', 'хуже некуда', 'не ок', 'даже не спрашивай', 'нет настроения']:
        bot.send_message(message.chat.id,
                         'Хорошие фильмы всегда поднимают настроение и дают позитивный настрой! Так что вперед, выбирай фильм',
                         reply_markup=keyboardGenres)

    elif message.text == 'Комедия':
        return_popular_films('35')
        keyboardPopFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboardPopFilms.row(str(arrayFilmTitle[0]), str(arrayFilmTitle[1]));
        keyboardPopFilms.row(str(arrayFilmTitle[2]), str(arrayFilmTitle[3]));
        keyboardPopFilms.row(str(arrayFilmTitle[4]), str(arrayFilmTitle[5]));
        bot.send_message(message.chat.id, 'Веселенькое дельце :)', reply_markup=keyboardPopFilms)

    elif message.text == 'Боевик':
        return_popular_films('28')
        keyboardPopFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboardPopFilms.row(str(arrayFilmTitle[0]), str(arrayFilmTitle[1]));
        keyboardPopFilms.row(str(arrayFilmTitle[2]), str(arrayFilmTitle[3]));
        keyboardPopFilms.row(str(arrayFilmTitle[4]), str(arrayFilmTitle[5]));
        bot.send_message(message.chat.id, 'Боевик? Есть, сэр! Заряжай!', reply_markup=keyboardPopFilms)

    elif message.text == 'Ужасы':
        return_popular_films('27')
        keyboardPopFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboardPopFilms.row(str(arrayFilmTitle[0]), str(arrayFilmTitle[1]));
        keyboardPopFilms.row(str(arrayFilmTitle[2]), str(arrayFilmTitle[3]));
        keyboardPopFilms.row(str(arrayFilmTitle[4]), str(arrayFilmTitle[5]));
        bot.send_message(message.chat.id, 'А ты смелый, как я погляжу :)', reply_markup=keyboardPopFilms)

    elif message.text == 'Приключения':
        return_popular_films('12')
        keyboardPopFilms = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboardPopFilms.row(str(arrayFilmTitle[0]), str(arrayFilmTitle[1]));
        keyboardPopFilms.row(str(arrayFilmTitle[2]), str(arrayFilmTitle[3]));
        keyboardPopFilms.row(str(arrayFilmTitle[4]), str(arrayFilmTitle[5]));
        bot.send_message(message.chat.id, 'Вперед, Индиана Джонс!', reply_markup=keyboardPopFilms)

    elif message.text == 'ДА!':
        bot.send_sticker(message.chat.id, random.choice(likeStickers))

    elif message.text == 'НЕТ!':
        bot.send_sticker(message.chat.id, random.choice(dislikeStkers))
        bot.send_message(message.chat.id, 'Давай поищем еще?', reply_markup=keyboardGenres)

    elif message.text in arrayFilmTitle:
        selectedFilm = message.text
        i = arrayFilmTitle.index(selectedFilm)
        selectedFilmId = arrayFilmId[i]
        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboardActions)

    elif message.text == 'Информация о фильме':
        bot.send_message(message.chat.id, return_message(str(selectedFilmId)))
        bot.send_message(message.chat.id, 'Будем смотреть?', reply_markup=keyboardLike)

    elif message.text == 'Почитать рецензию':
        info = return_review(str(selectedFilmId))
        if len(info) > 4096:
            for x in range(0, len(info), 4096):
                bot.send_message(message.chat.id, info[x:x + 4096])
        else:
            bot.send_message(message.chat.id, info)
        bot.send_message(message.chat.id, 'Смотреть-то будем?', reply_markup=keyboardLike)

    elif message.text == 'Вернуться к поиску':
        bot.send_sticker(message.chat.id, random.choice(dislikeStkers))
        bot.send_message(message.chat.id, 'Как скажешь...', reply_markup=keyboardGenres)

    else:
        bot.send_message(message.chat.id, 'Хм, похоже сегодня неподходящее настроение для просмотра фильмов')

bot.polling()
