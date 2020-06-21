from django.test import TestCase
from django.utils import timezone
from common.constants import RESPONSE_TYPE_JWT
from common.utils import structure_response_url
from oauth.models import Client, Grant
from oauth.services import validate_client, generate_response
from oauth.tests.faker.fake import ClientModelData
from user.models import User
from user.tests.faker.fake import UserModelData
import base64
import hashlib
import hmac
import json


class TestValidateClient(TestCase):
    def setUp(self):
        self._client = Client.objects.create(**ClientModelData.active_client())

    def test_invalid_json_payload(self):
        sig = "fake_sig"
        sso = base64.b64encode(b"fake").decode("utf-8")

        with self.assertRaises(ValueError):
            validate_client(sig, sso)

    def test_missing_client_key(self):
        sig = "fake_sig"
        buf = json.dumps(
            {"nonce": int(timezone.now().timestamp())}, separators=(",", ":")
        )
        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")

        with self.assertRaises(KeyError):
            validate_client(sig, sso)

    def test_missing_redirect_to(self):
        sig = "fake_sig"
        buf = json.dumps(
            {
                "nonce": int(timezone.now().timestamp()),
                "client_key": "fake-client-key",
            },
            separators=(",", ":"),
        )

        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        with self.assertRaises(KeyError):
            validate_client(sig, sso)

    def test_invalid_client_key(self):
        sig = "fake_sig"
        buf = json.dumps(
            {
                "nonce": int(timezone.now().timestamp()),
                "client_key": "fake-client-key",
                "redirect_to": "fake-redirect_key",
            },
            separators=(",", ":"),
        )

        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        with self.assertRaises(Client.DoesNotExist):
            validate_client(sig, sso)

        buf = json.dumps(
            {
                "nonce": int(timezone.now().timestamp()),
                "client_key": self._client.client_key,
                "redirect_to": "fake-redirect_key",
            },
            separators=(",", ":"),
        )

        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        with self.assertRaises(Client.DoesNotExist):
            validate_client(sig, sso)

    def test_signature_is_invalid(self):
        sig = "fake_sig"
        buf = json.dumps(
            {
                "nonce": int(timezone.now().timestamp()),
                "client_key": self._client.client_key,
                "redirect_to": self._client.callback_url,
            },
            separators=(",", ":"),
        )

        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        with self.assertRaises(ValueError):
            validate_client(sig, sso)

    def test_with_valid_params(self):
        dict_sso = {
            "nonce": int(timezone.now().timestamp()),
            "client_key": self._client.client_key,
            "redirect_to": self._client.callback_url,
        }
        buf = json.dumps(dict_sso, separators=(",", ":"),)

        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        sig = hmac.new(
            self._client.secret_key.encode("utf-8"), buf.encode("utf-8"), hashlib.sha512
        ).hexdigest()

        client, resp_dict_sso = validate_client(sig, sso)
        self.assertEqual(resp_dict_sso, dict_sso)
        self.assertEqual(client, self._client)


class TestGenerateResponse(TestCase):
    def setUp(self):
        self.client = Client.objects.create(**ClientModelData.active_client())
        self.user = User.objects.create(**UserModelData.non_blocked_user())
        self.decoded_sso = {
            "redirect_to": "http://localhost:9000/oauth/callback",
            "token_type": "grant",
        }

    def test_generate_response_not_valid_type(self):
        self.decoded_sso["token_type"] = "something"
        with self.assertRaises(ValueError):
            generate_response(self.client, self.decoded_sso, self.user)

    def test_generate_response_for_jwt(self):
        self.decoded_sso["token_type"] = RESPONSE_TYPE_JWT
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
