from django.http import JsonResponse
from version import version


def healthz(request):
    context = {"version": version, "message": "ok"}
    return JsonResponse(context)
