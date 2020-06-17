from urllib.parse import urlencode, urlparse, parse_qs
import base64
import bcrypt
import hashlib
import json


def get_clean_url(url: str) -> str:
    url_components = urlparse(url)
    return url_components._replace(query={}).geturl()


def merge_url_with_new_query_string(url: str, new_params: dict) -> str:
    url_components = urlparse(url)
    original_params = parse_qs(url_components.query)

    merged_params = {**original_params, **new_params}
    update_query = urlencode(merged_params, doseq=True)

    return url_components._replace(query=update_query).geturl()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


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
