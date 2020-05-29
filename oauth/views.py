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
    EmailorPasswordNotValid,
    ClientNotFound,
)
from common.utils import get_client_ip
from oauth.forms import LoginForm
from oauth.models import AccessToken, Verification, Grant
from oauth.services import (
    structure_response_url,
    check_user,
    get_active_client,
)
from user.models import LoginEvent
from uuid import uuid4
import json
import logging
import sys


logger = logging.getLogger(__name__)


class OauthLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {"errors": {"general_errors": [], "email": None, "password": None,}}

        flash_messages = get_messages(request)
        for message in flash_messages:
            context["errors"][message.extra_tags] = message

        return render(request, "oauth/index.html", context=context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            j_err = json.loads(form.errors.as_json())
            for k, v in j_err.items():
                messages.error(request, v[0]["message"], extra_tags=k)
            return HttpResponseRedirect(reverse("oauth:index"))

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        decoded_sso = request.session["decoded_sso"]

        try:
            client = get_active_client(decoded_sso["client_key"])
        except Client.DoesNotExist as e:
            logger.error(f"Client not found: {str(e)}")
            messages.error(request, [ClientNotFound], extra_tags="general_errors")
            return HttpResponseRedirect(reverse("oauth:index"))

        try:
            user = check_user(email, password)
        except Exception as e:
            logger.error(f"Error user not found: {str(e)}")
            LoginEvent.objects.create(
                email=email,
                client=client,
                ip_address=get_client_ip(request),
                action=f"{str(e)}",
            )
            messages.error(request, EmailorPasswordNotValid, extra_tags="email")
            return HttpResponseRedirect(reverse("oauth:index"))

        if user.otp_email_enabled:
            # Handle the OTP request and redirect to verify page
            return HttpResponseRedirect(reverse("oauth:verify"))

        # Create the grant
        grant = Grant.objects.create(code=str(uuid4()), client=client, user=user,)
        redirect_url = structure_response_url(
            decoded_sso, grant.code, client.secret_key
        )
        request.session["decoded_sso"] = None
        return HttpResponseRedirect(redirect_url)


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
