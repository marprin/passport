from oauth.models import Client
from user.models import User
from common.constants import GeneralError, SignatureOrSSONotPresent, ClientNotFound
from django.conf import settings
from importlib import import_module
from oauth.services import (
    validate_client,
    generate_response,
)
from django.core import signing
from django.http import (
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import reverse
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)


class OauthSignatureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._process_path = (
            reverse("oauth:index"),
            reverse("oauth:verify"),
        )

    def __call__(self, request):
        if request.path in self._process_path:
            sig = request.GET.get("sig") or None
            sso = request.GET.get("sso") or None
            if sig is None or sso is None:
                decoded_sso = request.session.get("decoded_sso", None)
                if decoded_sso is None:
                    return HttpResponseBadRequest(SignatureOrSSONotPresent)
                else:
                    try:
                        client = (
                            Client.objects.active()
                            .filter(client_key=decoded_sso["client_key"])
                            .get()
                        )
                    except Client.DoesNotExist as e:
                        logger.error(f"Error on get client: {str(e)}")
                        return HttpResponseNotFound(ClientNotFound)
            else:
                sig = unquote(sig)
                sso = unquote(sso)

                try:
                    client, decoded_sso = validate_client(sig, sso)
                except Exception as e:
                    return HttpResponseBadRequest(str(e))

            # If the session for user_id is set, no need to login anymore
            dec_user_id = request.session.get("user_id", None)
            if dec_user_id is not None:
                user_id = signing.loads(dec_user_id)

                try:
                    user = User.objects.non_blocked_user().filter(pk=user_id).get()
                except User.DoesNotExist as e:
                    logger.error(f"Error on get user {str(e)}")
                    request.session["user_id"] = None
                    return HttpResponseRedirect(reverse("oauth:index"))

                try:
                    redirect_to = generate_response(client, decoded_sso, user)
                    request.session["decoded_sso"] = None
                    return HttpResponseRedirect(redirect_to)
                except (ValueError, NotImplementedError) as e:
                    logger.error(f"Error in middleware to generate response: {str(e)}")
                    return HttpResponseBadRequest(e)
                except Exception as e:
                    logger.error(
                        f"Error while session for user_id still exists: {str(e)}"
                    )
                    return HttpResponseServerError(GeneralError)

            # Put the decoded_sso in session
            request.session["decoded_sso"] = decoded_sso

        # Handle the request in view
        response = self.get_response(request)
        return response
