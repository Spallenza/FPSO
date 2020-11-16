from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from faker import Faker

from api.models.User import User
from api.views import UserViewSet


class TestUsers(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faker = Faker()
        self.user = User.objects.create_user(email=self.faker.email(), username=self.faker.name(),
                                             password=self.faker.password(),
                                             is_staff=True)
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({'get': 'list', 'post': 'create',
                                         'patch': 'partial_update', 'delete': 'destroy'})
        self.uri = '/users/'

    def test_create(self):
        request = self.factory.post(self.uri, {'first_name': self.faker.first_name(),
                                               'last_name': self.faker.last_name(),
                                               'email': self.faker.email(),
                                               'password': self.faker.password()}, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        new_user = User.objects.create_user(email=self.faker.email(), username=self.faker.name(),
                                            password=self.faker.password(),
                                            is_staff=True)

        new_first_name = self.faker.first_name()
        request = self.factory.patch(self.uri + str(new_user.id),
                                     {'first_name': new_first_name},
                                     format='json')

        force_authenticate(request, user=new_user)
        response = self.view(request, pk=new_user.id)

        user = User.objects.get(id=new_user.id)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(user.first_name, new_first_name, 'Expected First name to be {0}, received {1} instead.'
                         .format(new_first_name, user.first_name))

    def test_list(self):
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_delete(self):
        new_user = User.objects.create_user(email=self.faker.email(), username=self.faker.name(),
                                            password=self.faker.password(),
                                            is_staff=True)

        request = self.factory.delete(self.uri + str(new_user.id))

        force_authenticate(request, user=new_user)
        response = self.view(request, pk=new_user.id)

        user = User.objects.filter(id=new_user.id).first()

        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))

        self.assertIsNone(user, 'User should not be found')
