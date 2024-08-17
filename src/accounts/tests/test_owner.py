from django.test import TestCase

from accounts.models.custom_user import Profile, User
from accounts.models import Owner

class OwnerTests(TestCase):

    def test_create_restaurant_owner(self):
        email = "owner@example.com"
        password = "password123"
        owner = Owner.objects.create_restaurant_owner(email=email, password=password)

        self.assertEqual(owner.email, email)
        self.assertTrue(owner.check_password(password))
        self.assertTrue(owner.is_staff)
        self.assertFalse(owner.is_superuser)
        self.assertTrue(owner.is_active)

    def test_owner_save_method(self):
        email = "owner@example.com"
        owner = Owner.objects.create_restaurant_owner(email=email, password="password123")
        
        # Save the owner and check if is_staff and is_superuser are set correctly
        owner.save()
        
        self.assertTrue(owner.is_staff)
        self.assertFalse(owner.is_superuser)
        self.assertTrue(owner.is_active)

    def test_owner_profile_url(self):
        email = "owner@example.com"
        owner = Owner.objects.create_restaurant_owner(email=email, password="password123")
        
        # Check the profile URL
        self.assertEqual(owner.get_profile_url(), "/owner/dashboard/")
