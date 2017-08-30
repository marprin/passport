from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from passport.common.helper import random_string, get_client_ip, check_password, convert_url
from passport.logic import OauthLogic, UserLogic

# Create your views here.
def index(request):
    email = request.POST.get('email') or ''
    password = request.POST.get('password') or ''
    redirect_url = request.POST.get('redirect_url') or request.GET.get('redirect_url') or None
    context = {
        'email': email,
        'redirect_url': redirect_url,
    }

    if (request.method == 'POST'):
        if (email is None):
            context['email_error'] = 'Harap memasukkan email'
            return render(request, 'index.html', context)
        elif (password is None):
            context['password_error'] = 'Harap memasukkan password'
            return render(request, 'index.html', context)
        else:
            attemp_user = UserLogic.find_user_by_email(email)

            if attemp_user is not None:
                if check_password(str(password), str(attemp_user.password)):
                    oauth_client = OauthLogic.find_oauth_client(redirect_url)
                    grant_code = str(random_string())

                    # generate a grant_code and return back to the request site
                    if oauth_client is None:
                        oauth_client = OauthLogic.find_oauth_client(settings.WEBSITE_URL)

                    OauthLogic.create_oauth_grant(grant_code, oauth_client, attemp_user, get_client_ip(request))
                    return HttpResponseRedirect(convert_url(oauth_client.callback_url, grant_code))
                else:
                    context['error'] = 'Please check your email or password'
            else:
                context['error'] = 'Please check your email and password'

            return render(request, 'login/index.html', context)
    else:
        return render(request, 'login/index.html', context)