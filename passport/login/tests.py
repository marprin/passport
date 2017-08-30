from django.test import Client
import unittest
from .models import User, OauthClient
from passport.common.helper import encrypt_password, get_today_date

# Create your tests here.

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_load_login_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_no_user(self):
        response = self.client.post('/', {'email': 'tes@gmail.com', 'password': 12345})
        self.assertEqual(response.status_code, 200)

    def test_success_login(self):
        self.user = User.objects.create(
            name='tes',
            email='admin@gmail.com',
            password=encrypt_password(123456),
            confirmed_account='Y',
            created_at=get_today_date(),
            updated_at=get_today_date()
        )

        self.oauth_client = OauthClient.objects.create(
            client_name = 'tes',
            client_public_key = 'aaa',
            client_secret_key = 'bbb',
            callback_url = 'http://aa.dev',
            is_enabled='Y',
            created_at = get_today_date(),
            updated_at = get_today_date()
        )
        response = self.client.post('/?redirect_url=http://aa.dev', {'email': self.user.email, 'password': 123456})
        self.assertEqual(response.status_code, 302)