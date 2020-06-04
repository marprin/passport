from django.test import TestCase
from django.test.client import RequestFactory
from common.utils import (
    merge_url_with_new_query_string,
    get_client_ip,
    validate_password,
    structure_response_url,
)
from urllib.parse import urlencode
import bcrypt
import json
import hashlib
import base64


class TestUtilsMergeUrlWithNewQueryString(TestCase):
    def setUp(self):
        self.new_params: dict = {
            "sso": "somesso",
            "sig": "somesig",
        }

    def test_with_normal_url(self):
        url: str = "http://localhost:9000/oauth/callback"
        expected_url = url + "?sso=somesso&sig=somesig"

        res = merge_url_with_new_query_string(url, self.new_params)

        self.assertEqual(expected_url, res)

    def test_with_query_string_on_url(self):
        url: str = "http://localhost:9000/oauth/callback?type=success"
        expected_url = url + "&sso=somesso&sig=somesig"

        res = merge_url_with_new_query_string(url, self.new_params)

        self.assertEqual(expected_url, res)


class TestGetClientIP(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.expected_ip = "127.0.0.1"
        self.health_url = "/healthz"

    def test_get_client_ip(self):
        request = self.factory.get(self.health_url)

        ip = get_client_ip(request)
        self.assertEqual(self.expected_ip, ip)

    def test_get_client_ip_from_x_forwarded_for(self):
        request = self.factory.get(self.health_url)
        request.META["HTTP_X_FORWARDED_FOR"] = "localhost,127.0.0.1"

        ip = get_client_ip(request)
        self.assertEqual(self.expected_ip, ip)


class TestValidatePassword(TestCase):
    def setUp(self):
        self.plain_pwd = "password"
        self.hash_pwd = bcrypt.hashpw(
            self.plain_pwd.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def test_match_password(self):
        is_vld_pwd = validate_password(self.hash_pwd, self.plain_pwd)
        self.assertTrue(is_vld_pwd)

    def test_not_match_password(self):
        is_vld_pwd = validate_password(self.hash_pwd, "somenewpass")
        self.assertFalse(is_vld_pwd)


class TestStructureResponseUrl(TestCase):
    def setUp(self):
        self.secret_key = "secret_things123"
        self.grant_token = "grant-code-123"

    def test_structure_normal_url(self):
        sso_payload = {
            "redirect_to": "http://localhost:9000/oauth/callback",
            "grant_token": self.grant_token,
        }
        buf = json.dumps(sso_payload)
        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        sig = hashlib.sha512((buf + self.secret_key).encode("utf-8")).hexdigest()
        params = {
            "sso": sso,
            "sig": sig,
        }
        expected_url = f"http://localhost:9000/oauth/callback?{urlencode(params)}"

        redirect_to = structure_response_url(
            sso_payload, self.grant_token, self.secret_key
        )

        self.assertEqual(redirect_to, expected_url)

    def test_structure_have_query_params_url(self):
        sso_payload_query = {
            "redirect_to": "http://localhost:9000/oauth/callback?type=success",
            "grant_token": self.grant_token,
        }

        buf = json.dumps(sso_payload_query)
        sso = base64.b64encode(buf.encode("utf-8")).decode("utf-8")
        sig = hashlib.sha512((buf + self.secret_key).encode("utf-8")).hexdigest()
        params = {
            "type": "success",
            "sso": sso,
            "sig": sig,
        }
        expected_url = f"http://localhost:9000/oauth/callback?{urlencode(params)}"

        redirect_to = structure_response_url(
            sso_payload_query, self.grant_token, self.secret_key
        )

        self.assertEqual(redirect_to, expected_url)
