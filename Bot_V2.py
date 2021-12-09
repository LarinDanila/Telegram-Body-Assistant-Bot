from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import random


# function to handle the /start command
def start(update, context):
    update.message.reply_text(
        'Список доступных команд:\n'
        '/help - посмотреть все доступные команды\n'
        '/createworkout - Создать тренировку\n'
        '/startworkout - Начать мою тренировку\n'
        '/getworkoutcode - Получить код сохраненной тренировки\n'
        '/setworkoutcode - Сохранить тренировку, используя код'
    )
    context.user_data['program'] = []
    context.user_data['task_time'] = 0
    context.user_data['relax_time'] = 0
    context.user_data['number_of_circles'] = 0

# function to handle the /help command


def help(update, context):
    update.message.reply_text(
        'Список доступных команд:\n'
        '/help - посмотреть все доступные команды\n'
        '/createworkout - Создать тренировку\n'
        '/startworkout - Начать мою тренировку\n'
        '/getworkoutcode - Получить код сохраненной тренировки\n'
        '/setworkoutcode - Сохранить тренировку, используя код'
    )
# function to handle errors occured in the dispatcher


def error(update, context):
    update.message.reply_text('an error occured')
# function to handle normal text


Exercises = ['Отжимания', 'Скручивания', 'Подъемы ног']
STATE = None
GET_EXERCISES = 1
GET_TASK_TIME = 2
GET_RELAX_TIME = 3
GET_NUMBER_OF_CIRCLES = 4
SET_TRAINING = 5
def text(update, context):
    global STATE
    if STATE == GET_EXERCISES:
        return get_exercises(update, context)
    if STATE == GET_TASK_TIME:
        return get_task_time(update, context)
    if STATE == GET_RELAX_TIME:
        return get_relax_time(update, context)
    if STATE == GET_NUMBER_OF_CIRCLES:
        return get_number_of_circles(update, context)
    if STATE == SET_TRAINING:
        return set_training(update, context)
    text_received = update.message.text
    if text_received == 'stop':
        context.user_data['stop'] = True
    else:
        update.message.reply_text(f'did you said "{text_received}" ?')


def createworkout(update, context):
    global STATE
    update.message.reply_text(
        'Опишите свою тренировку (Введите номера упражнений через пробел). Список доступных упражнений:\n'
        '1 - Отжимания\n'
        '2 - Скручивания\n'
        '3 - Подъемы ног'
    )
    STATE = GET_EXERCISES


def startworkout(update, context):
    if len(context.user_data['program']) == 0 or context.user_data['task_time'] == 0 or context.user_data['relax_time'] == 0 or context.user_data['number_of_circles'] == 0:
        update.message.reply_text('Сохраненная тренировка не найдена')
    else:
        training_process(update, context)


def get_exercises(update, context):
    global STATE
    try:
        training = list(map(int, update.message.text.split()))
        if len(training) == 0:
            raise ValueError
        for x in training:
            if x < 1 or x > len(Exercises):
                raise ValueError
        context.user_data['program'] = training
        STATE = GET_TASK_TIME
        update.message.reply_text(
            'Введите время, в течении которого вы будете выполнять каждое упражнение:'
        )
    except:
        update.message.reply_text('Пожалуйста, введите корректную программу тренировки')


def get_task_time(update, context):
    global STATE
    try:
        task_time = int(update.message.text)
        if task_time < 1:
            raise ValueError
        context.user_data['task_time'] = task_time
        STATE = GET_RELAX_TIME
        update.message.reply_text(
            'Введите время отдыха между подходами:'
        )
    except:
        update.message.reply_text('Пожалуйста, введите корректное время выполнения упражнений')


def get_relax_time(update, context):
    global STATE
    try:
        relax_time = int(update.message.text)
        if relax_time < 1:
            raise ValueError
        context.user_data['relax_time'] = relax_time
        STATE = GET_NUMBER_OF_CIRCLES
        update.message.reply_text(
            'Введите количество кругов в тренировке:'
        )
    except:
        update.message.reply_text('Пожалуйста, введите корректное время перерывов между упражнениями')


def get_number_of_circles(update, context):
    global STATE
    try:
        number_of_circles = int(update.message.text)
        if number_of_circles < 1:
            raise ValueError
        context.user_data['number_of_circles'] = number_of_circles
        update.message.reply_text(
            'Ваша тренировка сохранена.'
        )
        STATE = None
    except:
        update.message.reply_text('Пожалуйста, введите корректное число кругов в тренировке')


def training_process(update, context):
    for i in range(context.user_data['number_of_circles']):
        for exercise in context.user_data['program']:
            update.message.reply_text(f'Начинаем выполнение упражнения: {Exercises[exercise - 1]}')
            time.sleep(context.user_data['task_time'])
            update.message.reply_text(f'Отлично, закончили упражнение, перерыв')
            time.sleep(context.user_data['relax_time'])
    update.message.reply_text(f'Прекрасная работа, {update.message.chat.first_name}, тренировка завершена!')


def copy_training(update, context):
    if len(context.user_data['program']) == 0 or context.user_data['task_time'] == 0 or context.user_data['relax_time'] == 0 or context.user_data['number_of_circles'] == 0:
        update.message.reply_text('Сохраненная тренировка не найдена')
    else:
        code = ""
        code += str(context.user_data['task_time'])
        code += '.'
        code += str(context.user_data['relax_time'])
        code += '.'
        code += str(context.user_data['number_of_circles'])
        code += '.'
        code += '.'.join(map(str, context.user_data['program']))
        update.message.reply_text(f'Код тренировки:')
        update.message.reply_text(code)


def set_code_training(update, context):
    global STATE
    update.message.reply_text(f'{update.message.chat.first_name}, пожалуйста, введите код тренировки')
    STATE = SET_TRAINING


def set_training(update, context):
    global STATE
    try:
        code = list(map(int, update.message.text.split('.')))
        if len(code) < 4:
            raise ValueError
        if code[0] < 1 or code[1] < 1 or code[2] < 1:
            raise ValueError
        context.user_data['task_time'] = code[0]
        context.user_data['relax_time'] = code[1]
        context.user_data['number_of_circles'] = code[2]
        train = []
        for i in code[3:]:
            if i < 1 or i > len(Exercises):
                raise ValueError
            train.append(i)
        context.user_data['program'] = train
        update.message.reply_text('Тренировка сохранена.')
        STATE = None
    except:
        update.message.reply_text('Пожалуйста, введите корректный код тренировки')



def main():
    TOKEN = "2135852047:AAGEWFkoTmPFtqtAqQCJLoGjeZyqa60zplE"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("createworkout", createworkout))
    dispatcher.add_handler(CommandHandler("startworkout", startworkout))
    dispatcher.add_handler(CommandHandler("getworkoutcode", copy_training))
    dispatcher.add_handler(CommandHandler("setworkoutcode", set_code_training))


    # handlers normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # handler for errors
    dispatcher.add_error_handler(error)

    # start the bot
    updater.start_polling()

    # tun bot until CTRL-C
    updater.idle()


if __name__ == '__main__':
    main()
