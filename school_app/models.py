from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from datetime import datetime

# Create your models here.


class Push(models.Model):
    content = models.CharField("Содержание", max_length=256)
    type = models.IntegerField("Источник уведомления", default=1)

    # def save(self, parametr: int, user, text: str):
    #     if text is not None:
    #         content = text
    #     elif parametr==1:
    #         txt = "1"
    #         self.content = user.name + txt
    #     elif parametr==2:
    #         txt = "1"
    #         self.content = user.name + txt

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class File(models.Model):
    pass


class Task(models.Model):
    name = models.CharField("Название", max_length=32)
    text = models.CharField("Фамилия", max_length=32)
    correct_answer = models.CharField("Правильный ответ", max_length=32)
    files = models.ManyToManyField(File, "Файлы")


class Homework(models.Model):
    name = models.CharField("Название", max_length=32)
    tasks = models.ManyToManyField(Task, "Задания")


class Lesson(models.Model):
    name = models.CharField("Название", max_length=32)
    description = models.CharField("Описание", max_length=32)
    link = models.CharField("Ссылка", max_length=32)
    files = models.ManyToManyField(File, "Файлы", blank=True)
    homework = models.ForeignKey(Homework, "Домашняя работа", on_delete=models.CASCADE)


# class Progress(models.Model):
#


class User(AbstractBaseUser):
    is_active = models.BooleanField("Активный", default=True)
    name = models.CharField("Имя", max_length=32, default="Артём)")
    surname = models.CharField("Фамилия", max_length=32, default="Самотохин)")
    email = models.EmailField("Почта", max_length=32)
    registered = models.DateTimeField("Зарегистрировался", default=datetime.now())
    notifications = models.ManyToManyField(Push, "Уведомления")
    available_courses = models.CharField("Доступные курсы", max_length=2048)

    # progresses = models.ManyToManyField(Progress)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Teacher(User):
    pass

# class Chat(models.Model):
#


class Course(models.Model):
    is_active = models.BooleanField("Активный", default=True)
    name = models.CharField("Название", max_length=32)


class Admin(User):
    pass


class SuperUser(Admin):
    pass
