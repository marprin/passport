from django.test import TestCase
from django.test.client import RequestFactory
from common.utils import merge_url_with_new_query_string, get_client_ip


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
