from rest_framework import test
from rest_framework import status
from django.contrib.auth import get_user_model

# Register View Test
class RegisterTestCase(test.APITestCase):
    def test_registerUser(self):
        url = ('http://localhost:8000/api/rest-auth/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(get_user_model().objects.filter(name="Alex")),1)
        

    def test_registerUser_noEmail(self):
        url = ('http://localhost:8000/api/rest-auth/registration/')
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
        url = ('http://localhost:8000/api/rest-auth/registration/')
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
        url = ('http://localhost:8000/api/rest-auth/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'FAKEPASSWORD',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_hashPassword(self):
        url = ('http://localhost:8000/api/rest-auth/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test = get_user_model().objects.get(email=data['email'])
        self.assertNotEqual(test.password, data['password'])

# tests Login Route 
class LoginTestCase(test.APITestCase):
    # intial setup with a test user
    # def setup(self):

    # base functionality case
    def test_loginUser(self):
        url = ('http://localhost:8000/api/rest-auth/registration/')
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        self.client.post(url, data, format='json')


        url = ('http://localhost:8000/api/rest-auth/login/')
        data = {
            'email': 'test@test.com',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        print(response.data)
