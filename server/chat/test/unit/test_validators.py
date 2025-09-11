from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from chat.models import Room
from chat.validators import validate_name, validate_access, validate_status, validate_limit

User = get_user_model()


class ValidateNameTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )
        Room.objects.create(
            owner=self.user,
            name='Existing Room'
        )

    def test_valid_name(self):
        """Test valid room names pass validation"""
        valid_names = ['Valid Room', 'Room123', 'Chat Room 2024', 'ABC']
        for name in valid_names:
            self.assertEqual(validate_name(name), name)

    def test_name_too_short(self):
        """Test name shorter than 3 characters fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_name('AB')
        self.assertIn('at least 3 characters', str(cm.exception))

    def test_name_too_long(self):
        """Test name longer than 255 characters fails"""
        long_name = 'A' * 256
        with self.assertRaises(ValidationError) as cm:
            validate_name(long_name)
        self.assertIn('should not be more than 255', str(cm.exception))

    def test_name_invalid_characters(self):
        """Test name with invalid characters fails"""
        invalid_names = ['Room@123', 'Room#Test', 'Room$pecial', 'Room!']
        for name in invalid_names:
            with self.assertRaises(ValidationError) as cm:
                validate_name(name)
            self.assertIn('letters, numbers, and spaces', str(cm.exception))

    def test_duplicate_name(self):
        """Test that existing room name fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_name('Existing Room')
        self.assertIn('already exists', str(cm.exception))

    def test_name_with_only_spaces(self):
        """Test name with only spaces fails"""
        with self.assertRaises(ValidationError) as cm:
            validate_name('   ')
        self.assertIn('letters, numbers, and spaces', str(cm.exception))


class ValidateAccessTest(TestCase):
    def test_valid_access_types(self):
        """Test valid access types pass validation"""
        self.assertEqual(validate_access(Room.PUBLIC), Room.PUBLIC)
        self.assertEqual(validate_access(Room.PRIVATE), Room.PRIVATE)

    def test_invalid_access_type(self):
        """Test invalid access type fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_access('invalid_access')
        self.assertIn('Invalid access type', str(cm.exception))


class ValidateStatusTest(TestCase):
    def test_valid_status_types(self):
        """Test valid status types pass validation"""
        self.assertEqual(validate_status(Room.ACTIVE), Room.ACTIVE)
        self.assertEqual(validate_status(Room.INACTIVE), Room.INACTIVE)

    def test_invalid_status_type(self):
        """Test invalid status type fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_status('invalid_status')
        self.assertIn('Invalid status type', str(cm.exception))


class ValidateLimitTest(TestCase):
    def test_valid_limits(self):
        """Test valid limit values pass validation"""
        valid_limits = [1, 10, 25, 50]
        for limit in valid_limits:
            self.assertEqual(validate_limit(limit), limit)

    def test_limit_too_low(self):
        """Test limit below 1 fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_limit(0)
        self.assertIn('between 1 and 50', str(cm.exception))

    def test_limit_too_high(self):
        """Test limit above 50 fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_limit(51)
        self.assertIn('between 1 and 50', str(cm.exception))

    def test_negative_limit(self):
        """Test negative limit fails validation"""
        with self.assertRaises(ValidationError) as cm:
            validate_limit(-1)
        self.assertIn('between 1 and 50', str(cm.exception))
