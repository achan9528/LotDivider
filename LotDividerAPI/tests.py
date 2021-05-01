from rest_framework import test
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Project
from django.contrib.auth.hashers import make_password

# Register View Test
class RegisterTestCase(test.APITestCase):
    
    def setUp(self):
        self.url = ('http://localhost:8000/api/rest-auth/registration/')

    def test_registerUser(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(get_user_model().objects.filter(name="Alex")),1)
        

    def test_registerUser_noEmail(self):
        data = {
            'name': 'Alex',
            'email': '',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_nameLessThan3(self):
        data = {
            'name': 'Al',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_passwordsDoNotMatch(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'FAKEPASSWORD',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_hashPassword(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test = get_user_model().objects.get(email=data['email'])
        self.assertNotEqual(test.password, data['password'])

# tests Login Route 
class LoginTestCase(test.APITestCase):
    # intial setup with a test user
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        print(get_user_model().objects.all())

    # base functionality case
    def test_loginUser(self):
        url = ('http://localhost:8000/api/rest-auth/login/')
        data = {
            'email': 'test@test.com',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEquals(len(get_user_model().objects.all()), 1)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
    def test_403Error(self):
        url = ('http://localhost:8000/api/welcome/')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_200WithToken(self):
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.get('http://localhost:8000/api/welcome/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, {'welcome': 'hello!'})
        print(response.data)

class ProjectTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )

        pwHash = make_password('test5678')
        get_user_model().objects.create(
            name =  'Chris',
            email = 'test2@test.com',
            alias = 'cc',
            password = pwHash,
        )
        
        project = Project.objects.create(name= 'testProject')
        project.owners.add(get_user_model().objects.first())

        
    def test_setUpData(self):
        self.assertEqual(Project.objects.first().owners.all()[0].name,'Alex')

    def test_createProject(self):
        url = ('http://localhost:8000/api/projects/')
        data = {
            'name': 'testProject2',
            'owners': [
                {
                    'id': 1,
                    'name': 'Alex',
                    'email': 'test@test.com',
                    'alias': 'ac',
                }
            ],
        }
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.first().name, 'testProject')
        self.assertEqual(Project.objects.first().owners.all()[0].name, 'Alex')

    def test_listProjects(self):
        url = ('http://localhost:8000/api/projects/')
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_listProjectsDifferentUser(self):
        url = ('http://localhost:8000/api/projects/')
        self.client.login(email='test2@test.com', password='test5678')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
