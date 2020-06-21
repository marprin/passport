from django.core import signing
from django.core.signing import BadSignature
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from common.constants import SignatureOrSSONotPresent, UserSessionNotFound
from oauth.services import validate_client, generate_response
from oauth.models import Client
from user.models import User

import logging

logger = logging.getLogger(__name__)


class OauthSignatureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._process_path = (reverse("oauth:index"),)

    def __call__(self, request):
        if request.path in self._process_path:
            try:
                enc_user_id = request.session.get("user_id", None)
                if enc_user_id is None:
                    raise User.DoesNotExist(UserSessionNotFound)

                user = self._check_session(enc_user_id)

                sig = request.GET.get("sig") or None
                sso = request.GET.get("sso") or None
                if sig is None or sso is None:
                    raise ValueError(SignatureOrSSONotPresent)

                client, decoded_sso = validate_client(sig, sso)

                redirect_to = generate_response(client, decoded_sso, user)
                return HttpResponseRedirect(redirect_to)
            except (User.DoesNotExist, BadSignature) as e:
                request.session["user_id"] = None
                logger.info(f"In Middleware: {str(e)}")
            except (
                ValueError,
                KeyError,
                Client.DoesNotExist,
                NotImplementedError,
            ) as e:
                logger.error(f"In Middleware: {str(e)}")

        # Handle the request in view
        response = self.get_response(request)
        return response

    def _check_session(self, enc_user_id: str) -> User:
        user_id = signing.loads(enc_user_id)

        try:
            user = User.objects.non_blocked_user().filter(pk=user_id).get()
        except User.DoesNotExist as e:
            raise User.DoesNotExist(f"User with id: {user_id} is not found")
        return user
