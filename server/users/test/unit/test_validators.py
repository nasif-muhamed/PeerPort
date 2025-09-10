from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.validators import validate_username, validate_email, validate_password

User = get_user_model()


class ValidateUsernameTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='existing_user',
            email='existing@example.com',
            password='TestPass123!'
        )

    def test_valid_username(self):
        """Test valid username passes validation"""
        valid_usernames = ['test_user', 'user_test', 'abcd', 'test_user_long']
        for username in valid_usernames:
            self.assertEqual(validate_username(username), username)

    def test_username_too_short(self):
        """Test username shorter than 4 characters fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_username('abc')
        self.assertIn('at least 4 characters', str(cm.exception))

    def test_username_too_long(self):
        """Test username longer than 20 characters fails"""
        long_username = 'a' * 21
        with self.assertRaises(ValidationError) as cm:
            validate_username(long_username)
        self.assertIn('cannot be longer than 20', str(cm.exception))

    def test_username_insufficient_letters(self):
        """Test username with less than 3 letters fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_username('ab__')
        self.assertIn('at least three letters', str(cm.exception))

    def test_username_invalid_characters(self):
        """Test username with invalid characters fails"""
        invalid_usernames = ['Test123', 'test-user', 'test@user', 'test user']
        for username in invalid_usernames:
            with self.assertRaises(ValidationError) as cm:
                validate_username(username)
            self.assertIn('lowercase letters and underscores', str(cm.exception))

    def test_username_already_taken(self):
        """Test that existing username fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_username('existing_user')
        self.assertIn('already taken', str(cm.exception))


class ValidateEmailTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='test_user',
            email='existing@example.com',
            password='TestPass123!'
        )

    def test_valid_email(self):
        """Test valid email passes validation"""
        valid_email = 'new@example.com'
        self.assertEqual(validate_email(valid_email), valid_email)

    def test_duplicate_email(self):
        """Test that existing email fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_email('existing@example.com')
        self.assertIn('already registered', str(cm.exception))

    def test_case_insensitive_email_check(self):
        """Test that email check is case insensitive"""
        with self.assertRaises(ValidationError) as cm:
            validate_email('EXISTING@EXAMPLE.COM')
        self.assertIn('already registered', str(cm.exception))


class ValidatePasswordTest(TestCase):
    def test_valid_password(self):
        """Test valid password passes validation"""
        valid_password = 'TestPass123!'
        self.assertEqual(validate_password(valid_password), valid_password)

    def test_password_too_short(self):
        """Test password shorter than 8 characters fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('Test1!')
        self.assertIn('at least 8 characters', str(cm.exception))

    def test_password_missing_special_char(self):
        """Test password without special character fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('TestPass123')
        self.assertIn('special character', str(cm.exception))

    def test_password_missing_uppercase(self):
        """Test password without uppercase letter fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('testpass123!')
        self.assertIn('uppercase letter', str(cm.exception))

    def test_password_missing_lowercase(self):
        """Test password without lowercase letter fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('TESTPASS123!')
        self.assertIn('lowercase letter', str(cm.exception))

    def test_password_missing_digit(self):
        """Test password without digit fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('TestPass!')
        self.assertIn('digit', str(cm.exception))

    def test_password_contains_space(self):
        """Test password with space fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_password('Test Pass123!')
        self.assertIn('not contain empty space', str(cm.exception))
