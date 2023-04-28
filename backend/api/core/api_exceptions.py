from rest_framework import exceptions
from rest_framework import status


class PasswordDoNotMatchException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EmailExistsException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
