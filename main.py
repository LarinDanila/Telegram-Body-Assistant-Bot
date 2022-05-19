from telegram import Update, Audio, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from gtts import gTTS
import os
import pandas as pd
from pydub import AudioSegment


def generate_path(name):
    return '/home/danila/telebot_train/exercises/' + name + '.mp3'

def create_user_dir(user_id):
    user_id = str(user_id)
    os.mkdir('/home/danila/telebot_train/users/' + user_id)
    os.mkdir('/home/danila/telebot_train/users/' + user_id + '/training')
    os.mkdir('/home/danila/telebot_train/users/' + user_id + '/exercises')

def generate_user_path_to_train(user_id, name):
    return '/home/danila/telebot_train/users/' + str(user_id) + '/training/' + str(name) + '.mp3'

def generate_path_to_user_dir(user_id):
    return '/home/danila/telebot_train/users/' + str(user_id)

def generate_path_to_user_exer_dir(user_id):
    return '/home/danila/telebot_train/users/' + str(user_id) + '/exercises/'

def generate_path_to_user_exercise(user_id, name):
    return '/home/danila/telebot_train/users/' + str(user_id) + '/exercises/' + name + '.mp3'

def create_voice_train(user_id, name_of_train, duration_ex, duration_relax, number_of_circles, exercises):
    task_data = pd.read_csv('/home/danila/telebot_train/exercises/exercises_data.csv')
    task_data = pd.Series(task_data['0'])
    start_train = AudioSegment.from_mp3(generate_path('start_training'))
    finish_train = AudioSegment.from_mp3(generate_path('finish_training'))
    finish_circle = AudioSegment.from_mp3(generate_path('finish_circle'))
    circle = AudioSegment.empty()
    task_start = AudioSegment.from_mp3(generate_path('task_start'))
    task_stop = AudioSegment.from_mp3(generate_path('task_stop'))
    task_user_data = os.listdir(generate_path_to_user_exer_dir(user_id))
    for exercise in exercises:
        if exercise < len(task_data) + 1:
            circle += task_start + AudioSegment.from_mp3(generate_path(task_data[exercise - 1])) + AudioSegment.silent(duration=duration_ex * 1000) + task_stop + AudioSegment.silent(duration=duration_relax * 1000)
        else:
            circle += task_start + AudioSegment.from_mp3(generate_path_to_user_exer_dir(user_id) + task_user_data[exercise - 1 - len(task_data)]) + AudioSegment.silent(duration=duration_ex * 1000) + task_stop + AudioSegment.silent(duration=duration_relax * 1000)
    train = circle
    for i in range(number_of_circles - 1):
        train += finish_circle + circle
    train = start_train + train + finish_train
    train.export(generate_user_path_to_train(user_id, name_of_train))
    

