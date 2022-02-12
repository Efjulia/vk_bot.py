# import sys
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv
from os import environ as env
from functions import get_user_name,  get_YaWeather, want_main_menu,  name_bd_course, dow, picture, \
    stroka_schedule, printer
import logging


logging.basicConfig(filename='bot_log.log', level=logging.DEBUG)


# Главное меню, уровень 1
class KeyboardMainMenu():
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True)
        self.keyboard.add_button('Расписание', color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Погода', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Расположение', color=VkKeyboardColor.NEGATIVE)


# Меню для выбора направлений обучения, уровень 2
class KeyboardProgramm():
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True)
        self.keyboard.add_button('Приборостроение', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Информатика и вычислительная техника', color=VkKeyboardColor.NEGATIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Экономика', color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Главное меню', color=VkKeyboardColor.SECONDARY)


# Меню для выбора курса обучения, уровень 3
class KeyboardCourse():
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True)
        self.keyboard.add_button('Первый курс', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_button('Второй курс', color=VkKeyboardColor.NEGATIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Третий курс', color=VkKeyboardColor.NEGATIVE)
        self.keyboard.add_button('Четвертый курс', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Сменить направление', color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Главное меню', color=VkKeyboardColor.SECONDARY)


# Меню для выбора дня получения расписания, сегодня или завтра, уровень 4
class KeyboardScheduleDay():
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True)
        self.keyboard.add_button('Сегодня', color=VkKeyboardColor.NEGATIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Завтра', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Сменить курс', color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Главное меню', color=VkKeyboardColor.SECONDARY)


# Меню для выбора объектов расположения, уровень 5
class KeyboardUniversatiObject():
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True)
        self.keyboard.add_button('Учебный корпус', color=VkKeyboardColor.NEGATIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Спорткомплекс', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Общежитие', color=VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Главное меню', color=VkKeyboardColor.SECONDARY)


class MessageBot():
    def __init__(self):
        load_dotenv()  # .env
        self.vk_session = vk_api.VkApi(token=env['VK_TOKEN'])
        self.longpoll = VkBotLongPoll(self.vk_session, int(env['VK_BOT_ID']))
        # Словарь приветствий от пользователя для начала работы
        self.slovar = {'привет',
                       'добрый день',
                       'здравствуйте',
                       'добрый вечер',
                       'доброй ночи',
                       'хай',
                       'доброе утро',
                       'начать',
                       'старт',
                       'главное меню'
                       }

# Функция загрузки зображения-карты в сообщение пользователя
    def upload_image_object(self):
        attachments = []
        image = 'res.png'
        upload_image = vk_api.VkUpload(self.vk_session).photo_messages(photos=image)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        return attachments

# Функция формирования строки - расписания
    def write_msg(self, user_id, message):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message})

    def main_bot(self):
        # уровень меню - начальный первый
        level = 1
        # по умолчанию программа обучения выбрана  - Информатика и вычислительная техника
        education_programme = 1
        # по умолчанию первый курс
        course = 'first_course'
        # экземпляры классов клавиатур
        keyboard_main_menu = KeyboardMainMenu()
        keyboard_progr = KeyboardProgramm()
        keyboard_object = KeyboardUniversatiObject()
        keyboard_course = KeyboardCourse()
        keyboard_schedule_day = KeyboardScheduleDay()
        load_dotenv()  # .env
        for event in self.longpoll.listen():
            vk = self.vk_session.get_api()
            if event.type == VkBotEventType.MESSAGE_NEW:
                # получение id пользователя и текста сообщения
                from_id = event.obj.message['from_id']
                text = event.obj.message['text']
                # text
                if text.rstrip("!)( :;").lower() in self.slovar:
                    level = 1
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_main_menu.keyboard.get_keyboard(),
                        message=f'Приветствую, {fullname}! \n ',
                                # f' Для получения расписания наберите команду "расписание" \n '
                                # f'Для получения прогноза погоды наберите команду "погода" \n '
                                # f'Для получения расположения учебный объектов наберите команду "расположение" \n ',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif (text.lower() == 'расписание' and level == 1) or\
                        (text.lower() == "сменить направление" and level == 3):
                    level = 2
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_progr.keyboard.get_keyboard(),
                        message=f'{fullname}, выберите направление',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # выбор направления "Приборостроение" для работы с БД - приборка
                elif text.lower() == 'приборостроение' and level == 2 or\
                        (text.lower() == 'сменить курс' and level == 4 and education_programme == 2):
                    level = 3
                    education_programme = 2
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_course.keyboard.get_keyboard(),
                        message=f'{fullname}, для перехода к расписанию выберите курс',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # выбор направления "Информатика и вычислительная техника" для работы с БД - ИВТ
                elif (text.lower() == 'информатика и вычислительная техника' and level == 2) or\
                        (text.lower() == 'сменить курс' and level == 4 and education_programme == 1):
                    level = 3
                    education_programme = 1
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    self.vk_session.get_api().messages.send(
                        user_id=from_id,
                        keyboard=keyboard_course.keyboard.get_keyboard(),
                        message=f'{fullname}, для перехода к расписанию выберите курс',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # выбор направления "Экономика" для работы с БД - экономика
                elif (text.lower() == 'экономика' and level == 2) or\
                        (text.lower() == 'сменить курс' and level == 4 and education_programme == 3):
                    level = 3
                    education_programme = 3
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_course.keyboard.get_keyboard(),
                        message=f'{fullname}, для перехода к расписанию выберите курс',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'первый курс' and level == 3:
                    course = 'first_course'
                    level = 4
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, на какой день подготовить расписание? \n',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'второй курс' and level == 3:
                    course = 'second_course'
                    level = 4
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, на какой день подготовить расписание? \n',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'третий курс' and level == 3:
                    level = 4
                    course = 'third_course'
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, на какой день подготовить расписание? \n',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'четвертый курс' and level == 3:
                    level = 4
                    course = 'fourth_course'
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, на какой день подготовить расписание? \n',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'завтра' and level == 4:
                    name_bd = name_bd_course(education_programme)
                    stroka = stroka_schedule(name_bd, course, dow(0))
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, расписание на завтра: \n {stroka}',
                        random_id=random.randint(0, 2 ** 64)
                    )
                elif text.lower() == 'сегодня' and level == 4:
                    name_bd = name_bd_course(education_programme)
                    stroka = stroka_schedule(name_bd, course, dow())
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_schedule_day.keyboard.get_keyboard(),
                        message=f'{fullname}, расписание на сегодня: \n {stroka}',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # вывод погоды с использованием API
                elif text.lower() == 'погода' and level == 1:
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_main_menu.keyboard.get_keyboard(),
                        message=f'{fullname}, погода для вас: {get_YaWeather()}',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # вывод расположения объектов  с использованием API
                elif text.lower() == 'расположение' and level == 1:
                    level = 5
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=keyboard_object.keyboard.get_keyboard(),
                        message=f'{fullname}, выберите пункт назначения?',
                        random_id=random.randint(0, 2 ** 64)
                    )
                # вывод вариантов расположения объектов с использованием API
                elif text.lower() == 'учебный корпус' and level == 5:
                    fullname = get_user_name(from_id)
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    if picture(1):
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, готово',
                            random_id=random.randint(0, 2 ** 64),
                            attachment=','.join(MessageBot.upload_image_object(self))
                        )
                    else:
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, произошла ошибка в запросе, попробуйте позже',
                            random_id=random.randint(0, 2 ** 64),
                        )
                elif text.lower() == 'спорткомплекс' and level == 5:
                    fullname = get_user_name(from_id)
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    if picture(3):
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, готово',
                            random_id=random.randint(0, 2 ** 64),
                            attachment=','.join(MessageBot.upload_image_object(self))
                        )
                    else:
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, произошла ошибка в запросе, попробуйте позже',
                            random_id=random.randint(0, 2 ** 64),
                        )
                elif text.lower() == 'общежитие' and level == 5:
                    fullname = get_user_name(from_id)
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    if picture(2):
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, готово',
                            random_id=random.randint(0, 2 ** 64),
                            attachment=','.join(MessageBot.upload_image_object(self))
                        )
                    else:
                        vk.messages.send(
                            user_id=from_id,
                            keyboard=keyboard_object.keyboard.get_keyboard(),
                            message=f'{fullname}, произошла ошибка в запросе, попробуйте позже',
                            random_id=random.randint(0, 2 ** 64),
                        )
                # отработка непонятного запроса от пользователя
                else:
                    logging.info(f'New message {text}  from {from_id}')
                    # printer(f'New message {text} from {from_id}')
                    fullname = get_user_name(from_id)
                    vk.messages.send(
                        user_id=from_id,
                        message=f'{fullname}! Ваш запрос мне непонятен '
                                f' и я пока не могу поддержать диалог! Перефразируйте вопрос :)'
                                f' ' + want_main_menu(),
                        random_id=random.randint(0, 2 ** 64)
                    )
            # логирование всего-всего
            elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
                logging.info(f'Write ' + str(get_user_name(event.obj.from_id)) + ' for ' + str(event.obj.to_id))
                printer(f'Write ' + str(get_user_name(event.obj.from_id)) + ' for ' + str(event.obj.to_id))
            elif event.type == VkBotEventType.GROUP_JOIN:
                logging.info(str(get_user_name(event.obj.user_id)) + ' joined a group!')
                printer(str(get_user_name(event.obj.user_id)) + ' joined a group!')
            elif event.type == VkBotEventType.GROUP_LEAVE:
                logging.info(str(get_user_name(event.obj.user_id)) + ' left the group')
                printer(str(get_user_name(event.obj.user_id)) + ' left the group')
            else:
                logging.info(event.type)
                printer(event.type)


if __name__ == '__main__':
    MessageBot().main_bot()
