from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.views.generic import View
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from common.constants import (
    SignatureOrSSONotPresent,
    GeneralError,
    RedirectionNotPresent,
)
from .forms import LoginForm
from .models import AccessToken
from .services import (
    validate_client,
    generate_grant_token_from_access_token,
    structure_response_url,
)
from urllib.parse import unquote
import json
import logging
import base64


logger = logging.getLogger(__name__)


class OauthLoginView(View):
    def get(self, request, *args, **kwargs):
        sig = request.GET.get("sig") or request.session.get("sig") or None
        sso = request.GET.get("sso") or request.session.get("sso") or None

        if sig is None or sso is None:
            referer = request.META.get("HTTP_REFERER", None)
            if referer is None:
                return HttpResponseNotFound(SignatureOrSSONotPresent)
            return HttpResponseRedirect(referer)

        sig = unquote(sig)
        sso = unquote(sso)

        try:
            client, decoded_sso = validate_client(sig, sso)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        # If the session is set, no need to login anymore
        access_token = request.session.get("access_token", None)
        if access_token is not None:
            # We have the data so only need to return the grant token
            try:
                grant = generate_grant_token_from_access_token(access_token, client)
                redirect_to = structure_response_url(
                    decoded_sso, grant.code, client.secret_key
                )
                return HttpResponseRedirect(redirect_to)
            except ValueError as e:
                logger.error(f"Error on check access token: {str(e)}")
                request.session["access_token"] = None
            except Exception as e:
                logger.error(
                    f"Error while session for access token still exists: {str(e)}"
                )
                return HttpResponseServerError(GeneralError)

        # Put the sig and sso in session
        request.session["sig"] = sig
        request.session["sso"] = sso

        context = {"errors": {"general_errors": []}}

        flash_messages = get_messages(request)
        for message in flash_messages:
            try:
                err = json.loads(message)
            except (ValueError, TypeError) as e:
                context["errors"]["general_errors"] = GeneralError
                logger.error(
                    f"Error in parsing payload of error message login: {str(e)}"
                )
                continue

            context["errors"]["email"] = err["email"][0]["message"]
            context["errors"]["password"] = err["password"][0]["message"]

        return render(request, "oauth/index.html", context=context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            err_str = form.errors.as_json()
            err = json.loads(err_str)
            messages.error(request, err_str)
            return HttpResponseRedirect(reverse("oauth:index"))

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        print(email, password)

        return HttpResponse("Success")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        redirect_url = request.GET.get("redirect_to", None)
        if redirect_url is None:
            return HttpResponseBadRequest(RedirectionNotPresent)

        acc_token = request.session["access_token"]
        # Need to revoke the token
        AccessToken.find_by_access_token(acc_token).update(revoked=True)

        # Remove session token
        try:
            del request.session["access_token"]
        except KeyError:
            pass

        return HttpResponseRedirect(redirect_url)


class VerificationView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "oauth/verify.html", context=context)

    def post(self, request, *args, **kwargs):
        pass
