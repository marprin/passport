from login.models import User

def find_user_by_email(email):
    try:
        return User.objects.get(email=email, confirmed_account = 'Y')
    except Exception as e:
        return None