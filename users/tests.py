from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_user(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass123",
            "age": 25,
            "rating": 1500,
            "country": "Test Country",
        }
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="testuser").rating, 1500)

    def test_create_user_invalid_data(self):
        data = {
            "username": "test user",  # Invalid: contains space
            "email": "test@test.com",
            "password": "testpass123",
            "age": 200,  # Invalid: too high
            "rating": 4000,  # Invalid: too high
            "country": "Test Country 123",  # Invalid: contains numbers
        }
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("age", response.data)
        self.assertIn("rating", response.data)
        self.assertIn("country", response.data)

    def test_update_user(self):
        user = User.objects.create_user("updateuser", "update@test.com", "updatepass")
        data = {"age": 30, "rating": 1600, "country": "Updated Country"}
        response = self.client.patch(f"/api/users/{user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.age, 30)
        self.assertEqual(user.rating, 1600)
        self.assertEqual(user.country, "Updated Country")

    def test_delete_user(self):
        user = User.objects.create_user("deleteuser", "delete@test.com", "deletepass")
        response = self.client.delete(f"/api/users/{user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username="deleteuser").count(), 0)
