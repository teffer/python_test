from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser, Organization

class UserModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organization = Organization.objects.create(
            name='Test Org',
            description='Test description'
        )
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User',
            phone='88005552525'
        )
        self.user.organizations.add(self.organization)


    def test_user_creation(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser1@example.com',
            'password': 'testpass',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '88005552525',
            'organizations': [int(self.organization.id)],
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_profile_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('user-profile', args=[self.user.id]), {
            'first_name': 'Updated'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_organization_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('organization-create'), {
            'name': 'New Org',
            'description': 'New description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)

    def test_organization_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_organization_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('organization-detail', args=[self.organization.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['organization']['name'], 'Test Org')
        self.assertEqual(len(response.data['users']), 1)

    def test_token_obtain_pair(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'test@example.com',
            'password': 'testpass'
        })
        print('\n')
        print(response.content) 
        print('\n')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