main_menu_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('\U0000270D Создать тренировку'), KeyboardButton('\U0001F4AA Начать тренировку'),  KeyboardButton('\U00002795 Добавить упражнение')],
    [KeyboardButton('\U0001F4DD Мои тренировки'), KeyboardButton('\U0001F4DD Мои упражнения'), KeyboardButton('\U0001F4E6 Поделиться тренировкой')], 
    [KeyboardButton('\U0000270F Вставить код тренировки'), KeyboardButton('\U0000274C Удалить тренировку'), KeyboardButton('\U0000274C Удалить упражнение')], 
    [KeyboardButton('\U0001F527 Помощь')]
], resize_keyboard=True)
def start(update, context):
    users_data = pd.read_csv('users_data.csv')
    if any(users_data['chat_id'] == update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome back')
    else:
        users_data.loc[len(users_data.index)] = [update.effective_chat.id, 0]
        users_data.to_csv('users_data.csv', index=False)
        create_user_dir(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id,text=
        '*Приветствуем!* \U0001F44B \n'
        'Бот предназначен для того, чтобы помочь Вам с созданием собственных тренировок.\n'
        '*Вот список доступных команд:*\n\n'
        '\U0000270D*Создать тренировку*\U0000270D - Вам будет предложено выбрать набор из упражнений, которые будут входить в вашу тренировку, время на выполнение каждого упражнения, время на отдых между упражнениями, а также количество кругов в тренировке. После этого бот сформирует аудиофайл в формате mp3, который вы сможете включать в любое время и заниматься спортом!\n\n'
        '\U0001F4AA*Начать тренировку*\U0001F4AA - Выберете одну из ваших программ, и бот отправит аудиофайл с этой записанной тренировкой.\n\n'
        '\U00002795*Добавить упражнение*\U00002795 - Если вы хотите использовать в занятиях другие упражнения, а не только базовые, то воспользуйтесь этой функцией. После добавления вашего упражнения оно появится в списке, когда вы будете создавать тренировку.\n\n'
        '\U0001F4DD*Мои тренировки*\U0001F4DD - Посмотреть список ваших сохраненных тренировок.\n\n'
        '\U0001F4DD*Мои упражнения*\U0001F4DD - Посмотреть список ваших добавленных упражнений.\n\n'
        '\U0001F4E6*Поделиться тренировкой*\U0001F4E6 и\n \U0000270F*Вставить код тренировки*\U0000270F - если вы хотите поделиться своей тренировкой с другими пользователями, то получите код вашей тренировки с помощью *Поделиться тренировкой*, и отправьте этот код другому пользователю. Тот, в свою очередь, должен скопировать себе эту тренировку, воспользовавшись  функцией *Вставить код тренировки*.\n\n'
        '\U0000274C*Удалить тренировку*\U0000274C - Удалить ненужную тренировку.\n\n'
        '\U0000274C*Удалить упражнение*\U0000274C - Удалить ненужное упражнение.',
        reply_markup=main_menu_keyboard, parse_mode='Markdown'
    )
    context.user_data['program'] = []
    context.user_data['task_time'] = 0
    context.user_data['relax_time'] = 0
    context.user_data['number_of_circles'] = 0



def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text=
        '*Список доступных команд:*\n\n'
        '\U0000270D*Создать тренировку*\U0000270D - Вам будет предложено выбрать набор из упражнений, которые будут входить в вашу тренировку, время на выполнение каждого упражнения, время на отдых между упражнениями, а также количество кругов в тренировке. После этого бот сформирует аудиофайл в формате mp3, который вы сможете включать в любое время и заниматься спортом!\n\n'
        '\U0001F4AA*Начать тренировку*\U0001F4AA - Выберете одну из ваших программ, и бот отправит аудиофайл с этой записанной тренировкой.\n\n'
        '\U00002795*Добавить упражнение*\U00002795 - Если вы хотите использовать в занятиях другие упражнения, а не только базовые, то воспользуйтесь этой функцией. После добавления вашего упражнения оно появится в списке, когда вы будете создавать тренировку.\n\n'
        '\U0001F4DD*Мои тренировки*\U0001F4DD - Посмотреть список ваших сохраненных тренировок.\n\n'
        '\U0001F4DD*Мои упражнения*\U0001F4DD - Посмотреть список ваших добавленных упражнений.\n\n'
        '\U0001F4E6*Поделиться тренировкой*\U0001F4E6 и\n \U0000270F*Вставить код тренировки*\U0000270F - если вы хотите поделиться своей тренировкой с другими пользователями, то получите код вашей тренировки с помощью *Поделиться тренировкой*, и отправьте этот код другому пользователю. Тот, в свою очередь, должен скопировать себе эту тренировку, воспользовавшись  функцией *Вставить код тренировки*.\n\n'
        '\U0000274C*Удалить тренировку*\U0000274C - Удалить ненужную тренировку.\n\n'
        '\U0000274C*Удалить упражнение*\U0000274C - Удалить ненужное упражнение.',
        reply_markup=main_menu_keyboard, parse_mode='Markdown'
    )


def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Error')



