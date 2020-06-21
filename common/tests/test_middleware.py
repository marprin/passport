from django.test import TestCase
from django.shortcuts import reverse
from django.core import signing
from django.core.signing import BadSignature
from django.utils import timezone
from common.constants import RESPONSE_TYPE_GRANT
from oauth.models import Client, Grant
from oauth.services import generate_response
from oauth.tests.faker.fake import ClientModelData
from user.models import User
from user.tests.faker.fake import UserModelData
import base64
import hashlib
import hmac
import json


class BaseTestData(TestCase):
    def setUp(self):
        super().setUp()
        self._client = Client.objects.create(**ClientModelData.active_client())
        self._user = User.objects.create(**UserModelData.non_blocked_user())
        self._blocked_user = User.objects.create(**UserModelData.confirmed_account())

        sso = {
            "client_key": self._client.client_key,
            "redirect_to": self._client.callback_url,
            "token_type": RESPONSE_TYPE_GRANT,
            "nonce": int(timezone.now().timestamp()),
        }

        json_sso = json.dumps(sso, separators=(",", ":"))
        encoded_sso = base64.b64encode(json_sso.encode("utf-8"))
        sig = hmac.new(
            self._client.secret_key.encode("utf-8"),
            json_sso.encode("utf-8"),
            hashlib.sha512,
        )
        self._dict_sso = sso
        self._sso = encoded_sso.decode("utf-8")
        self._sig = sig.hexdigest()


class TestOauthSignatureMiddleware(BaseTestData):
    def setUp(self):
        super().setUp()
        self._url = reverse("oauth:index")

    def test_user_id_not_exist_in_session(self):
        req = self.client.get(self._url)
        self.assertEqual(req.status_code, 200)

    def test_user_but_invalid_session(self):
        session = self.client.session
        session["user_id"] = "fake-user-id"
        session.save()

        req = self.client.get(self._url)
        self.assertEqual(req.status_code, 200)

    def test_session_found_but_no_user_found(self):
        session = self.client.session
        session["user_id"] = signing.dumps(self._blocked_user.id)
        session.save()

        req = self.client.get(self._url)
        self.assertEqual(req.status_code, 200)

    def test_user_found_but_no_sig_or_sso_found(self):
        session = self.client.session
        session["user_id"] = signing.dumps(self._user.id)
        session.save()

        req = self.client.get(self._url)
        self.assertEqual(req.status_code, 200)

    def test_user_found_but_sig_or_sso_invalid(self):
        session = self.client.session
        session["user_id"] = signing.dumps(self._user.id)
        session.save()

        req = self.client.get(self._url + "?sso=fake-sso&sig=fake-sig")
        self.assertEqual(req.status_code, 200)

    def test_user_found_sso_and_sig_valid(self):
        session = self.client.session
        session["user_id"] = signing.dumps(self._user.id)
        session.save()

        self.assertEqual(Grant.objects.count(), 0)

        req = self.client.get(self._url + f"?sso={self._sso}&sig={self._sig}")
        self.assertEqual(req.status_code, 302)
        self.assertIsNotNone(req.url)

        self.assertEqual(Grant.objects.count(), 1)
