from secrets import choice
from typing import overload
from venv import create
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.

class Push(models.Model):

    class types(models.TextChoices):
        admin = '0', _('AdminPush')
        homework = '1', _('HomeworkPush')
        stream = '2', _('StreamPush')
        course = '3', _('CoursePush')
    
    content = models.CharField("Содержание", max_length=256)
    type = models.CharField('Тип пуша', choices=types.choices, max_length=128, default=types.admin)

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

class FileTask(models.Model):
    name = models.CharField("Название", max_length=128)
    file = models.FileField("Файл", null=True, blank=True, upload_to="files", default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл Задания"
        verbose_name_plural = "Файлы Задания"

class FileLesson(models.Model):
    name = models.CharField("Название", max_length=128)
    file = models.FileField("Файл", null=True, blank=True, upload_to="files", default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл Урока"
        verbose_name_plural = "Файлы Урока"


class Task(models.Model):
    name = models.CharField("Название задания", max_length=128)
    text = models.CharField("Текст задания", max_length=4096)
    correct_answer = models.CharField("Правильный ответ", max_length=512)
    files = models.ManyToManyField(FileTask, related_name="Файлы+", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Homework(models.Model):
    name = models.CharField("Название", max_length=32)
    tasks = models.ManyToManyField(Task, related_name="Задания+")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Домашняя работа"
        verbose_name_plural = "Домашние работы"


class Lesson(models.Model):
    class accesses(models.TextChoices):
        available = '0', _('Available')
        partavailable = '1', _('PartAvailable')
        closed = '2', _('Closed')
    
    name = models.CharField("Название", max_length=128)
    description = models.CharField("Описание", max_length=2048)
    link = models.CharField("Ссылка", max_length=256)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    files = models.ManyToManyField(FileLesson, related_name="Файлы+", blank=True)
    index = models.IntegerField("Индекс внутри курса", default=0)

    access = models.CharField("Уровень доступа",  default=accesses.closed, choices=accesses.choices, max_length=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

class Progress(models.Model):
    id_course = models.IntegerField("ID курса", default=0)
    is_bought = models.BooleanField("", default=False)
    whole_course = models.IntegerField("Весь курс", default=0)
    lessons = models.CharField("Уроки %", max_length=512, default=" ") # may be change to 1024
    tasks = models.CharField("Задачи курса", max_length=8192, default=" ")
    status_tasks = models.CharField("Задачи курса", max_length=8192, default=" ")

    # 67 50 90 for lessons : split(" ")
    # 0 1 2.3 4 5 for tasks : split(".") : split(" ")
    # 0 1 2.0 1 0 for status_tasks : split(".") : split(" ")
    # to status_tasks : 0 is default, 1 is completed, 2 is wrong

    # tasks, status_tasks
    """Парсит данные о задании и его статусе выполнения:
             формат : lesson1.lesson2.  .lessonN
             id task: 0 1 2 3.4 6 7 8.  .9 11 15 16 17  Хранится id из БД - id могут быть (будут) не упорядочены
        status_tasks: 0 1 0 2.2 1 2 0.  .0 0 1 2 1      0 is default, 1 is completed, 2 is wrong
    """
    @staticmethod
    def parseToList(tasks : str) -> list:
        Array = tasks.split('.')
        for i in range(len(Array)):
            Array[i] = Array[i].split(' ')
        #print('.'.join([' '.join(i) for i in Array]))
        return Array

    """
        Получает на вход индекс курса, парсит строку, переводит в массив, возвращает прогресс по курсу(%) int
    """
    def lessonPercentage(self, index : int) -> int:
        tasks = parseToList(self.tasks)
        status_tasks = parseToList(self.status_tasks)
        percent = round(tasks[index]/status_tasks[index].count('1'))
        return percent

    """
        Получает на вход индекс курса и прогресс по уроку int, либо добавляет прогресс по уроку, либо обновляет существующий
    """
    def lessonManage(self, index : int, percent : int) -> str:
        Array = self.lesson.split(" ")
        if index == len(Array):
            Array.append(percent)
        else:
            Array[index] = percent
        return " ".join(Array)

    """
        Передаем строку с прогрессом в % на курсе по каждому lesson: 67 50 90 for lessons : split(" ")
        
    """
    def save(self, *args, **kwargs):
        super(Progress, self).save(*args, **kwargs)
        if kwargs.lesson is not None:
            array_tasks = parseToList(self.tasks)
            array_tasks.append([i.id for i in list(kwargs.lesson.homework.tasks.all())])
            array_status_tasks = parseToList(self.status_tasks)
            array_status_tasks.append(["0" for i in range(len(list(kwargs.lesson.homework.tasks.all())))])
            self.tasks = '.'.join([' '.join(i) for i in array_tasks])
            self.lessons = '.'.join([' '.join(i) for i in array_status_tasks])
            percent = self.lessonPercentage(kwargs.lesson.index)
            self.lessons = self.lessonManage(kwargs.lesson.index, percent)

        self.whole_course = round(self.status_task.count('1')/
                (len(self.status_tasks)-self.status_tasks.count(' ')-self.status_tasks.count('.')))


    """
        Вызывается при покупке курса без начала бесплатного прохождения
    """
    # Покупка курсов
    @overload
    def bought(course):
        create(course, True)

    """
        Вызывается при начале бесплатного прохождения. Записывает
    """
    @overload
    def bought(self, course):
        lessons = list(course.lessons.filter(access=Lesson.accesses.partavailable))
        tasks = list()
        status_tasks = list()
        for i in range(len(lessons)):
            tasks.append([])
            status_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in all_tasks:
                tasks[i].append(k.id)
                status_tasks[i].append("0")
        self.tasks = '.'.join([' '.join(i) for i in tasks])
        self.status_tasks = '.'.join([' '.join(i) for i in status_tasks])
        self.lessons = " ".join(["0" for i in range(len(lessons))])
        self.is_bought = True

        
    """
        
    """
    @classmethod
    def create(cls, course, param=False):
        lessons = 0
        if param :
            lessons = course.lessons.exclude(access=Lesson.accesses.closed)
        else:
            lessons = course.lessons.filter(access=Lesson.accesses.available)
        tasks = list()
        status_tasks = list()
        for i in range(len(lessons)):
            tasks.append([])
            status_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in all_tasks:
                tasks[i].append(k.id)
                status_tasks[i].append("0")
        _tasks = '.'.join([' '.join(i) for i in tasks])
        _status_tasks = '.'.join([' '.join(i) for i in status_tasks])
        count_lessons = len(lessons)
        _lessons = " ".join(["0" for i in range(count_lessons)])
        progress = cls(lessons=_lessons, tasks=_tasks, status_tasks=_status_tasks, course=course.id, is_bought=param)
        return progress


    def __str__(self):
        return self.id_course

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class User(AbstractBaseUser):
    is_active = models.BooleanField("Активный", default=True)
    name = models.CharField("Имя", max_length=32, default="")
    surname = models.CharField("Фамилия", max_length=64, default="")
    email = models.EmailField("Почта", max_length=128)
    registered = models.DateTimeField("Зарегистрировался", default=datetime.now())
    notifications = models.ManyToManyField(Push, related_name="Уведомления+", blank=True)
    my_courses = models.CharField("Доступные курсы", max_length=2048, blank=True)
    avatar = models.ImageField("Аватар", blank=True, default=None)
    progresses = models.ManyToManyField(Progress, related_name="Прогресс по курсам+", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Teacher(User):
    description = models.CharField(max_length=8192)

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
    name = models.CharField("Название", max_length=128)
    description = models.CharField("Описание",max_length=8192)
    product_preview = models.CharField("Превью курса", max_length=2048)
    value = models.IntegerField("Стоимость", default=0)
    teachers = models.ManyToManyField(Teacher, related_name="Учителя+")
    users = models.ManyToManyField(User, related_name="Ученики+")
    trials = models.ManyToManyField(User, related_name="Триалы+")
    lessons = models.ManyToManyField(Lesson, related_name="Уроки+")
    chat = models.ManyToManyField(Chat, related_name="Чат+")

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
