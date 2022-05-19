from operator import gt
import pandas as pd
from gtts import gTTS


def generate_path(name):
    return '/home/danila/telebot_train/exercises/' + name + '.mp3'


def generate_exercises(exercises):
    for exercise in exercises:
        tts = gTTS(text=exercise, lang='ru')
        tts.save(generate_path(exercise))


def main():
    exer = pd.Series(dtype='float64')
    with open('list_of_exercises.txt', 'r') as ff:
        exer = pd.Series(ff.read().split('\n'))
        generate_exercises(exer.values)
    exer.to_csv('exercises_data.csv')
    tts = gTTS(text='Приступаем к упражнению - ', lang='ru')
    tts.save(generate_path('task_start'))
    tts = gTTS(text='Закончили упражнение, перерыв', lang='ru')
    tts.save(generate_path('task_stop'))
    tts = gTTS(text='Начинаем тренировку', lang='ru')
    tts.save(generate_path('start_training'))
    tts = gTTS(text='Тренировка окончена', lang='ru')
    tts.save(generate_path('finish_training'))
    tts = gTTS(text='Круг завершен', lang='ru')
    tts.save(generate_path('finish_circle'))


if __name__ == '__main__':
    main()