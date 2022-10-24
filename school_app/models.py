from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

# Create your models here.


class Push(models.Model):
    pass


class File(models.Model):
    pass


class Task(models.Model):
    name = models.CharField()
    text = models.CharField()
    correct_answer = models.CharField()
    files = models.ManyToManyField(File)


class Homework(models.Model):
    name = models.CharField()
    tasks = models.ManyToManyField(Task)


class Lesson(models.Model):
    name = models.CharField()
    description = models.CharField()
    link = models.CharField()
    files = models.ManyToManyField(File, blank=True)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)


# class Progress(models.Model):
#


class User(AbstractBaseUser):
    is_active = models.BooleanField(default=True)
    name = models.CharField(default="Артём)")
    surname = models.CharField(default="Самотохин)")
    email = models.EmailField("Почта")
    registered = models.DateTimeField()
    notifications = models.ManyToManyField(Push)
    available_courses = models.CharField()

    # progresses = models.ManyToManyField(Progress)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Teacher(User):
    pass

# class Chat(models.Model):
#


class Course(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField()


class Admin(User):
    pass

class SuperUser(Admin):
    pass
