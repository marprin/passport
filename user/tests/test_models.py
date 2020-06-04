from django.test import TestCase
from user.models import User, LoginEvent, Device
from user.tests.faker.fake import UserModelData
from oauth.models import Client
from oauth.tests.faker.fake import ClientModelData
from uuid import uuid4


class TestModel(TestCase):
    def setUp(self):
        self.active_usr = User.objects.create(**UserModelData.active_user())
        self.confirmed_usr = User.objects.create(**UserModelData.confirmed_account())
        self.reach_max_lgn_attmpt_usr = User.objects.create(
            **UserModelData.reach_max_login_attempt()
        )
        self.non_blck_usr = User.objects.create(**UserModelData.non_blocked_user())

    def test_active_usr(self):
        usr = User.objects.active().filter(email=self.active_usr.email).get()
        self.assertEqual(self.active_usr, usr)

        self.active_usr.revoked = True
        self.active_usr.save()

        with self.assertRaises(User.DoesNotExist):
            User.objects.active().filter(email=self.active_usr.email).get()

    def test_login_attempt(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.not_reach_max_attempt().filter(
                email=self.reach_max_lgn_attmpt_usr.email
            ).get()

        self.reach_max_lgn_attmpt_usr.failed_login_attempt = 0
        self.reach_max_lgn_attmpt_usr.save()

        usr = (
            User.objects.not_reach_max_attempt()
            .filter(email=self.reach_max_lgn_attmpt_usr.email)
            .get()
        )

        self.assertEqual(self.reach_max_lgn_attmpt_usr, usr)

    def test_confirmed(self):
        usr = User.objects.confirmed().filter(email=self.confirmed_usr.email).get()

        self.assertEqual(self.confirmed_usr, usr)

        self.confirmed_usr.confirmed_account = False
        self.confirmed_usr.save()

        with self.assertRaises(User.DoesNotExist):
            User.objects.confirmed().filter(email=self.confirmed_usr.email).get()

    def test_non_blocked_user(self):
        usr = (
            User.objects.non_blocked_user().filter(email=self.non_blck_usr.email).get()
        )

        self.assertEqual(self.non_blck_usr, usr)

        self.non_blck_usr.revoked = True
        self.non_blck_usr.save()

        with self.assertRaises(User.DoesNotExist):
            User.objects.non_blocked_user().filter(email=self.non_blck_usr.email).get()

    def test_user__str__(self):
        usr = User.objects.active().filter(email=self.active_usr.email).get()

        self.assertEqual(self.active_usr.name, str(usr))


class TestLoginEvent(TestCase):
    def setUp(self):
        self.email = "eam@gmail.com"
        client = Client.objects.create(**ClientModelData.active_client())
        self.lgn_evnt = LoginEvent.objects.create(email=self.email, client=client)

    def test_login_event_str(self):
        self.assertEqual(self.email, str(self.lgn_evnt))


class TestDevice(TestCase):
    def setUp(self):
        client = Client.objects.create(**ClientModelData.active_client())
        self.usr = User.objects.create(**UserModelData.active_user())

        self.dvc = Device.objects.create(
            user=self.usr, client=client, identifier=str(uuid4())
        )

    def test_device_str(self):
        self.assertEqual(self.usr.name, str(self.dvc))
