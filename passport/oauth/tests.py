# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import Client
import unittest
from passport.login.models import User, OauthClient, OauthGrant
from passport.common.helper import get_today_date

# Create your tests here.
class OauthTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_validation_error(self):
        response = self.client.post('/api/v1/oauth/')
        self.assertEqual(response.status_code, 422)

    def test_oauth_client_not_found(self):
        response = self.client.post('/api/v1/oauth/', {
            'client_key': 'sa',
            'secret_key': 'sab',
            'grant_code': 'bb'
        })

        body_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body_response['error'], 'UNKNOWN_CLIENT')
        self.assertEqual(body_response['status'], 400)
        self.assertEqual(body_response['success'], False)

    def test_invalid_grant_code(self):
        self.oauth_client = OauthClient.objects.create(
            client_name= 'test',
            client_public_key = 'sa',
            client_secret_key = 'sa',
            callback_url = 'http://test.dev',
            is_enabled = 'Y',
            created_at = get_today_date(),
            updated_at = get_today_date()
        )

        response = self.client.post('/api/v1/oauth/', {
            'client_key': 'sa',
            'secret_key': 'sa',
            'grant_code': 'bb'
        })

        body_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body_response['error'], 'INVALID_GRANT')
        self.assertEqual(body_response['status'], 400)
        self.assertEqual(body_response['success'], False)

    def test_success_validate_oauth_and_get_access_token(self):
        self.oauth_client = OauthClient.objects.create(
            client_name='test',
            client_public_key='saa',
            client_secret_key='saa',
            callback_url='http://test2.dev',
            is_enabled='Y',
            created_at=get_today_date(),
            updated_at=get_today_date()
        )

        self.user = User.objects.create(
            name = 'test',
            email = 'testing@gmail.com',
            created_at = get_today_date(),
            updated_at = get_today_date()
        )

        self.oauth_grant = OauthGrant.objects.create(
            grant_code = 'bb',
            client = self.oauth_client,
            user = self.user,
            ip_address='127.0.0.1',
            created_at = get_today_date(),
        )

        response = self.client.post('/api/v1/oauth/', {
            'client_key': 'saa',
            'secret_key': 'saa',
            'grant_code': 'bb'
        })

        body_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body_response['status'], 200)
        self.assertEqual(body_response['success'], True)
        self.assertEqual(body_response['data']['type'], 'bearer')