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
    name = models.CharField("Название", max_length=128)
    file = models.FileField("Файл", null=True, blank=True, upload_to="files", default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class Task(models.Model):
    name = models.CharField("Название задания", max_length=128)
    text = models.CharField("Текст задания", max_length=4096)
    correct_answer = models.CharField("Правильный ответ", max_length=512)
    files = models.ManyToManyField(File, "Файлы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Homework(models.Model):
    name = models.CharField("Название", max_length=32)
    tasks = models.ManyToManyField(Task, "Задания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Домашняя работа"
        verbose_name_plural = "Домашние работы"


class Lesson(models.Model):
    name = models.CharField("Название", max_length=32)
    description = models.CharField("Описание", max_length=32)
    link = models.CharField("Ссылка", max_length=32)
    files = models.ManyToManyField(File, "Файлы", blank=True)
    homework = models.ForeignKey(Homework, "Домашняя работа", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

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
    description = models.CharField(max_length=4096)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class Chat(models.Model):
    name = models.CharField("Название", max_length=64)
    url = models.CharField("Ссылка", max_length=256)
    image = models.ImageField(null=True, blank=True, upload_to="images", default=None) #!!!!!!!!!!!!!!!!

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Course(models.Model):
    is_active = models.BooleanField("Активный", default=True)
    name = models.CharField("Название", max_length=32)
    teachers = models.ManyToManyField(Teacher, "Учителя")
    users = models.ManyToManyField(User, "Ученик")
    lessons = models.ManyToManyField(Lesson, "Уроки")
    chat = models.ManyToManyField(Chat, "Чат")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Admin(User):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Админ"
        verbose_name_plural = "Админы"


class SuperUser(Admin):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "БОГ"
        verbose_name_plural = "БОГИ"
