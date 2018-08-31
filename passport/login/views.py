from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from common.helper import random_string, get_client_ip, check_password, \
        convert_url, get_today_date, add_minutes_from_now
from users.models import User
from oauth.models import Grant, Client

# Create your views here.
def index(request):
    email = request.POST.get('email') or ''
    password = request.POST.get('password') or ''
    redirect_url = request.POST.get('redirect_url') or request.GET.get('redirect_url') or None
    context = {
        'email': email,
        'redirect_url': redirect_url,
    }

    if request.method == 'POST':
        if email is None:
            context['email_error'] = 'Harap memasukkan email'
            return render(request, 'index.html', context)
        elif password is None:
            context['password_error'] = 'Harap memasukkan password'
            return render(request, 'index.html', context)
        else:
            try:
                attemp_user = User.objects.get(email=email, confirmed_account = 'Y')
            except User.DoesNotExist as e:
                attemp_user = None

            if attemp_user is not None:
                if check_password(str(password), str(attemp_user.password)):
                    redirect_url = redirect_url if redirect_url is not None else settings.WEBSITE_URL
                    try:
                        oauth_client = Client.objects.get(is_enabled='Y', callback_url=redirect_url)
                    except Client.DoesNotExist as e:
                        oauth_client = Client.objects.get(is_enabled='Y', callback_url=settings.WEBSITE_URL)
                    grant_code = str(random_string())

                    Grant.objects.create(
                        grant_code = str(grant_code),
                        client = oauth_client,
                        user = attemp_user,
                        ip_address = str(get_client_ip(request)),
                        created_at = get_today_date(),
                        expired_at = add_minutes_from_now(settings.GRANT_MINUTES)
                    )
                    return HttpResponseRedirect(convert_url(oauth_client.callback_url, grant_code))
                else:
                    context['error'] = 'Please check your email or password'
            else:
                context['error'] = 'Please check your email and password'

            return render(request, 'login/index.html', context)
    else:
        return render(request, 'login/index.html', context)