STATE = None
GET_EXERCISES = 1
GET_TASK_TIME = 2
GET_RELAX_TIME = 3
GET_NUMBER_OF_CIRCLES = 4
SET_TRAINING = 5
GET_NAME_OF_TRAIN = 6
FIND_TRAIN = 7
GET_DELETE_NAME = 8
GET_EXERCISE_NAME = 9
GET_DELETE_EXERCISE_NAME = 10
GET_NAME_WANNA_SHARE = 11
def text(update, context):
    global STATE
    command = update.message.text
    if command == '\U0000270D Создать тренировку':
        return createworkout(update, context)
    if command == '\U0001F4AA Начать тренировку':
        return startworkout(update, context)
    if command == '\U0001F4DD Мои тренировки':
        return check_saved_training(update, context)
    if command == '\U0001F4DD Мои упражнения':
        return check_saved_exercises(update, context)
    if command == '\U0001F4E6 Поделиться тренировкой':
        return copy_training(update, context)
    if command == '\U0000270F Вставить код тренировки':
        return set_code_training(update, context)
    if command == '\U0000274C Удалить тренировку':
        return delete_workout(update, context)
    if command == '\U0000274C Удалить упражнение':
        return delete_exercise(update, context)
    if command == '\U00002795 Добавить упражнение':
        return add_exercise(update, context)
    if command == '\U0001F527 Помощь':
        return help(update, context)
    if STATE == GET_EXERCISES:
        return get_exercises(update, context)
    if STATE == GET_TASK_TIME:
        return get_task_time(update, context)
    if STATE == GET_RELAX_TIME:
        return get_relax_time(update, context)
    if STATE == GET_NUMBER_OF_CIRCLES:
        return get_number_of_circles(update, context)
    if STATE == GET_NAME_OF_TRAIN:
        return get_name_of_train(update, context)
    if STATE == FIND_TRAIN:
        return try_to_find_train(update, context)
    if STATE == GET_DELETE_NAME:
        return delete_workout_finish(update, context)
    if STATE == GET_EXERCISE_NAME:
        return add_exercise_finish(update, context)
    if STATE == GET_DELETE_EXERCISE_NAME:
        return delete_exercise_finish(update, context)
    if STATE == GET_NAME_WANNA_SHARE:
        return print_share_code(update, context)
    if STATE == SET_TRAINING:
        return set_training(update, context)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Как же это понимать, реально *"{command}"* ?', parse_mode='Markdown')


def createworkout(update, context):
    task_data = pd.read_csv('/home/danila/telebot_train/exercises/exercises_data.csv')
    global STATE
    text_str = '*Опишите свою тренировку (Введите номера упражнений через пробел). Список доступных упражнений:*\n\n'
    for i in range(len(task_data['0'].values)):
        task = task_data.loc[i, '0']
        text_str += f'*{i + 1}*. {task}\n'
    user_exercises = os.listdir(generate_path_to_user_exer_dir(update.effective_chat.id))
    for i in range(len(task_data['0'].values), len(task_data['0'].values) + len(user_exercises)):
        task = user_exercises[i - len(task_data['0'].values)][:-4]
        text_str += f'*{i + 1}*. {task}\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=
        text_str, parse_mode='Markdown'
    )
    STATE = GET_EXERCISES


def delete_workout(update, context):
    global STATE
    lst = os.listdir(os.path.join(generate_path_to_user_dir(update.effective_chat.id), 'training'))
    keyboard = []
    if len(lst) > 0:
        for i in range(0, len(lst) - len(lst) % 2, 2):
            keyboard.append([lst[i][:-4], lst[i + 1][:-4]])
        if len(lst) % 2 != 0:
            keyboard.append([lst[-1][:-4]])
        mrk = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Введите название тренировки:*', reply_markup=mrk, parse_mode='Markdown')
        STATE = GET_DELETE_NAME
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных тренировок.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
        STATE = None


def delete_workout_finish(update, context):
    name = update.message.text
    if os.path.exists(generate_user_path_to_train(update.effective_chat.id, name)):
        os.remove(generate_user_path_to_train(update.effective_chat.id, name))
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка удалена!*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка не найдена.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')


