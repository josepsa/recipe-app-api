from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email='testexample.com'
        password='testpass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    #all function name should start with test_ for django to pick it
    def test_new_user_email_normalized(self):
        sample_emails =[
            ['test@EXAMPLE.COM','test@example.com'],
            ['test1@EXAMPLE.com','test1@example.com']
        ]
        for email,expected in sample_emails:
            user=get_user_model().objects.create_user(email,'samplepassword123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','samplepassword123')

