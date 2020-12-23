import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid
)


COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    except MultipleObjectsReturned:
        print("Найдено несколько школьников с таким именем!")
    except ObjectDoesNotExist:
        print("Школьник с таким именем не найден!")


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
    except MultipleObjectsReturned:
        print("Найдено несколько школьников с таким именем!")
    except ObjectDoesNotExist:
        print("Школьник с таким именем не найден!")


def create_commendation(schoolkid_name, lesson_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        if not lesson_name:
            print("Наименование предмета не должно быть пустым!")
            return
        lessons = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title__contains=lesson_name
        )
        if not lessons:
            print("Отсутствуют доступные уроки! Проверьте наименование предмета!")
            return
        last_lesson = lessons.order_by('-date').first()
        for lesson in lessons:
            if not Commendation.objects.filter(
                created=last_lesson.date,
                schoolkid=schoolkid,
                subject=lesson.subject,
                teacher=lesson.teacher
            ).exists():
                Commendation.objects.create(
                    text=random.choice(COMMENDATIONS),
                    created=last_lesson.date,
                    schoolkid=schoolkid,
                    subject=lesson.subject,
                    teacher=lesson.teacher
                )
                break
    except MultipleObjectsReturned:
        print("Найдено несколько школьников с таким именем!")
    except ObjectDoesNotExist:
        print("Школьник с таким именем не найден!")
