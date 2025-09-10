from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPass123!",
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_create_user(self):
        """Test creating a user with valid data"""
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("TestPass123!"))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_string_representation(self):
        """Test the string representation of user model"""
        self.assertEqual(str(self.user), "test_user")

    def test_unique_username_constraint(self):
        """Test that username must be unique"""
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data["email"] = "different@example.com"

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_unique_email_constraint(self):
        """Test that email must be unique"""
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data["username"] = "different_user"

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_user_ordering(self):
        """Test that users are ordered by date_joined descending"""
        user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="TestPass123!",
        )

        users = User.objects.all()
        self.assertEqual(users.first(), user2)  # Most recent first
        self.assertEqual(users.last(), self.user)  # Oldest (from setUpTestData)
