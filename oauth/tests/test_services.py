from django.test import TestCase
from common.constants import RESPONSE_TYPE_JWT
from common.utils import structure_response_url
from oauth.models import Client, Grant
from oauth.services import validate_client, generate_response
from oauth.tests.faker.fake import ClientModelData
from user.models import User
from user.tests.faker.fake import UserModelData


class TestGenerateResponse(TestCase):
    def setUp(self):
        self.client = Client.objects.create(**ClientModelData.active_client())
        self.user = User.objects.create(**UserModelData.non_blocked_user())
        self.decoded_sso = {
            "redirect_to": "http://localhost:9000/oauth/callback",
            "type": "grant",
        }

    def test_generate_response_not_valid_type(self):
        self.decoded_sso["type"] = "something"
        with self.assertRaises(ValueError):
            generate_response(self.client, self.decoded_sso, self.user)

    def test_generate_response_for_jwt(self):
        self.decoded_sso["type"] = RESPONSE_TYPE_JWT
        with self.assertRaises(NotImplementedError):
            generate_response(self.client, self.decoded_sso, self.user)

    def test_generate_response_for_grant(self):
        g_count = Grant.objects.count()
        self.assertEqual(0, g_count)

        res = generate_response(self.client, self.decoded_sso, self.user)

        grant = Grant.objects.all()
        self.assertEqual(1, grant.count())
        exp_url = structure_response_url(
            self.decoded_sso, grant[0].code, self.client.secret_key
        )

        self.assertEqual(exp_url, res)
