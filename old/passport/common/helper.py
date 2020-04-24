from rest_framework import status
from datetime import datetime
from django.utils import timezone
import bcrypt, uuid, hashlib, datetime as parent_datetime
from django.conf import settings
import urllib

""" PASSWORD SECTION """

def check_password(password, encrypt_pass):
    return bcrypt.hashpw(password.encode('UTF_8'), encrypt_pass.encode('UTF_8')) == encrypt_pass


def encrypt_password(password):
    hashed = bcrypt.hashpw(str(password), bcrypt.gensalt(10))
    return hashed


def encrypt_sha256(password):
    hash_password = hashlib.sha256(password).hexdigest()
    return hash_password

""" DATE SECTION """

def convert_date(given_date, type = "database-complete"):
    converted_date = given_date
    if type == "database-complete":
        converted_date = datetime.strftime(given_date, "%Y-%m-%d %H:%M:%S")
    elif type == "database-date":
        converted_date = datetime.strftime(given_date, "%Y-%m-%d")
    elif type == "human-complete":
        converted_date = datetime.strftime(given_date, "%d %B %Y %H:%M:%S")
    elif type == "human-date":
        converted_date = datetime.strftime(given_date, "%d %B %Y")
    elif type == "time":
        converted_date = datetime.strftime(given_date, "%H:%M:%S")
    return converted_date

def add_days_from_today(days):
    return (timezone.now() + timezone.timedelta(days = days))


def add_minutes_from_now(minutes):
    return (timezone.now() + timezone.timedelta(minutes = minutes))


def get_client_ip(request):
    """ IP SECTION """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def random_string():
    """ Generate Random String """
    return str(uuid.uuid4())


def get_authorization(request):
    """ Get Authorization Code """
    return request.META.get("HTTP_X_AUTHORIZATION")


def response():
    """ Get Response """
    context = {
        "message": "something went wrong",
        "result" : None,
        "code"   : status.HTTP_400_BAD_REQUEST
    }
    return context


def convert_url(url, grant_code):
    """ Create Query String URL """
    return url + "?" + urllib.urlencode({'grant_code': grant_code})