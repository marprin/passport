from oauth.models import Grant, Client, AccessToken
from common.constants import (
    UserNotFound,
    InvalidPayload,
    MissingClientKey,
    ClientNotFound,
    SignatureNotValid,
)
from user.models import User, LoginEvent
from common.utils import merge_url_with_new_query_string
from django.core.cache import cache
from uuid import uuid4
import base64
import bcrypt
import json
import hashlib
import requests


def check_user(email: str, password: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise User.DoesNotExist(UserNotFound)

    is_pwd_valid = validate_password(user.password, password)
    if is_pwd_valid is False:
        raise ValueError(UserNotFound)
    return user


def validate_password(hash_password: str, password: str) -> bool:
    if bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8")):
        return True
    return False


def structure_response_url(sso_payload: dict, grant_token: str, secret_key: str) -> str:
    redirect_url = sso_payload["redirect_to"]

    sso_payload["grant_token"] = grant_token
    buf = json.dumps(sso_payload)

    sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
    sso_w_secret = buf + secret_key
    sig = hashlib.sha512(sso_w_secret.encode("utf-8")).hexdigest()

    new_params = {
        "sso": sso,
        "sig": sig,
    }

    return merge_url_with_new_query_string(redirect_url, new_params)


def validate_client(sig: str, sso: str) -> (Client, dict):
    # Need to implement cache to reduce call into DB
    json_sso = base64.b64decode(sso).decode("utf-8")
    try:
        dict_sso = json.loads(json_sso)
    except ValueError:
        raise ValueError(InvalidPayload)

    try:
        client_key = dict_sso["client_key"]
    except KeyError:
        raise KeyError(MissingClientKey)

    try:
        client = Client.objects.active().filter(client_key=client_key).get()
    except Client.DoesNotExist:
        raise Client.DoesNotExist(ClientNotFound)

    sso_w_secret = json_sso + client.secret_key
    created_sig = hashlib.sha512(sso_w_secret.encode("utf-8")).hexdigest()
    if created_sig != sig:
        raise ValueError(SignatureNotValid)

    return client, dict_sso


def generate_grant_token_from_user_id(id: int, client: Client) -> Grant:
    try:
        user = User.objects.non_blocked_user().filter(pk=id).get()
    except User.DoesNotExist:
        raise ValueError(UserNotFound)

    return Grant.objects.create_grant(code=str(uuid4()), client=client, user=user)
