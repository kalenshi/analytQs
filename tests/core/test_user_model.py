"""
Tests the user model
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tests.accounts.test_user_api import create_user

CREATE_USER_URL = reverse("accounts:create")
TOKEN_URL = reverse("accounts:token")


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user = {
            "first_name": "john",
            "last_name": "doe",
            "email": "test@example.com",
            "password": "password123"
        }

    def test_create_user_with_email_successful(self):
        """
        Tests that creating a user with email works
        """

        user = get_user_model().objects.create_user(
            **self.user
        )

        self.assertEquals(user.email, self.user["email"])
        self.assertTrue(user.check_password(self.user["password"]))

    def test_create_superuser_works(self):
        user = get_user_model().objects.create_superuser(
            **self.user
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_token_for_user(self):
        """Tests generating token"""

        _ = create_user(**self.user)

        payload = {
            "email": self.user["email"],
            "password": self.user["password"]
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_token_bad_credentials(self):
        """Tests returns an error if bad credentials are passed in"""
        _ = create_user(**self.user)
        payload = {
            "email": self.user["email"],
            "password": "badpassword"
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test create token returns an error with no password """
        payload = {
            "email": "test@example.com",
            "password": ""
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
