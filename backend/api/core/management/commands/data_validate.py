from datetime import datetime
import re

TYPE_ID_IS_NOT_A_NUMBER = 5
TYPE_ID_IS_NOT_ALLOWED = 6
INVALID_DATE_FORMAT = "1992-08-07T00:00:00Z"
INVALID_PRODUCT_NAME_FORMAT = "CHECK PRODUCT NAME"
INVALID_PRICE_FORMAT = 999999999
INVALID_SELLER_NAME_FORMAT = "VERIFY NAME"

VALIDATE_PRODUCT_NAME = r'^[A-Za-z -]+$'
VALIDATE_SELLER_NAME = r'^[a-zA-Z\s]+$'


def validate_type_id(type_id):
    """
        `1- Validates if the type of the id is a number`, if not
         lift returns the number the value 8, which will be used
         as a reference for errors in the Database.

         `2- if it is between 1 and 4` which are currently allowed types
         in the database, otherwise it returns 9 which will be
         used as a reference for errors in the Database.
    """
    try:
        number = int(type_id)
        if number >= 1 and number <= 4:
            return number
        return TYPE_ID_IS_NOT_ALLOWED

    except ValueError:
        return TYPE_ID_IS_NOT_A_NUMBER


def validate_date_format(date_string):
    """
        Validates if the input date of the txt document is
         in `Date - ISO Date + GMT` format, if it is
         returns the date, otherwise returns a standard date
         which will be used as a reference for errors.
    """
    date = date_string.replace(" ", "")
    try:
        formated_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        return formated_date
    except ValueError:
        return INVALID_DATE_FORMAT


def validate_product(product):
    """
        Validates that the product name is made up of letters and spaces only,
        otherwise it will return a pattern used as a reference for errors
    """
    item = product.strip()
    if bool(re.match(VALIDATE_PRODUCT_NAME, item)):
        return item
    return INVALID_PRODUCT_NAME_FORMAT


def validate_price(price):
    """
        Validates that the input value in cents is an integer value
        and greater than 0. Otherwise, it returns the default number for
        error reference.
    """
    try:
        int_price = int(price)
        if int_price > 0:
            return int_price
    except ValueError:
        return INVALID_PRICE_FORMAT


def validate_seller(seller):
    """
        Validates that the seller name is made up of letters and spaces only,
        otherwise it will return a pattern used as a reference for errors
    """
    name = seller.strip()
    if bool(re.match(VALIDATE_SELLER_NAME, name)):
        return name
    return INVALID_SELLER_NAME_FORMAT
