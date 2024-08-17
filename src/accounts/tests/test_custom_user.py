from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()



# UserManager Tests
class UserManagerTests(TestCase):
    
    def test_create_user(self):
        email = "testuser@example.com"
        password = "password123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_create_superuser(self):
        email = "superuser@example.com"
        password = "password123"
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_without_staff_status(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password123", is_staff=False
            )

    def test_create_superuser_without_superuser_status(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password123", is_superuser=False
            )


# User Tests
class UserTests(TestCase):

    def test_user_str(self):
        email = "testuser@example.com"
        user = User.objects.create_user(email=email, password="password123")
        self.assertEqual(str(user), email)

    def test_is_owner(self):
        staff_user = User.objects.create_user(email="staff@example.com", password="password123", is_staff=True)
        superuser = User.objects.create_superuser(email="super@example.com", password="password123")

        self.assertTrue(staff_user.is_owner())
        self.assertFalse(superuser.is_owner())
        
        
# Profile Tests
class ProfileTests(TestCase):

    def test_profile_creation(self):
        email = "testuser@example.com"
        user = User.objects.create_user(email=email, password="password123")
        
        # Check that the profile is automatically created
        profile = Profile.objects.get(user=user)
        
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.get_fullname(), "کاربر جدید")

    def test_profile_str(self):
        email = "testuser@example.com"
        user = User.objects.create_user(email=email, password="password123")
        profile = Profile.objects.get(user=user)
        
        self.assertEqual(str(profile), user.email)

    def test_profile_fullname(self):
        email = "testuser@example.com"
        user = User.objects.create_user(email=email, password="password123")
        profile = Profile.objects.get(user=user)
        
        profile.first_name = "Ali"
        profile.last_name = "Rezaei"
        profile.save()
        
        self.assertEqual(profile.get_fullname(), "Ali Rezaei")





from django.db.models.signals import post_save
from unittest.mock import MagicMock

class SignalTest(TestCase):

    def test_signal_triggered_on_user_creation(self):
        mock_handler = MagicMock()
        post_save.connect(mock_handler, sender=User)

        try:
            email = "user@example.com"
            user = User.objects.create_user(email=email, password="password123")

            self.assertTrue(mock_handler.called)
            mock_handler.assert_called_once_with(
                sender=User,
                instance=user,
                created=True,
                signal=post_save,
                update_fields=None,
                raw=False,
                using='default'
            )
        finally:
            post_save.disconnect(mock_handler, sender=User)
