from rest_framework import exceptions
from rest_framework import status


class PasswordDoNotMatchException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': 'Passwords do not match!'}
    default_code = 'error'
