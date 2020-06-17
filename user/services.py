from common.constants import UserNotFound
from common.utils import get_client_ip, validate_password
from oauth.models import Client
from user.models import LoginEvent, User


def create_login_event(request, email: str, client: Client, action: str):
    LoginEvent.objects.create(
        email=email,
        client=client,
        ip_address=get_client_ip(request),
        platform=request.user_agent.os.family,
        platform_version=request.user_agent.os.version_string,
        browser=request.user_agent.browser.family,
        browser_version=request.user_agent.browser.version_string,
        device=request.user_agent.device.brand,
        device_version=request.user_agent.device.model,
        action=action,
    )


def check_user(email: str, password: str):
    try:
        user = User.objects.non_blocked_user().filter(email=email).get()
    except User.DoesNotExist:
        raise User.DoesNotExist(UserNotFound)

    is_pwd_valid = validate_password(user.password, password)
    if is_pwd_valid is False:
        raise ValueError(UserNotFound)
    return user
