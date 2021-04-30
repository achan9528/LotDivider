from rest_framework import test
from rest_framework import status
from LotDividerAPI.models import User

# Registration View Test
class RegistrationTestCase(test.APITestCase):
    def test_registerUser(self):
        url = ('http://localhost:8000/api/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(name="Alex")),1)

    def test_registerUser_noEmail(self):
        url = ('http://localhost:8000/api/registration/')
        data = {
            'name': 'Alex',
            'email': '',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_nameLessThan3(self):
        url = ('http://localhost:8000/api/registration/')
        data = {
            'name': 'Al',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_passwordsDoNotMatch(self):
        url = ('http://localhost:8000/api/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'FAKEPASSWORD',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            