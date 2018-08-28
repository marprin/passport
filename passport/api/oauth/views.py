# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from login.models import OauthClient, OauthGrant, OauthAccessToken, User
from logic.OauthLogic import create_oauth_access_token

# Create your views here.

class Index(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request, format = None):
        data = request.data

        client_key = data.get('client_key')
        if client_key is None:
            return Response({'success': False, 'status': status.HTTP_422_UNPROCESSABLE_ENTITY, 'error': 'CLIENT_KEY_NOT_SUPPLIED'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        secret_key = data.get('secret_key')
        if secret_key is None:
            return Response({'success': False, 'status': status.HTTP_422_UNPROCESSABLE_ENTITY, 'error': 'SECRET_KEY_NOT_SUPPLIED'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        grant = data.get('grant_code')
        if grant is None:
            return Response({'success': False, 'status': status.HTTP_422_UNPROCESSABLE_ENTITY, 'error': 'GRANT_CODE_NOT_SUPPLIED'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            oauth_client = OauthClient.objects.get(is_enabled='Y', client_public_key=client_key, client_secret_key=secret_key)
        except Exception:
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'error': 'UNKNOWN_CLIENT'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            oauth_grant = OauthGrant.objects.get(revoked=False, grant_code=grant, client=oauth_client)
        except Exception as e:
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'error': 'INVALID_GRANT'}, status=status.HTTP_400_BAD_REQUEST)

        oauth_access_token = create_oauth_access_token(user = oauth_grant.user, client = oauth_client)
        oauth_grant.revoked = True
        oauth_grant.save()

        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'data': {
                'type': 'bearer',
                'access_token': oauth_access_token.access_token,
                'refresh_token': oauth_access_token.refresh_token
            }
        }, status=status.HTTP_200_OK)