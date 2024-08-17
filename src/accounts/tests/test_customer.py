from django.test import TestCase
from accounts.models.custom_user import Profile, User
from accounts.models.customer import Customer, CustomerAddress, Address
from django.db.utils import IntegrityError

# CustomerManager Tests
class CustomerManagerTests(TestCase):

    def test_create_customer(self):
        email = "customer@example.com"
        password = "password123"
        customer = Customer.objects.create_customer(email=email, password=password)

        self.assertEqual(customer.email, email)
        self.assertTrue(customer.check_password(password))
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_superuser)
        self.assertTrue(customer.is_customer)

    def test_create_customer_no_email(self):
        with self.assertRaises(ValueError):
            Customer.objects.create_customer(email="", password="password123")
            

# Customer Tests
class CustomerTests(TestCase):

    def test_customer_str(self):
        email = "customer@example.com"
        customer = Customer.objects.create_customer(email=email, password="password123")
        self.assertEqual(str(customer), email)

    def test_save_customer(self):
        email = "customer@example.com"
        customer = Customer.objects.create_customer(email=email, password="password123")

        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_superuser)
        self.assertTrue(customer.is_customer)

    def test_get_customer_by_email(self):
        email = "customer@example.com"
        Customer.objects.create_customer(email=email, password="password123")
        
        customer = Customer.get_customer_by_email(email)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.email, email)

        non_existent_customer = Customer.get_customer_by_email("nonexistent@example.com")
        self.assertFalse(non_existent_customer)


# CustomerAddress Tests
class CustomerAddressTests(TestCase):

    def test_customer_address_str(self):
        customer = Customer.objects.create_customer(email="customer@example.com", password="password123")
        address = Address.objects.create(street="123 Main St", city="Tehran", state="Tehran", zipcode="1234567890")
        customer_address = CustomerAddress.objects.create(customer=customer, address=address, main_address=True)

        self.assertEqual(str(customer_address), f"{customer}-address")

    def test_customer_address_creation(self):
        customer = Customer.objects.create_customer(email="customer@example.com", password="password123")
        address = Address.objects.create(street="123 Main St", city="Tehran", state="Tehran", zipcode="1234567890")
        customer_address = CustomerAddress.objects.create(customer=customer, address=address, main_address=True)

        self.assertTrue(customer_address.main_address)
        self.assertEqual(customer_address.customer, customer)
        self.assertEqual(customer_address.address, address)

# Address Tests
class AddressTests(TestCase):

    def test_address_str(self):
        address = Address.objects.create(street="123 Main St", city="Tehran", state="Tehran", zipcode="1234567890")
        self.assertEqual(str(address), "Tehran, Tehran, 123 Main St")

    def test_address_creation(self):
        address = Address.objects.create(street="123 Main St", city="Tehran", state="Tehran", zipcode="1234567890")
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.city, "Tehran")
        self.assertEqual(address.state, "Tehran")
        self.assertEqual(address.zipcode, "1234567890")
        

class CustomerProfileTests(TestCase):

    def test_profile_creation_after_customer_creation(self):
        email = "customer@example.com"
        customer = Customer.objects.create_customer(email=email, password="password123")

        self.assertTrue(Profile.objects.filter(user=customer).exists())

        profile = Profile.objects.get(user=customer)
        # self.assertEqual(profile.user, customer) # erorr  <User: customer@example.com> != <Customer: customer@example.com>

        # Compare user ids instead of objects directly
        self.assertEqual(profile.user.id, customer.id)
        self.assertEqual(profile.get_fullname(), "کاربر جدید")
        
        

from django.db.models.signals import post_save
from unittest.mock import MagicMock

class SignalTest(TestCase):

    def test_signal_triggered_on_customer_creation(self):
        mock_handler = MagicMock()
        post_save.connect(mock_handler, sender=Customer)

        try:
            email = "customer@example.com"
            customer = Customer.objects.create_customer(email=email, password="password123")

            # Assert that the signal was triggered once
            self.assertTrue(mock_handler.called)
            mock_handler.assert_called_once_with(
                sender=Customer,
                instance=customer,
                created=True,
                signal=post_save,
                update_fields=None,
                raw=False,
                using='default'
            )
        finally:
            post_save.disconnect(mock_handler, sender=Customer)

