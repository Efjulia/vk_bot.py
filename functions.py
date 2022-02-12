import bs4 as bs4
import requests
import datetime
import sqlite3
from yaweather import Russia, YaWeather


# Функция для получения карты расположения объектов
def picture(object):
    if object == 1:
        # координаты учебного корпуса
        cord = '50.606843,55.364875'
    elif object == 2:
        # координаты общежития
        cord = '50.577522,55.359666'
    else:
        # коодинаты спорткомплекса
        cord = '50.581699,55.360147'
    url = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'l': 'map',
        'll': cord,
        'size': '650,450',
        'pt': cord + ',pm2rdm',
        'z': 17
    }
    response = requests.request('get', url, params=params)
    if response.status_code == 200:
        # Если все успешно возвращаем True
        with open('res.png', 'wb') as file:
            file.write(response.content)
        return True
    else:
        # Если запрос не удался возвращаем False
        return False


# Запись событий в лог.txt, вариант колхоз пати:))), поменяла на logging, в итоговом варианте функцию убрать
def printer(printing):
    log_file = open("log.txt", "a", encoding='utf-8')
    print(str(datetime.datetime.now()) + ' ' + str(printing))
    log_file.write(str(datetime.datetime.now()) + ' ' + str(printing) + '\n')
    log_file.close()
    return printer


# Функция перевода текущей даты в день недели для считывания нужного столбца из БД
# Параметр n = 1 для текущего дня и равен 0 для следующего дня
def dow(now=1):
    if now != 1:
        now = 0
    days = ['monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'Суббота',
            'Воскресенье'
            ]
    return days[datetime.date.today().toordinal() % 7 - now]


# Функция получения названия бд в зависимости от направления обучения
def name_bd_course(education_programme):
    if education_programme == 1:
        name_bd = 'schedule_db_educaiton_programm_1.db'
    elif education_programme == 2:
        name_bd = 'schedule_db_educaiton_programm_2.db'
    else:
        name_bd = 'schedule_db_educaiton_programm_3.db'
    return name_bd


# Функция преобразования фамилии преподавателя в ФИО
def get_fio(surname):
    dict_fio = {"Мухаметзянов": "Мухаметзянов Ильшат Ринатович",
                "Парфенова": "Парфенова Елена Леонидовна",
                "Николаев": "Николаев Михаил Иванович",
                "Воронина": "Воронина Виктория Александровна",
                "Ефимова": "Ефимова Юлия Викторовна",
                "Кузнецова": "Кузнецова Наталья Анатоьевна",
                "Севрюгин": "Севрюгин Сергей Юрьевич",
                "Иванов": "Иванов Николай Михайлович",
                "Жукова": "Жукова Наталья Евгеньевна",
                "Туктарова": "Туктарова Вера Валерьевна",
                "Семина": "Семина Марина Александровна",
                "Теплых": "Теплых Людмила Владимировна",
                "Бакеева": "Бакеева Римма Равилевна",
                "Мирсайзянова": "Мирсайзянова Светлана Анатольевна",
                "Ситдикова": "Ситдикова Лариса Анатольевна",
                "Классен": "Классен Виктор Иванович",
                "Зелинский": "Зелинский Руслан Владимирович",
                "Ахматов": "Ахматов Артем Николаевич",
                "Гаврилов": "Гаврилов Артем Геннадьевич",
                "Белош": "Белош Виктор Владимирович",
                "Мунина": "Мунина Марина Влаерьевна",
                "Мингалимова": "Мингалимова Алсу Вазыховна",
                "Свирина": "Свирина Анна Андреевна",
                "Прохоров": "Прохоров Сергей Григорьевич",
                "Петрулевич": "Петрулевич Елена Александровна"
                }
    return str(dict_fio[surname])


def get_YaWeather():
    dict_sample = {"clear": "ясно",
                   "partly-cloudy": "малооблачно",
                   "cloudy": "облачно с прояснениями",
                   "overcast": "пасмурно",
                   "drizzle": "морось",
                   "light-rain": "небольшой дождь",
                   "rain": "дождь",
                   "moderate-rain": "умеренно сильный дождь",
                   "heavy-rain": "сильный дождь",
                   "continuous-heavy-rain": "длительный сильный дождь",
                   "showers": "ливень",
                   "wet-snow": "дождь со снегом",
                   "light-snow": "небольшой снег",
                   "snow": "снег",
                   "snow-showers": "снегопад",
                   "hail": "град",
                   "thunderstorm": "гроза",
                   "thunderstorm-with-rain": "дождь с грозой",
                   "thunderstorm-with-hail": "гроза с градом"
                   }
    # ключ api_key получен на тестовый режим (валиден на 30 дней с 05.05.2021, до 5000 запросов),
    # если на момент тестирования отвалится, то для доступа необходимо получить новый в кабинете разработчика
    # https://developer.tech.yandex.ru/services/
    y = YaWeather(api_key='8971e254-635e-411a-9c5d-a867ef8f6977')
    res = y.forecast(Russia.Kazan)
    return f'температура: {res.fact.temp} °C, ощущается {res.fact.feels_like} °C ' + '\n'\
           f'на улице: {dict_sample[res.fact.condition]}'


# Чтение бд расписания
def read_db(course_bd, day, course):
    spisok = []
    # Создание соединения для БД
    con = sqlite3.connect(course_bd)
    cur = con.cursor()
    cur.execute(
        'SELECT ' + day + ',' + day + '_teacher' + ',' + day + '_aud' +
        ' FROM '
        + course
    )
    # print(*map(lambda x: x[0], cur.description))
    for row in cur.fetchall():
        spisok.append(row[0])
        spisok.append(row[1])
        spisok.append(row[2])
    return spisok


# Функция, возвращающая расписание в "красивом" виде
def stroka_schedule(db_schedule,number_course, current_day):
    time_schedule = {
        1: "8.15-9.45",
        2: "9.55-11.25",
        3: "12.25-13.55",
        4: "14.05-15.35"
        }
    res_str = ''
    if current_day == 'Суббота' or current_day == 'Воскресенье':
        res_str = f'{current_day} - выходной день'
    else:
        stroka = read_db(db_schedule, current_day, number_course)
        n = 0
        for i in range(0, len(stroka), 3):
            n += 1

            if stroka[i].lower() != 'нет пары':
                res_str += f"_____________________________________________\n"
                res_str += f"{n} пара {time_schedule[n]} \n{stroka[i]}\n"
                res_str += f"Преподаватель: {get_fio(stroka[i+1].strip())}\n"
                res_str += f"Аудитория: {stroka[i+2]}\n"
            else:
                res_str += ""
        res_str += "_____________________________________________\n"
    return res_str


# Получение имени пользователя из id
def get_user_name(user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    result = ""
    not_skip = True
    for i in list(bs.findAll("title")[0]):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True
    return result.split()[0]


# Функция формирования строки - отбивки для предложения возврата в главное меню
def want_main_menu():
    return '\n' + 'Для перехода в главное меню наберите "Старт"' + '\n'
