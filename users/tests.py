from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, UserManager
from django.urls import reverse
from .views import get_tokens_for_user
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserCreateTests(APITestCase):

    def test_create_account(self):
        users_before = User.objects.count()
        url = reverse('register')
        expected_email = "test@gmail.com"
        expected_username = "test"
        data = {"email": expected_email, "password": "111", "username": expected_username}
        response = self.client.post(url, data, format='json')

        users_after = User.objects.count()
        last_user = User.objects.order_by('-id').first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Wrong response code.")
        self.assertEqual(users_before + 1, users_after, "Users number not increased.")
        self.assertEqual(last_user.email, expected_email, "New user email is incorrect.")
        self.assertEqual(last_user.username, expected_username, "New username is incorrect.")


class UsersTests(APITestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(
            email="test1@gmail.com", password="111", username="test1")
        user_test1.save()
        user_test2 = User.objects.create_user(
            email="test2@gmail.com", password="111", username="test2")
        user_test2.save()

        self.user_test1_token = get_tokens_for_user(user_test1)['access']
        # self.user_test2_token = Token.objects.create(user=user_test2)

    def test_login(self):
        url = reverse('login')
        data = {"email": "test1@gmail.com", "password": "111"}
        response = self.client.post(url, data, format='json')
        user = User.objects.filter(email=data["email"]).first()
        raw_token = response.data.get('token')

        self.assertIsNotNone(raw_token)
        
        auth = JWTAuthentication()
        validated_token = auth.get_validated_token(raw_token)
        token_user = auth.get_user(validated_token)

        self.assertEqual(token_user.id, user.id, "User ID from token not equal to actual.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('update')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_test1_token)
        data = {
            "email": "test1@gmail.com",
            "password": "111",
            "first_name": "inga",
            "last_name": "gffed",
            "username": "test1",
            "description": "ukjuhtrgrfvrt"
        }
        response = self.client.put(url, data, format='json')
        description = response.data.get('description')
        self.assertIsNotNone(description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_info(self):
        user = User.objects.first()
        url = f'/users/{user.id}'
        response = self.client.get(url, format='json')
        username = response.data.get('username')
        self.assertEqual(username, 'test1')
        email = response.data.get('email')
        self.assertEqual(email, 'test1@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile(self):
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_test1_token)
        response = self.client.get(url, format='json')
        email = response.data.get('email')
        self.assertEqual(email, 'test1@gmail.com')
        username = response.data.get('username')
        self.assertEqual(username, 'test1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_avatar_from_url(self):
        url = reverse('upload_avatar_from_url')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_test1_token)
        data = {
            "url": "https://p2.zoon.ru/preview/U3a1uyz3s8zY1zpnQ3x9vg/2400x1500x85/1/7/5/original_5d5d700467cd9302f61f1858_5d5d70990a995.jpg"}
        response = self.client.post(url, data, format='json')
        user = User.objects.first()
        self.assertNotEqual(user.avatar, 'images/noimage-300x300.png')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

