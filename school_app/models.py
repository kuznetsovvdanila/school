from typing import overload
import django
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime, timedelta, timezone
from django.db.models.signals import pre_save, post_save, post_init, m2m_changed
import json

# Create your models here.

class intf():
    @staticmethod
    def parseToList(tasks: str) -> list:
        Array = tasks.split('.')
        for i in range(len(Array)):
            Array[i] = Array[i].split(' ')
        # print('.'.join([' '.join(i) for i in Array]))
        return Array

    @staticmethod
    def joinToString(array: list):
        if type(array[0]) is list: #for status_task
            return '.'.join([' '.join(i) for i in array])
        elif type(array[0]) is not list: # for lessons [89 78 0 15] %
            return " ".join(["0" for i in range(len(array))]) # вызывается при создании прогресса для лессонов


    @staticmethod
    def statusCode(status_code: bool) -> int:
        if status_code:
            return 1  # правильный ответ
        else:
            return 2  # неправильный ответ

class Tag(models.Model):
    name = models.CharField("Название", max_length=63, unique=True)

    def str(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

class Event(models.Model):
    class types(models.TextChoices):
        admin = '0', _('AdminNotification')
        homework = '1', _('HomeworkNotification')
        stream = '2', _('StreamNotification')
        course = '3', _('CourseNotification')

    created = models.DateTimeField("Создан", default=django.utils.timezone.now)
    content = models.CharField("Содержание", max_length=255)
    type = models.CharField('Тип уведомления', choices=types.choices, max_length=127, default=types.admin)
    #link = models.URLField('') ссылка на зону

    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="events", null=True, blank=True)

    @classmethod
    def create(cls, course, content, type):
        event = cls(course=course, content=content, type=type)
        return event

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Шаблон события"
        verbose_name_plural = "Шаблоны событий"

class Notification(models.Model):
    template_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="notifications")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notifications")

    def finish(self):
        return f"Привет {self.user.name}! {self.template_event.content}"

    def __str__(self):
        return "f{self.user.email} - f{self.template_event.content}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class FileTask(models.Model):
    name = models.CharField("Название", max_length=127)
    file = models.FileField("Файл", null=True, blank=True, upload_to="Tasks_files")

    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="task_files")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл Задания"
        verbose_name_plural = "Файлы Задания"


class FileLesson(models.Model):
    name = models.CharField("Название", max_length=127)
    file = models.FileField("Файл", null=True, blank=True, upload_to="Lessons_files")

    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE, related_name="lesson_files")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл Урока"
        verbose_name_plural = "Файлы Урока"


class Task(models.Model):
    name = models.CharField("Название задания", max_length=127)
    text = models.CharField("Текст задания", max_length=4095)
    correct_answer = models.CharField("Правильный ответ", max_length=511)
    index = models.IntegerField("Индекс внутри homework", default=0)

    homework = models.ForeignKey("Homework", on_delete=models.CASCADE, related_name="tasks")

    def checkAnswer(self, user, answer: str, path: str = None) -> bool:
        status = False
        if answer == self.correct_answer:
            status = True

        if path is not None:
            user.updateTaskProgress(path, status)
            return status
        return intf.statusCode(status)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

# Добавить закрытый доступ, для отложенного открытия.
class Homework(models.Model):
    name = models.CharField("Название", max_length=31)

    @classmethod
    def create(cls, name):
        homework = cls(name=name)
        return homework

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Домашняя работа"
        verbose_name_plural = "Домашние работы"

# Сделать отложенное открытие
class Lesson(models.Model):
    class accesses(models.TextChoices):
        available = '0', _('Available')
        partavailable = '1', _('PartAvailable')
        closed = '2', _('Closed')

    name = models.CharField("Название", max_length=127)
    description = models.CharField("Описание", max_length=2047)
    link = models.URLField("Ссылка на ютуб", max_length=255)
    index = models.IntegerField("Индекс внутри курса", default=0)
    date_to_start = models.DateTimeField("Дата:Время начала", default=django.utils.timezone.now)
    slug = models.SlugField("Часть url")
    access = models.CharField("Уровень доступа", default=accesses.closed, choices=accesses.choices, max_length=1)

    homework = models.OneToOneField(Homework, on_delete=models.SET_NULL, related_name="lesson", blank=True, null=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="lessons")

    @property
    def getTasks(self) -> int :
        return len(self.homework.tasks.all())
    
    @property
    def slug_pk(self) -> str :
        return "%s_%s" % (self.slug, self.index)
        
    def check_to_open_access(self):
        def check_access() -> bool:
            homework = self.homework
            if homework:
                if homework.tasks.count() > 0:
                    return True
            return False

        return check_access()

    # self.course.create_event(content=content_choice(sender_info=self.closed_to_open_event(),
    # choice=event_classification.lesson_closed_to_open), type=Event.types.course)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"


