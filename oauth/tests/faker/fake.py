from faker import Faker
from faker.providers import BaseProvider
from uuid import uuid4

fake = Faker()


class ClientModelData(BaseProvider):
    @staticmethod
    def active_client():
        return dict(
            name=fake.name(),
            client_key=str(uuid4()),
            secret_key=str(uuid4()),
            revoked=False,
        )
