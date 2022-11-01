from typing import overload
from venv import create
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime, timedelta, timezone
from django.db.models.signals import pre_save, post_save, post_init, m2m_changed

# Create your models here.

class intf():
    @staticmethod
    def parseToList(tasks : str) -> list:
        Array = tasks.split('.')
        for i in range(len(Array)):
            Array[i] = Array[i].split(' ')
        #print('.'.join([' '.join(i) for i in Array]))
        return Array
    
    @staticmethod
    def joinToString(array : list):
        if array[0] is list:
            return '.'.join([' '.join(i) for i in array])
        elif array[0] is not list:
            return " ".join(["0" for i in range(len(array))])

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
    index = models.IntegerField("Индекс внутри homework", default=0)
    files = models.ManyToManyField(FileTask, related_name="Файлы+", blank=True)

    def checkAnswer(self, user, answer: str, path: str) -> bool:
        status = False
        if answer == self.correct_answer:
            status = True

        user.updateTaskProgress(path, status)
        return status

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Homework(models.Model):
    name = models.CharField("Название", max_length=32)
    tasks = models.ManyToManyField(Task, related_name="Задания+", blank=True)

    @classmethod
    def create(cls, name):
        homework = cls(name=name)
        return homework

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
    
    id_course = models.IntegerField("ID курса", default=0)
    name = models.CharField("Название", max_length=128)
    description = models.CharField("Описание", max_length=2048)
    link = models.CharField("Ссылка на ютуб", max_length=256)
    homework = models.ForeignKey(Homework, on_delete=models.SET_NULL, blank=True, null=True)
    files = models.ManyToManyField(FileLesson, related_name="Файлы+", blank=True)
    index = models.IntegerField("Индекс внутри курса", default=0)
    slug = models.SlugField("Часть url", blank=True)

    access = models.CharField("Уровень доступа",  default=accesses.closed, choices=accesses.choices, max_length=1)

    def setId(self, id, index):
        self.id_course = id
        self.index = index
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

@receiver(post_init, sender=Lesson)
def postRequestFields(sender, instance, **kwargs):
    instance.slug = instance.name + "_" + str(instance.id)
    homework = Homework.create(name=instance.name)
    homework.save()
    instance.homework = homework
    instance.save()

