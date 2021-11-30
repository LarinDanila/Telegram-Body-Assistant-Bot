## Подключение необходимых библиотек
```python
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import random 
```

## Базовые команды и функции бота бота: start, help, error

```python
def start(update, context):
    update.message.reply_text(
        'Список доступных команд:\n'
        '/help - посмотреть все доступные команды\n'
        '/createworkout - Создать тренировку\n'
        '/startworkout - Начать мою тренировку'
    )
    context.user_data['program'] = []
    context.user_data['task_time'] = 0
    context.user_data['relax_time'] = 0
    context.user_data['number_of_circles'] = 0


def help(update, context):
    update.message.reply_text(
        'Список доступных команд:\n'
        '/help - посмотреть все доступные команды\n'
        '/createworkout - Создать тренировку\n'
        '/startworkout - Начать мою тренировку'
    )


def error(update, context):
    update.message.reply_text('an error occured')
```

## Функция text, отвечающая за обработку обычных сообщений от пользователя
```python
Exercises = ['Отжимания', 'Скручивания', 'Подъемы ног']

STATE = None # STATE - переменная, содержащая информацию о текущем процессе. Далее перечисление процессов:
GET_EXERCISES = 1 # STATE == GET_EXERCISES => Пользователь вводит набор упражнений
GET_TASK_TIME = 2 # Пользователь вводит время на выполнение упражнений
GET_RELAX_TIME = 3 # Пользователь вводит время перерывов между упражнениями
GET_NUMBER_OF_CIRCLES = 4 # Пользователь вводит количество кругов в тренировке

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
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')
```

## Функции, отвечающие за создание тренировки
```python
def createworkout(update, context):
    global STATE
    update.message.reply_text(
        'Опишите свою тренировку (Введите номера упражнений через пробел). Список доступных упражнений:\n'
        '1 - Отжимания\n'
        '2 - Скручивания\n'
        '3 - Подъемы ног'
    )
    STATE = GET_EXERCISES

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
```

## Функция, активирующая тренировку, и сама функция тренировки
```python
def startworkout(update, context):
    if len(context.user_data['program']) == 0 or context.user_data['task_time'] == 0 or context.user_data['relax_time'] == 0 or context.user_data['number_of_circles'] == 0:
        update.message.reply_text('Сохраненная тренировка не найдена')
        update.message.reply_text(f'{len(context.user_data["program"])} '
                                  f'{context.user_data["task_time"]} '
                                  f'{context.user_data["relax_time"]} '
                                  f'{context.user_data["number_of_circles"]}')
    else:
        training_process(update, context)


def training_process(update, context):
    for i in range(context.user_data['number_of_circles']):
        for exercise in context.user_data['program']:
            update.message.reply_text(f'Начинаем выполнение упражнения: {Exercises[exercise - 1]}')
            time.sleep(context.user_data['task_time'])
            update.message.reply_text(f'Отлично, закончили упражнение, перерыв')
            time.sleep(context.user_data['relax_time'])
    update.message.reply_text(f'Прекрасная работа, {update.message.chat.first_name}, тренировка завершена!')


```

# Функция main, в которой включается сам бот и его функции
```python
def main():
    TOKEN = "TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("createworkout", createworkout))
    dispatcher.add_handler(CommandHandler("startworkout", startworkout))

    dispatcher.add_handler(MessageHandler(Filters.text, text))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
 ```