def delete_exercise(update, context):
    global STATE
    lst = os.listdir(os.path.join(generate_path_to_user_dir(update.effective_chat.id), 'exercises'))
    keyboard = []
    if len(lst) > 0:
        for i in range(0, len(lst) - len(lst) % 2, 2):
            keyboard.append([lst[i][:-4], lst[i + 1][:-4]])
        if len(lst) % 2 != 0:
            keyboard.append([lst[-1][:-4]])
        mrk = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Введите название вашего упражнения:*', reply_markup=mrk, parse_mode='Markdown')
        STATE = GET_DELETE_EXERCISE_NAME
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных упражнений.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')


def delete_exercise_finish(update, context):
    global STATE
    name = update.message.text
    if os.path.exists(generate_path_to_user_exercise(update.effective_chat.id, name)):
        os.remove(generate_path_to_user_exercise(update.effective_chat.id, name))
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Упражнение удалено!*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Упражнение не найдено.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')



def check_saved_training(update, context):
    lst = os.listdir(os.path.join(generate_path_to_user_dir(update.effective_chat.id), 'training'))
    txt = '*Ваши тренировки:*\n'
    if len(lst) > 0:
        for i in range(len(lst)):
            txt += f'\t*{i + 1}*. {lst[i][:-4]}\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных тренировок.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')


def check_saved_exercises(update, context):
    lst = os.listdir(generate_path_to_user_exer_dir(update.effective_chat.id))
    txt = '*Ваши упражнения:*\n'
    if len(lst) > 0:
        for i in range(len(lst)):
            txt += f'\t*{i + 1}*. {lst[i][:-4]}\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=main_menu_keyboard, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных упражнений.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')


def add_exercise(update, context):
    global STATE
    context.bot.send_message(chat_id=update.effective_chat.id, text='*Введите название вашего упражнения:*', parse_mode='Markdown')
    STATE = GET_EXERCISE_NAME


def add_exercise_finish(update, context):
    global STATE
    name = update.message.text
    tts = gTTS(text=name, lang='ru')
    tts.save(generate_path_to_user_exercise(update.effective_chat.id, name))
    context.bot.send_message(chat_id=update.effective_chat.id, text='*Упражнение добавлено!*', reply_markup=main_menu_keyboard, parse_mode='Markdown')



def startworkout(update, context):
    global STATE
    lst = os.listdir(os.path.join(generate_path_to_user_dir(update.effective_chat.id), 'training'))
    keyboard = []
    if len(lst) > 0:
        for i in range(0, len(lst) - len(lst) % 2, 2):
            keyboard.append([lst[i][:-4], lst[i + 1][:-4]])
        if len(lst) % 2 != 0:
            keyboard.append([lst[-1][:-4]])
        mrk = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Введите название тренировки:*', reply_markup=mrk, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных тренировок.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    
    STATE = FIND_TRAIN


def get_exercises(update, context):
    task_data = pd.read_csv('/home/danila/telebot_train/exercises/exercises_data.csv')
    global STATE
    try:
        training = list(map(int, update.message.text.split()))
        if len(training) == 0:
            raise ValueError
        for x in training:
            if x < 1 or x > len(task_data) + len(os.listdir(generate_path_to_user_exer_dir(update.effective_chat.id))):
                raise ValueError
        context.user_data['program'] = training
        STATE = GET_TASK_TIME
        context.bot.send_message(chat_id=update.effective_chat.id, text=
            '*Введите время, в течении которого вы будете выполнять каждое упражнение:*', parse_mode='Markdown'
        )
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Пожалуйста, введите корректную программу тренировки*', parse_mode='Markdown')


def get_task_time(update, context):
    global STATE
    try:
        task_time = int(update.message.text)
        if task_time < 1:
            raise ValueError
        context.user_data['task_time'] = task_time
        STATE = GET_RELAX_TIME
        context.bot.send_message(chat_id=update.effective_chat.id, text=
            '*Введите время отдыха между подходами:*', parse_mode='Markdown'
        )
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Пожалуйста, введите корректное время выполнения упражнений*', parse_mode='Markdown')


