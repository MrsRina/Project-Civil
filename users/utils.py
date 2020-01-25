'''
Módule for user tools definition.
'''
from datetime import datetime, date
from functools import wraps
from black_list.models import TokenBlackList


# TODO melhorar esta validação posteriormente
def is_adult(birth_date):
    '''
    Validate if the user is and adult_person
    given the birth date.

    param birth_date: <date>
    return: <bool>
    '''

    now = datetime.now().date()
    age = now.year - birth_date.year - \
            ((now.month, now.day) < (birth_date.month, birth_date.day))
    if age > 18:
        return True
    return False

# A principio so funciona se o token vier na forma:
# "Authorization": "JWT token""
# TODO implementar uma alterantiva para receber Bearer token
def access_required(function):
    '''
    Verify if the user is logged on the system.
    '''
    @wraps(function)
    def decorated(*args, **kwargs):
        user_token = args[1].context.META.get('HTTP_AUTHORIZATION')
        is_black_listed = TokenBlackList.objects.filter(token=user_token)
        if is_black_listed:
            raise Exception('Session Expired, please log in again!')

        user = args[1].context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return function(*args, **kwargs)
    return decorated
