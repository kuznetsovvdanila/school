from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from models import Lesson, Course, Calendar
from django.db.models import Max
from utils.websocket_observer import observe_lesson

# Проверка возможности внесения изменений в поле access. 
# При невозможности изменения значение возвращается к оригинальному.
@receiver(pre_save, sender=(Course, Lesson))
def try_to_update_access(sender, instance, **kwargs):
    if instance.pk is not None:
        original_access = sender.objects.get(pk=instance.pk).access
        if original_access == sender.accesses.closed and instance.access != original_access:
            if not(instance.check_to_open_access()):
                instance.access = original_access
            else:
                pass

# Инициализация курса. Создание календаря связанного с текущим курсом.
@receiver(post_save, sender=Course)
def course_init(sender, instance, created):
    if created:
        calendar = Calendar.objects.create()
        instance.calendar = calendar
        instance.save() # Потестить без сейва
    else:
        pass

# Изменения в Course, которые влияют на информацию связанную с пользователями и обрабатываются с 
# целью передачи им актуальных данных.
# @receiver(post_save, sender=Course)
# def upload_changes_to_users(sender, instance, **kwargs):
#     pass
        
@receiver(post_save, sender=Lesson)
def lesson_init(sender, instance, created, update_fields):
    # Инициализация лессона. Добавление информации о Lesson.index и проброс изменений в Calendar
    if created:
        instance.index = instance.course.lessons.aggregate(Max("index"))["index__max"] + 1
        instance.save() # Потестить без сейва
        instance.course.set_datetime(instance.id, instance.name, instance.date_to_start, instance.index, instance.slug_pk)
    # Изменение лессона. Отслеживание изменений в доступе и Calendar с последующей передачей актуальных данных   
    else:
        if 'access' in update_fields and instance.access != sender.accesses.closed:
            instance.course.update_accesses(instance.access)
        if 'date_to_start' in update_fields or 'name' in update_fields:
            instance.course.calendar.set_datetime(instance.id, instance.name, instance.date_to_start, instance.index, instance.slug_pk)
        
        observe_lesson(instance)