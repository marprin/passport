from passport.login.models import OauthClient, OauthGrant, OauthAccessToken, User
from passport.common.helper import get_today_date, add_minutes_from_now, random_string, add_days_from_today
from django.conf import settings

def find_oauth_client(redirect_url = None):
    redirect_url = redirect_url if redirect_url is not None else settings.WEBSITE_URL

    try:
        return OauthClient.objects.get(is_enabled='Y', callback_url=redirect_url)
    except Exception as e:
        return None

def create_oauth_grant(grant_code, client = None, user = None, ip_address = None):
    try:
        return OauthGrant.objects.create(
                grant_code = str(grant_code),
                client = client,
                user = user,
                ip_address = str(ip_address),
                created_at = get_today_date(),
                expired_at = add_minutes_from_now(settings.GRANT_MINUTES)
            )
    except Exception as e:
        return None

def create_oauth_access_token(user, client):
    try:
        return OauthAccessToken.objects.create(
                access_token = random_string(),
                user = user,
                client = client,
                refresh_token = random_string(),
                expired_at = add_days_from_today(20),
                created_at = get_today_date(),
                updated_at = get_today_date()
            )
    except Exception as e:
        return None