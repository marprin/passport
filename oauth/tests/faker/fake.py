from django.utils import timezone
from datetime import timedelta
from faker import Faker
from faker.providers import BaseProvider
from oauth.models import Client
from user.models import User
from user.tests.faker.fake import UserModelData
from uuid import uuid4

fake = Faker()


class ClientModelData(BaseProvider):
    @staticmethod
    def active_client():
        return dict(
            name=fake.name(),
            client_key=str(uuid4()),
            secret_key=str(uuid4()),
            callback_url=fake.url(),
            revoked=False,
        )


class IPAddressModelData(BaseProvider):
    @staticmethod
    def active_ip_address():
        return dict(
            client=Client.objects.create(**ClientModelData.active_client()),
            ip_address=fake.ipv4(),
            revoked=False,
        )

    @staticmethod
    def revoked_ip_address():
        return dict(
            client=Client.objects.create(**ClientModelData.active_client()),
            ip_address=fake.ipv4(),
            revoked=True,
        )


class GrantModelData(BaseProvider):
    @staticmethod
    def revoked_grant():
        return dict(
            code=str(uuid4()),
            client=Client.objects.create(**ClientModelData.active_client()),
            user=User.objects.create(**UserModelData.non_blocked_user()),
            revoked=True,
        )

    @staticmethod
    def active_grant():
        return dict(
            code=str(uuid4()),
            client=Client.objects.create(**ClientModelData.active_client()),
            user=User.objects.create(**UserModelData.non_blocked_user()),
            revoked=False,
        )

    @staticmethod
    def expired_token():
        return dict(
            code=str(uuid4()),
            client=Client.objects.create(**ClientModelData.active_client()),
            user=User.objects.create(**UserModelData.non_blocked_user()),
            revoked=False,
            expired_at=(timezone.now() - timedelta(minutes=10)),
        )