class Progress(models.Model):
    id_course = models.IntegerField("ID курса", default=0)
    is_bought = models.BooleanField("Куплено", default=False)
    whole_course = models.IntegerField("Весь курс", default=0)
    lessons = models.CharField("Уроки %", max_length=512, default=" ") # may be change to 1024
    status_tasks = models.CharField("Задачи курса (статус)", max_length=8192, default=" ")

    # 67 50 90 for lessons : split(" ")
    # 0 1 2.3 4 5 for tasks : split(".") : split(" ")
    # 0 1 2.0 1 0 for status_tasks : split(".") : split(" ")
    # to status_tasks : 0 is default, 1 is completed, 2 is wrong
    
    # tasks, status_tasks

    def lessonPercentage(self, index : int) -> int:
        status_tasks = intf.parseToList(self.status_tasks)
        percent = round(100*status_tasks[index].count('1')/len(status_tasks[index]))
        return percent

    def lessonManage(self, index : int, percent : int) -> str:
        Array = self.lesson.split(" ")
        if index == len(Array):
            Array.append(percent)
        else:
            Array[index] = percent
        return " ".join(Array)

    def taskProgress(self, lesson_index, task_index, status_code):
        # Для обновления по результатам выполнения одного Taska
        # Требуемые поля: status_code, lesson_index, task_index.

        if (lesson_index is not None) and (task_index is not None):
            array_status_tasks = intf.parseToList(self.status_tasks)

            array_status_tasks[lesson_index][task_index] = status_code

            self.status_tasks = intf.joinToString(array_status_tasks)

            percent = self.lessonPercentage(lesson_index)
            self.lessons = self.lessonManage(lesson_index, percent)

            self.whole_course = round(self.status_tasks.count('1') /
                                      (len(self.status_tasks) - self.status_tasks.count(
                                          ' ') - self.status_tasks.count('.')))
            self.save()

    def openLesson(self, lesson):
        if lesson is not None:
            array_status_tasks = intf.parseToList(self.status_tasks)

            array_status_tasks.append(["0" for i in range(len(list(lesson.homework.tasks.all())))])

            self.status_tasks = intf.joinToString(array_status_tasks)

            self.lessons = self.lessonManage(lesson.index, 0)

            self.whole_course = round(self.status_task.count('1')/
                    (len(self.status_tasks)-self.status_tasks.count(' ')-self.status_tasks.count('.')))
            self.save()

    # Покупка курсов
    @overload
    def bought(course):
        create(course, True)
    
    @overload
    def bought(self, course):
        lessons = list(course.lessons.filter(access=Lesson.accesses.partavailable))
        status_tasks = list()

        for i in range(len(lessons)):
            status_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in range(len(all_tasks)):
                status_tasks[i].append("0")

        self.status_tasks = intf.joinToString(status_tasks)
        self.lessons = intf.joinToString(lessons)
        self.is_bought = True
        self.save()

    @classmethod
    def create(cls, course, param=False):
        lessons = 0
        if param : lessons = course.lessons.exclude(access=Lesson.accesses.closed)
        else: lessons = course.lessons.filter(access=Lesson.accesses.available)

        status_tasks = list()

        for i in range(len(lessons)):
            status_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in range(len(all_tasks)):
                status_tasks[i].append("0")
        
        _status_tasks = intf.joinToString(status_tasks)
        _lessons = intf.joinToString(lessons)
        progress = cls(lessons=_lessons, status_tasks=_status_tasks, course=course.id, is_bought=param)
        return progress


    def __str__(self):
        return str(self.id_course)

    class Meta:
        verbose_name = "Прогресс по курсу"
        verbose_name_plural = "Прогресс по курсам"

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

    def updateTaskProgress(self, path: str, status_code: bool):
        pathlist = path.split('/')
        id_course = pathlist[0].split("_")[1]
        lesson_index = pathlist[1].split("_")[1]
        task_index = pathlist[2]
        progress = self.progresses.get(id_course=id_course)
        progress.taskProgress(lesson_index=lesson_index, task_index=task_index, status_code=status_code)

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

    @classmethod
    def create(cls, name, url):
        chat = cls(name=name, url=url)
        return chat

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Course(models.Model):
    #Main
    name = models.CharField("Название", max_length=128)
    description = models.CharField("Описание",max_length=8192)
    product_preview = models.CharField("Превью курса", max_length=2048)
    value = models.IntegerField("Стоимость", default=0)
    slug = models.SlugField("Часть url", blank=True)

    #Atributes
    duration = models.DurationField("Длительность", blank=True, default=timedelta(days=20, hours=10))
    date_open = models.DateField("Дата начала", blank=True, auto_now_add=True)
    repeat = models.DateField("Частота добавления уроков", blank=True, auto_now_add=True)
    is_active = models.BooleanField("Активный", default=True)

    #M2M
    teachers = models.ManyToManyField(Teacher, related_name="Учителя+")
    users = models.ManyToManyField(User, related_name="Ученики+")
    trials = models.ManyToManyField(User, related_name="Триалы+")
    lessons = models.ManyToManyField(Lesson, related_name="Уроки+") # Teacher have access
    chat = models.ManyToManyField(Chat, related_name="Чат+")

    def updateLessons(self):
        lessons = self.lessons.all()
        print(lessons)
        for i in range(len(lessons)):
            lessons[i].setId(self.id, i)
    
    def save(self, *args, **kwargs):
        self.is_active = True
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

@receiver(m2m_changed, sender=Course.lessons.through)
def postRequestM2M(sender, instance, action, pk_set, **kwargs):
    instance.updateLessons()

# @receiver(m2m_changed, sender=Course.chat.through)
# def postRequestM2M(sender, instance, action, pk_set, **kwargs):
#     if action == 'post_add':
#         if instance.id not in pk_set:
#             e1 = Chat.create(name="hui1", url="")
#             e2 = Chat.create(name="hui1", url="")
#             e3 = Chat.create(name="hui1", url="")
#             e1.save() ; e2.save() ; e3.save()
#             instance.chat.add(e1, e2, e3)

@receiver(post_save, sender=Course)
def postRequestFields(sender, instance, created, **kwargs):
    if created:
        instance.slug = "_" + str(instance.id)

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
