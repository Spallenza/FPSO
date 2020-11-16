from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from faker import Faker

from api.models.User import User
from api.models.Vessel import Vessel
from api.views import VesselViewSet


class TestVessels(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faker = Faker()
        self.user = User.objects.create_user(email=self.faker.email(), username=self.faker.name(),
                                             password=self.faker.password(),
                                             is_staff=True)
        self.factory = APIRequestFactory()
        self.view = VesselViewSet.as_view({'get': 'list', 'post': 'create',
                                         'patch': 'partial_update', 'delete': 'destroy'})
        self.uri = '/vessels/'

    def test_create(self):
        request = self.factory.post(self.uri, {'code': self.faker.sentence(nb_words=1)}, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        new_vesel = Vessel.objects.create(code=self.faker.sentence(nb_words=1))

        new_code = self.faker.sentence(nb_words=1)
        request = self.factory.patch(self.uri + str(new_vesel.id),
                                     {'code': new_code},
                                     format='json')

        force_authenticate(request, user=self.user)
        response = self.view(request, pk=new_vesel.id)

        vessel = Vessel.objects.get(id=new_vesel.id)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(vessel.code, new_code, 'Expected number to be {0}, received {1} instead.'
                         .format(new_code, vessel.code))

    def test_list(self):
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_delete(self):
        new_vessel = Vessel.objects.create(code=self.faker.sentence(nb_words=1))
        request = self.factory.delete(self.uri + str(new_vessel.id))

        force_authenticate(request, user=self.user)
        response = self.view(request, pk=new_vessel.id)

        vessel = Vessel.objects.filter(id=new_vessel.id).first()

        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))

        self.assertIsNone(vessel, 'Vessel should not be found')


    def test_cant_insert_duplicate(self):
        vesel = Vessel.objects.create(code=self.faker.sentence(nb_words=1))

        request = self.factory.post(self.uri, {'code': vesel.code}, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))
