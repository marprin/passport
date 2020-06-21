from django.test import TestCase
from oauth.models import Client, IPAddress, Grant, AccessToken, Verification
from oauth.tests.faker.fake import ClientModelData, IPAddressModelData, GrantModelData


class TestClient(TestCase):
    def setUp(self):
        self._client = Client.objects.create(**ClientModelData.active_client())

    def test_client__str__(self):
        self.assertEqual(str(self._client), self._client.name)


class TestIPAddress(TestCase):
    def setUp(self):
        self._ipaddress = IPAddress.objects.create(
            **IPAddressModelData.active_ip_address()
        )

    def test_ipaddress__str__(self):
        self.assertEqual(str(self._ipaddress), self._ipaddress.ip_address)

    def test_find_is_authorized_ipaddress(self):
        revoked_ip = IPAddress.objects.create(**IPAddressModelData.revoked_ip_address())

        ip = IPAddress.is_authorized_ipaddress(revoked_ip.ip_address)
        self.assertEqual(len(ip), 0)

        ip = IPAddress.is_authorized_ipaddress(self._ipaddress.ip_address)
        self.assertEqual(len(ip), 1)


class TestGrant(TestCase):
    def setUp(self):
        self._deactive_grant = Grant.objects.create_grant(
            **GrantModelData.revoked_grant()
        )
        self._active_grant = Grant.objects.create_grant(**GrantModelData.active_grant())
        self._expired_token = Grant.objects.create(**GrantModelData.expired_token())

    def test_grant__str__(self):
        self.assertEqual(str(self._deactive_grant), self._deactive_grant.code)
        self.assertEqual(str(self._active_grant), self._active_grant.code)

    def test_find_active_client(self):
        with self.assertRaises(Grant.DoesNotExist):
            Grant.objects.active().filter(code=self._deactive_grant.code).get()

        grant = Grant.objects.active().filter(code=self._active_grant.code).get()
        self.assertIsNotNone(grant)

    def test_find_not_expired_token(self):
        grant = Grant.objects.not_expired().filter(code=self._active_grant.code).get()
        self.assertIsNotNone(grant)

        with self.assertRaises(Grant.DoesNotExist):
            Grant.objects.not_expired().filter(code=self._expired_token.code).get()

    def test_find_valid_token(self):
        grant = Grant.objects.valid_token().filter(code=self._active_grant.code).get()
        self.assertIsNotNone(grant)

        with self.assertRaises(Grant.DoesNotExist):
            Grant.objects.valid_token().filter(code=self._expired_token.code).get()


class TestAccessToken(TestCase):
    def setUp(self):
        pass