def get_relax_time(update, context):
    global STATE
    try:
        relax_time = int(update.message.text)
        if relax_time < 1:
            raise ValueError
        context.user_data['relax_time'] = relax_time
        STATE = GET_NUMBER_OF_CIRCLES
        context.bot.send_message(chat_id=update.effective_chat.id, text=
            '*Введите количество кругов в тренировке:*', parse_mode='Markdown'
        )
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Пожалуйста, введите корректное время перерывов между упражнениями*', parse_mode='Markdown')


def get_number_of_circles(update, context):
    global STATE
    try:
        number_of_circles = int(update.message.text)
        if number_of_circles < 1:
            raise ValueError
        context.user_data['number_of_circles'] = number_of_circles
        context.bot.send_message(chat_id=update.effective_chat.id, text=
            '*Введите название вашей тренировки:*', parse_mode='Markdown'
        )
        STATE = GET_NAME_OF_TRAIN
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Пожалуйста, введите корректное число кругов в тренировке*', parse_mode='Markdown')


def get_name_of_train(update, context):
    global STATE
    name = update.message.text
    try:
        create_voice_train(update.effective_chat.id, name, context.user_data['task_time'], context.user_data['relax_time'], context.user_data['number_of_circles'], context.user_data['program'])
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка сохранена.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(generate_user_path_to_train(update.effective_chat.id, name), 'rb'), reply_markup=main_menu_keyboard)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Не удалось сохранить тренировку - слишком большой объём входных данных.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    STATE = None


def try_to_find_train(update, context):
    global STATE
    name = update.message.text
    if os.path.exists(generate_user_path_to_train(update.effective_chat.id, name)):
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(generate_user_path_to_train(update.effective_chat.id, name), 'rb'), reply_markup=main_menu_keyboard)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка не найдена.*', parse_mode='Markdown')
    

def copy_training(update, context):
    global STATE
    lst = os.listdir(os.path.join(generate_path_to_user_dir(update.effective_chat.id), 'training'))
    keyboard = []
    if len(lst) > 0:
        for i in range(0, len(lst) - len(lst) % 2, 2):
            keyboard.append([lst[i][:-4], lst[i + 1][:-4]])
        if len(lst) % 2 != 0:
            keyboard.append([lst[-1][:-4]])
        mrk = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Введите название тренировки:*', reply_markup=mrk, parse_mode='Markdown')
        STATE = GET_NAME_WANNA_SHARE
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Нет сохраненных тренировок*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
        STATE = None


def set_code_training(update, context):
    global STATE
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'*{update.message.chat.first_name}, пожалуйста, введите код тренировки*', parse_mode='Markdown')
    STATE = SET_TRAINING


def print_share_code(update, context):
    global STATE
    name = update.message.text
    if os.path.exists(generate_user_path_to_train(update.effective_chat.id, name)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'*Код вашей тренировки:* \"{update.effective_chat.id}.{name}\"', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка не найдена.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
    STATE = None


def set_training(update, context):
    global STATE
    try:
        code = update.message.text.strip().split('.')
        shared_train = AudioSegment.from_mp3(generate_user_path_to_train(code[0], code[1]))
        shared_train.export(generate_user_path_to_train(update.effective_chat.id, code[1]))
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Тренировка сохранена.*', reply_markup=main_menu_keyboard, parse_mode='Markdown')
        STATE = None
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='*Пожалуйста, введите корректный код тренировки.*', parse_mode='Markdown')
  

def main():
    TOKEN = "TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("createworkout", createworkout))
    dispatcher.add_handler(CommandHandler("startworkout", startworkout))
    dispatcher.add_handler(CommandHandler("shareworkout", copy_training))
    dispatcher.add_handler(CommandHandler("setworkoutcode", set_code_training))
    dispatcher.add_handler(CommandHandler("mytraining", check_saved_training))
    dispatcher.add_handler(CommandHandler("myexercises", check_saved_exercises))
    dispatcher.add_handler(CommandHandler("deleteworkout", delete_workout))
    dispatcher.add_handler(CommandHandler("addexercise", add_exercise))
    dispatcher.add_handler(CommandHandler("deleteexercise", delete_exercise))

    dispatcher.add_handler(MessageHandler(Filters.text, text))
    
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
