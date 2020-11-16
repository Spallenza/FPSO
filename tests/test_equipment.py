from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from faker import Faker

from api.models.User import User
from api.models.Vessel import Vessel
from api.models.Equipment import Equipment
from api.views import EquipmentViewSet


class TestEquipment(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faker = Faker()
        self.user = User.objects.create_user(email=self.faker.email(), username=self.faker.name(),
                                             password=self.faker.password(),
                                             is_staff=True)

        self.vessel = Vessel.objects.create(code=self.faker.sentence(nb_words=1))
        self.factory = APIRequestFactory()
        self.view = EquipmentViewSet.as_view({'get': 'list', 'post': 'create',
                                         'patch': 'partial_update', 'delete': 'destroy'})
        self.uri = '/equipments/'

    def test_create(self):
        request = self.factory.post(self.uri, {'name': self.faker.sentence(nb_words=1),
                                                'code': self.faker.sentence(nb_words=1),
                                                'location': self.faker.country(),
                                                'vessel': self.vessel.id
                                                }, format='json')

        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

        self.assertEqual(response.data['status'], 'active', 'Expected status to be {0}, received {1} instead.'
                         .format('active', response.data['status']))



    def test_update(self):
        new_equipment = Equipment.objects.create(
                                                    name=self.faker.sentence(nb_words=1),
                                                    code= self.faker.sentence(nb_words=1),
                                                    location= self.faker.country(),
                                                    vessel= self.vessel
                                                )

        new_code = self.faker.sentence(nb_words=1)
        request = self.factory.patch(self.uri + str(new_equipment.id),
                                     {'code': new_code},
                                     format='json')

        force_authenticate(request, user=self.user)
        response = self.view(request, pk=new_equipment.id)

        equipment = Equipment.objects.get(id=new_equipment.id)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(equipment.code, new_code, 'Expected number to be {0}, received {1} instead.'
                         .format(new_code, equipment.code))
        
        
    def test_list(self):
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_delete(self):
        new_equipment = Equipment.objects.create(
                                                    name=self.faker.sentence(nb_words=1),
                                                    code= self.faker.sentence(nb_words=1),
                                                    location= self.faker.country(),
                                                    vessel= self.vessel
                                                )
        request = self.factory.delete(self.uri + str(new_equipment.id))

        force_authenticate(request, user=self.user)
        response = self.view(request, pk=new_equipment.id)

        equipment = Equipment.objects.filter(id=new_equipment.id).first()

        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))

        self.assertIsNone(equipment, 'Vessel should not be found')

    def test_cant_insert_duplicate(self):
        equipment = Equipment.objects.create(
                                                    name=self.faker.sentence(nb_words=1),
                                                    code= self.faker.sentence(nb_words=1),
                                                    location= self.faker.country(),
                                                    vessel= self.vessel
                                                )

        request = self.factory.post(self.uri, {'name': self.faker.sentence(nb_words=1),
                                                'code': equipment.code,
                                                'location': self.faker.country(),
                                                'vessel': self.vessel.id
                                                }, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))
