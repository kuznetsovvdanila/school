from django.db import models
from django.db.models.query import QuerySet

# User
class UserCourses(models.Manager):
   def get_user_courses(self, user_id):
        try:
            user = self.get_queryset().get(id=user_id)
            courses_bought = user.courses.all()
            courses_trial = user.courses_trial.all()
            return courses_bought | courses_trial
        except self.model.DoesNotExist as e:
            raise(e)

# Course
class AccessFilterManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(accesses__in=[self.__class__.accesses.wait_for_begin, self.__class__.accesses.is_active])

