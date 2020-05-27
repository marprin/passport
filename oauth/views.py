from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.views.generic import View
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from common.constants import (
    GeneralError,
    RedirectionNotPresent,
)
from oauth.forms import LoginForm
from oauth.models import AccessToken, Verification
from oauth.services import (
    structure_response_url,
    check_user,
)
import json
import logging
import sys


logger = logging.getLogger(__name__)


class OauthLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {"errors": {"general_errors": []}}

        flash_messages = get_messages(request)
        for message in flash_messages:
            try:
                err = json.loads(message)
            except (ValueError, TypeError) as e:
                context["errors"]["general_errors"].append(GeneralError)
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
            messages.error(request, err_str)
            return HttpResponseRedirect(reverse("oauth:index"))

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        sig = request.session["sig"]
        sso = request.session["sso"]

        try:
            user = check_user(email, password)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            HttpResponseRedirect(reverse("oauth:index"))

        return HttpResponseRedirect(reverse("oauth:verify"))


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
        # Add handler to return 400 when user refresh the page, can see sample from ss of instagram OTP
        reference = kwargs["reference"]

        context = {"data": {"reference": reference}}
        return render(request, "oauth/verify.html", context=context)

    def post(self, request, *args, **kwargs):
        pass


class ReOTP(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
