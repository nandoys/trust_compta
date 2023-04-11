from django.db.utils import OperationalError
from django.http.response import HttpResponseServerError


def db_operational_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError:
            return HttpResponseServerError('Error Establishing a DB connection')
    return inner_function