class Progress(models.Model):
    id_course = models.CharField("ID course", max_length=31)
    is_bought = models.BooleanField("Куплено", default=False)
    whole_course = models.IntegerField("Весь курс", default=0)
    lessons = models.CharField("Уроки %", max_length=511, default=" ")  # may be change to 1024
    status_tasks = models.CharField("Задачи курса (статус)", max_length=2047, default=" ")
    answer_tasks = models.CharField("Ответы на задания", max_length=4095, default=" ")

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="progresses")

    # 67 50 90 for lessons : split(" ")
    # 0 1 2.0 1 0 for status_tasks : split(".") : split(" ")
    # to status_tasks : 0 is default, 1 is completed, 2 is wrong

    # tasks, status_tasks

    # Вызывается из taskProgress,... ; возвращает процент выполненных task по уроку
    def lessonPercentage(self, index: int) -> int:
        status_tasks = intf.parseToList(str(self.status_tasks))
        percent = round(100 * status_tasks[index].count('1') / len(status_tasks[index]))
        return percent

    # Вызывается из taskProgress,openLesson ; возвращает массив с процентами по lesson`ам
    def lessonManage(self, index: int, percent: str) -> str:
        Array = self.lessons.split(" ")
        if index == len(Array):
            Array.append(percent)
        else:
            Array[index] = percent
        return " ".join(Array)

    # Вызываетя из updateTaskProgress, обновляет статусы тасков и прогрессы по курсу и урокам
    # Для обновления по результатам выполнения одного Taska
    def taskProgress(self, lesson_index : int, task_index : int, status_code : int, answer : str):
        if (lesson_index is not None) and (task_index is not None):
            if status_code == 1:
                answers = intf.parseToList(self.answer_tasks)
                answers[lesson_index][task_index] = answer
                self.answer_tasks = intf.joinToString(answers)

            array_status_tasks = intf.parseToList(str(self.status_tasks))

            array_status_tasks[lesson_index][task_index] = str(status_code)

            self.status_tasks = intf.joinToString(array_status_tasks)
            self.save()

            percent = self.lessonPercentage(lesson_index)
            self.lessons = self.lessonManage(lesson_index, str(percent))

            self.whole_course = round(self.status_tasks.count('1') /
                                      (len(self.status_tasks) - self.status_tasks.count(
                                          ' ') - self.status_tasks.count('.')))
            self.save()

    # Вызывается из !!!!!!!!!!!!!!!!!
    def openLesson(self, lesson):
        if lesson is not None:
            array_status_tasks = intf.parseToList(str(self.status_tasks))
            array_answer_tasks = intf.parseToList(self.answer_tasks)

            array_status_tasks.append(["0" for i in range(len(list(lesson.homework.tasks.all())))])
            array_answer_tasks.append(["null" for i in range(len(list(lesson.homework.tasks.all())))])

            self.status_tasks = intf.joinToString(array_status_tasks)
            self.answer_tasks = intf.joinToString(array_answer_tasks)

            self.lessons = self.lessonManage(lesson.index, "0")

            self.whole_course = round(self.status_task.count('1') /
                    (len(self.status_tasks) - self.status_tasks.count(' ') - self.status_tasks.count('.')))
            self.save()

    # вызывается из вивсов при покупке пользователем курса, если пользователь не отправлял таски(нет progress)
    @overload
    def bought(course):
        Progress.create(course, True).save()  # параметр доступа для create

    # вызывается из вивсов при покупке пользователем курса, если пользователь отправлял таски(есть progress)
    @overload
    def bought(self, course):
        lessons = list(course.lessons.filter(access=Lesson.accesses.partavailable))
        status_tasks = list()
        answer_tasks = list()

        for i in range(len(lessons)):
            status_tasks.append([])
            answer_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in range(len(all_tasks)):
                status_tasks[i].append("0")
                answer_tasks[i].append("null")

        self.status_tasks = intf.joinToString(status_tasks)
        self.answer_tasks = intf.joinToString(answer_tasks)
        self.lessons = intf.joinToString(lessons)
        self.is_bought = True
        self.save()

    # вызывается из bought при покупке курса без Progress
    @classmethod
    def create(cls, course, param=False):  # параметр (куплен ли курс) передается из bought
        lessons = 0
        if param:
            lessons = course.lessons.exclude(access=Lesson.accesses.closed)
        else:
            lessons = course.lessons.filter(access=Lesson.accesses.available)  # без оплаты записываются открытые уроки

        status_tasks = list()
        answer_tasks = list()

        for i in range(len(lessons)):
            status_tasks.append([])
            answer_tasks.append([])
            all_tasks = list(lessons[i].homework.tasks.all())
            for k in range(len(all_tasks)):
                status_tasks[i].append("0")
                answer_tasks[i].append("null")

        _answer_tasks = intf.joinToString(answer_tasks)
        _status_tasks = intf.joinToString(status_tasks)
        _lessons = intf.joinToString(lessons)
        progress = cls(id_course=course.id, lessons=_lessons, status_tasks=_status_tasks, 
                       answer_tasks=_answer_tasks, is_bought=param) #куплен ли курс зависит от параметра
        return progress

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "Прогресс по курсу"
        verbose_name_plural = "Прогресс по курсам"


