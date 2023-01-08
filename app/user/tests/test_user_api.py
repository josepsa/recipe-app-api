from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL=reverse('user:create')
TOKEN_URL=reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client=APIClient()

    def test_create_user(self):
        payload={
            'email':'testemail@example.com',
            'password':'testpass123',
            'name':'Test Name',
        }
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_with_same_email(self):
        payload={
            'email':'testemail@example.com',
            'password':'testpass123',
            'name':'Test Name',
        }
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        payload={
            'email':'testemail@example.com',
            'password':'test',
            'name':'Test Name',
        }
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        #checking user is not created
        user_exist=get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)


    def test_create_user_token(self):
        user_details={
            'name':'test name',
            'email':'testemail@example.com',
            'password':'testpassword'
        }

        create_user(**user_details)

        payload={
            'email':user_details['email'],
            'password':user_details['password']
        }

        res=self.client.post(TOKEN_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_user_token_bad_credentials(self):
        user_details={
            'name':'test name',
            'email':'testemail@example.com',
            'password':'correctpassword'
        }

        create_user(**user_details)

        payload={
            'email':user_details['email'],
            'password':'wrongpassword'
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_user_token_blank_password(self):
        payload={
            'email':'testemail@example.com',
            'password':''
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)