from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import json

# Create your views here.
class OauthLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oauth/index.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        return HttpResponse("Success")
