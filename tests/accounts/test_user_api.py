from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

CREATE_USER_URL = reverse("accounts:create")
ACCOUNT_URl = reverse("accounts:account", kwargs={"user_id": 1})


def create_user(**kwargs):
    """Creates and returns a new User"""
    return get_user_model().objects.create_user(**kwargs)


# Unauthenticated requests
class TestPublicUserApiTests(APITestCase):
    """Tests the public features of the API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {
            "first_name": "john",
            "last_name": "doe",
            "email": "test@example.com",
            "password": "testpassword123"
        }

    def test_create_user_success(self):
        """
        Tests creating a user is successful
        """

        response = self.client.post(CREATE_USER_URL, data=self.data)
        user = get_user_model().objects.get(email=self.data["email"])
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertNotIn("password", response.data)

    def test_user_with_email_exists_error(self):
        """
        Tests an error is generated when a user with an existing email already exists
        """
        _ = create_user(**self.data)
        response = self.client.post(CREATE_USER_URL, data=self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Tests that a given password meets the required length of passwords
        """
        payload = {
            "first_name": "john",
            "last_name": "doe",
            "email": "test@example.com",
            "password": "te"
        }
        response = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email=payload["email"]).exists()
        )

    def test_retrieve_user_unauthorized(self):
        """Tests authentication is required and enforced for user account"""
        response = self.client.get(ACCOUNT_URl, AnonymousUser.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(APITestCase):
    """Tests that require authentication"""

    def setUp(self) -> None:
        """set up authentication"""
        self.data = {
            "first_name": "john",
            "last_name": "doe",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        self.user = create_user(**self.data)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for authenticated users"""
        response = self.client.get(
            reverse("accounts:account", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            self.data
        )

    def test_post_account_not_allowed(self):
        """Test POST not allowed for the account endpoint"""
        response = self.client.post(ACCOUNT_URl, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_email_works(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            "email": "test2@example.com"
        }
        response = self.client.patch(ACCOUNT_URl, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_user_password_works(self):
        """Test updating the password works"""
        payload = {
            "password": "new_password123"
        }
        response = self.client.patch(ACCOUNT_URl, payload)
        self.user.refresh_from_db()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_updating_both_email_and_password_works(self):
        """Test authenticated user can update both the email and password"""
        payload = {
            "email": "test2@example.com",
            "password": "secure_password"
        }

        response = self.client.patch(ACCOUNT_URl, payload)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
