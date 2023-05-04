import re
from school_app.models import User
from email_validate import validate

# возвращает bool и User
def authValid(login : str, password : str) -> tuple:
    truth = False
    user_instance = None
    isUser = False
    if list(login).count("@") == 1:
        isUser = User.objects.filter(email=login).exists()
        if isUser:
            user_instance = User.objects.get(email=login)
            if (user_instance.check_password(password)):
                truth = True
    else:
        isUser = User.objects.filter(phone_number=login).exists()
        if isUser:
            user_instance = User.objects.get(phone_number=login)
            if (user_instance.check_password(password)):
                truth = True
    return (truth, user_instance, "Wrong login or password")

# возвращает tuple(check : bool, error_message : string, User.id : int)
def regValid(login : str, password : str) -> tuple:
    truth = False
    error_message = ""
    user_instance = None
    print(login)

    # Проверяем на соответствие поля телефонному номеру
    if re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', login):
        isUser: bool = User.objects.filter(phone_number=login).exists()
        if not (isUser):
            user_instance = User(phone_number=login)
            user_instance.set_password(password)
            user_instance.save()
            truth = True
        else:
            error_message = "Пользователь с таким номером мобильного телефона уже существует"

     # Проверяем на соответствие поля "email"у
    elif validate(login):
        isUser : bool = User.objects.filter(email=login).exists()
        if not(isUser):
            user_instance = User(email=login)
            user_instance.set_password(password)
            user_instance.save()
            truth = True
        else:
            error_message = "Пользователь с таким email адресом уже существует"

    else:
        error_message = "Login не соответствует существующему email или номеру мобильного телефона"

    return (truth, error_message, user_instance)