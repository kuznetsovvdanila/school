# Общая документация:
# et - event template
# 
# 
# 
# 
# 

from ..models import Event

# sender_info classification
class event_classification():
    lesson_closed_to_open = 0

# Основная функция для выбора параметра content на основе sender_info
def content_choice(self, sender_info : dict, choice : event_classification):
    if choice == event_classification.lesson_closed_to_open: 
        return new_lesson_et(sender_info)
    elif None:
        pass
    
# def closed_to_open_event(self):
#         return { "name" : self.name }
    
# def create_event(self, content, type):
#         event = None
#         if content is not None: 
#             event = Event.create(course=self, content=content, type=type)
#             event.save()

def new_lesson_et(sender) -> str:
    return f"Lesson \"{sender['name']}\" is available now!"