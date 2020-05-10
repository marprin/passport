from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from .forms import LoginForm
import json
import logging


logger = logging.getLogger(__name__)


class OauthLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {"errors": {"general_errors": []}}

        flash_messages = get_messages(request)
        for message in flash_messages:
            try:
                err = json.loads(message)
            except (ValueError, TypeError) as e:
                context["errors"]["general_errors"] = "Please try again in a moment"
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


class VerificationView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "oauth/verify.html", context=context)

    def post(self, request, *args, **kwargs):
        pass
