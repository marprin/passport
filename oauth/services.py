from oauth.models import Grant, Client
from common.constants import (
    InvalidPayload,
    MissingClientKey,
    ClientNotFound,
    SignatureNotValid,
    RESPONSE_TYPE_GRANT,
    RESPONSE_TYPE_JWT,
    InvalidTypeResponse,
)
from user.models import User, LoginEvent
from common.utils import structure_response_url
from django.core.cache import cache
from uuid import uuid4
import base64
import json
import hashlib


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


def generate_response(client: Client, decoded_sso: dict, user: User) -> str:
    response_type = decoded_sso.get("type", "grant")
    if response_type == RESPONSE_TYPE_GRANT:
        grant = Grant.objects.create_grant(code=str(uuid4()), client=client, user=user)
        return structure_response_url(decoded_sso, grant.code, client.secret_key)
    elif response_type == RESPONSE_TYPE_JWT:
        # Need to handle the JWT response
        raise NotImplementedError(InvalidTypeResponse)
    else:
        raise ValueError(InvalidTypeResponse)
