from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from models import Lesson, Course, Calendar
from django.db.models import Max

@receiver(pre_save, sender=(Course, Lesson))
def try_to_update_access(sender, instance, **kwargs):
    pk = instance.pk
    if pk is not None:
        access = instance.access
        original_access = sender.objects.get(pk=pk).access
        if original_access == sender.accesses.closed and access != original_access:
            if not(instance.check_to_open_access()):
                instance.access = original_access
            else:
                pass

@receiver(post_save, sender=Course)
def course_init(sender, instance, created):
    if created:
        calendar = Calendar.objects.create()
        instance.calendar = calendar
        instance.save()

@receiver(post_save, sender=Lesson)
def lesson_init(sender, instance, created):
    if created:
        instance.index = instance.course.lessons.aggregate(Max("index"))["index__max"] + 1
        instance.save()

@receiver(post_save, sender=Course)
def upload_changes_to_users(sender, instance, **kwargs):
    pass

@receiver(post_save, sender=Lesson)
def upload_changes_from_lessons(sender, instance, created, update_fields):
    if 'access' in update_fields and instance.access != Lesson.accesses.closed:
        instance.course.update_accesses(instance.access)
    if 'date_to_start' in update_fields:
        instance.course.send_new_time(instance.id, instance.name)