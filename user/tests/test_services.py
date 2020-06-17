from django.test import TestCase
from django.test.client import RequestFactory
from common.constants import UserNotFound
from oauth.models import Client
from oauth.tests.faker.fake import ClientModelData
from user.models import LoginEvent, User
from user.services import create_login_event, check_user
from user.tests.faker.fake import UserModelData


class TestCreateLoginEvent(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client.objects.create(**ClientModelData.active_client())
        self.request = self.factory.get("/healthz")
        self.request.user_agent.os.family = "Ubuntu"
        self.request.user_agent.os.version_string = ""
        self.request.user_agent.browser.family = "Chrome"
        self.request.user_agent.browser.version_string = "8.10.1343"
        self.request.user_agent.device.brand = ""
        self.request.user_agent.device.model = ""

    # def test_create_login_history(self):
    #     login_count = LoginEvent.objects.count()
    #     self.assertEqual(0, login_count)

    #     create_login_event(self.request, "test@gmail.com", self.client, UserNotFound)

    #     login_count = LoginEvent.objects.count()
    #     self.assertEqual(1, login_count)


class TestCheckUser(TestCase):
    def setUp(self):
        self.vld_user = User.objects.create(**UserModelData.non_blocked_user())
        self.non_vld_user = User.objects.create(
            **UserModelData.reach_max_login_attempt()
        )

    def test_not_found_user(self):
        with self.assertRaises(User.DoesNotExist):
            check_user(self.non_vld_user.email, "pass")

    def test_found_user_but_not_valid_pwd(self):
        with self.assertRaises(ValueError):
            check_user(self.vld_user.email, "pwd")

    def test_valid_user(self):
        user = check_user(self.vld_user.email, "password")
        self.assertEqual(self.vld_user, user)