class User(AbstractBaseUser):
    is_active = models.BooleanField("Активный", default=True)
    name = models.CharField("Имя", max_length=63)
    surname = models.CharField("Фамилия", max_length=63, null=True, blank=True)
    grade = models.CharField("Класс/КолледжУник/Год", max_length=31, null=True, blank=True) 
    email = models.EmailField("Почта", max_length=127, null=True, blank=True, unique=True)
    phone_number = models.CharField("Номер телефона", max_length=31, null=True, blank=True, unique=True)
    registered = models.DateTimeField("Зарегистрировался", default=django.utils.timezone.now)
    avatar = models.ImageField("Аватар", blank=True, null=True, upload_to="avatar")

    completed = models.BooleanField("Закончена авторизация", default=False, 
            help_text="проверка на то закончил ли пользователь регистрацию")
    
    unchecked_lessons = models.JSONField("Непросмотренные уроки", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def registered_datetime(self) -> str : return self.registered.strftime("%H:%M:%S, %m/%d/%Y")

    # вызывается из checkAnswer, записывает данные по заданию, вызывает taskProgress, где прогресс обновляется
    def updateTaskProgress(self, path: str, status_code: bool):
        pathlist = path.split('/')
        id_course = pathlist[0].split("_")[1]
        lesson_index = pathlist[1].split("_")[1]
        task_index = pathlist[2]
        progress = self.progresses.get(id_course=id_course)
        progress.taskProgress(lesson_index=lesson_index, task_index=task_index,
                              status_code=intf.statusCode(status_code))
        
    def update_unchecked_lessons(self, course_id):
        pass
        # Need to update JSONField and inspect the Progress to call openLesson or smthg


    def __str__(self):
        return f"{self.email} {self.phone_number}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Teacher(User):
    description = models.CharField("Описание", max_length=8191)
    telegram_link = models.URLField("Ссылка на телеграм", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class Chat(models.Model):
    name = models.CharField("Название", max_length=63)
    url = models.URLField("Ссылка", max_length=255)
    image = models.ImageField("Аватар чата", null=True, blank=True, upload_to="chat_avatar")

    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="chats")

    @classmethod
    def create(cls, name : str, url : str):
        chat = cls(name=name, url=url)
        return chat

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

class Calendar(models.Model):
    date_storage = models.JSONField("Хранение дат", null=True, blank=True)

    def set_datetime(self, lesson_id, lesson_name, lesson_date_to_start, index, lesson_slug):
        dates : dict = json.loads(self.date_storage)
        new_datetime = {
            lesson_id : {
                "name" : lesson_name,
                "date_to_start" : lesson_date_to_start,
                "slug" : lesson_slug
            }
        }
        if lesson_id not in dates.keys():
            dates.update(new_datetime)
        else:
            dates[lesson_id] = new_datetime[lesson_id]
        self.date_storage = json.dumps(dates)
        self.save()

    def __str__(self):
        return "%s_%s" % (self.course.name, self.course.date_open)

    class Meta:
        verbose_name = "Календарь"
        verbose_name_plural = "Календари"

class Course(models.Model):

    class accesses(models.IntegerChoices):
        closed = 0, _('закрытый')
        is_active = 1, _('активен')
        is_archive = 2, _('архив')

    # Main
    name = models.CharField("Название", max_length=127)
    description = models.CharField("Описание", max_length=8191)
    product_preview = models.CharField("Превью курса", max_length=2047)
    value = models.IntegerField("Стоимость", default=1)
    slug = models.SlugField("URL", unique=True)

    # Atributes
    duration = models.DurationField("Длительность", default=timedelta(days=20, hours=10))
    date_open = models.DateField("Дата начала", blank=True, auto_now_add=True)
    lesson_stream_duration = models.IntegerField("Суммарная длительность уроков", default=100, help_text="длительность записана в часах")
    repeat = models.DateField("Частота добавления уроков", blank=True, auto_now_add=True)
    access = models.IntegerField("Активный",  default=accesses.closed, choices=accesses.choices)

    calendar = models.OneToOneField(Calendar, on_delete=models.PROTECT, related_name="course", null=True, blank=True)

    # M2M
    teachers = models.ManyToManyField(Teacher, related_name="courses_teacher")
    users = models.ManyToManyField(User, related_name="courses")
    trials = models.ManyToManyField(User, related_name="courses_trial")
    tags = models.ManyToManyField(Tag, related_name="courses")

    @property
    def lessonsCount(self) -> int:
        return len(self.lessons.all())

    # вызывается из вивсов при покупке пользователем курса
    def addUser(self, user):
        self.users.add(user)
        self.save()

    def addTrial(self, user):
        self.trials.add(user)
        self.save()

    def check_to_open_access(self):

        return True

    def update_accesses(self, lesson_access: Lesson.accesses):
        if lesson_access == Lesson.accesses.available:
            for user in self.trials.all() | self.users.all():
                user.update_unchecked_lessons(self.id)
        elif lesson_access == Lesson.accesses.partavailable:
            for user in self.users.all():
                user.update_unchecked_lessons(self.id)

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
