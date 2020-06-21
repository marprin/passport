from django.test import TestCase, Client
from django.shortcuts import reverse
from version import version


class TestHealthz(TestCase):
    def setUp(self):
        self.client = Client()
        self.healthz_url = reverse("healthz")
        self.expected_response = {
            "version": version,
            "message": "ok",
        }

    def test_get_healthz(self):
        req = self.client.get(self.healthz_url)

        self.assertEqual(200, req.status_code)
        self.assertDictEqual(self.expected_response, req.json())
