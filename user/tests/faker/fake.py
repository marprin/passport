from faker import Faker
from faker.providers import BaseProvider
from django.conf import settings
import bcrypt


fake = Faker()


class UserModelData(BaseProvider):
    @staticmethod
    def active_user():
        return dict(
            name=fake.name(),
            email=fake.email(),
            password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
            confirmed_account=False,
            revoked=False,
            otp_email_enabled=False,
            failed_login_attempt=0,
        )

    @staticmethod
    def confirmed_account():
        return dict(
            name=fake.name(),
            email=fake.email(),
            password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
            confirmed_account=True,
            revoked=True,
            otp_email_enabled=False,
            failed_login_attempt=0,
        )

    @staticmethod
    def reach_max_login_attempt():
        return dict(
            name=fake.name(),
            email=fake.email(),
            password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
            confirmed_account=False,
            revoked=False,
            otp_email_enabled=False,
            failed_login_attempt=settings.MAX_FAILED_LOGIN_ATTEMPT + 1,
        )

    @staticmethod
    def non_blocked_user():
        return dict(
            name=fake.name(),
            email=fake.email(),
            password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
            confirmed_account=True,
            revoked=False,
            otp_email_enabled=False,
            failed_login_attempt=0,
        )
