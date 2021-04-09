from django.test import TestCase, Client
from lots.models import *
from django.core.exceptions import ObjectDoesNotExist

class LotTest(TestCase):
    @classmethod
    def setUp(cls):
        newUser = User.objects.create(
            name = "stephanie",
            alias = "schan",
            email = "schan@test.com",
            password = 'test1234',
        )
        User.objects.create(
            name = "alex",
            alias = "achan",
            email = "achan@test.com",
            password = 'test1234',
        )

    def test_dashboard(self):
        print("Hello")
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/portfolios/new/')
        self.assertEqual(response.status_code, 302)

    def test_get_user(self):
        newUser = User.objects.get(id=1)
        self.assertEqual(newUser.name, 'stephanie')
        self.assertIsNotNone(newUser.number, 'stephanie')
    
    def test_edit_user(self):
        newUser = User.objects.get(id=1)
        newUser.name = 'stephanieChan'
        self.assertEqual(newUser.name, 'stephanieChan')

    def test_delete_user(self):
        num_deleted = User.objects.get(id=1).delete()[0]
        self.assertEqual(num_deleted, 1)

    def test_view_addPortfolio(self):
        c = Client()
        post_data = {
            "name": "testPortfolio"
        }
        response = c.post('/portfolios/add/', post_data)
        self.assertEqual(response.status_code, 302)
        newPortfolio = Portfolio.objects.last()
        print(newPortfolio.name)
        self.assertEqual(newPortfolio.name, post_data['name'])

