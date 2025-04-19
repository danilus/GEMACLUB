from django.test import TestCase
from django.contrib.auth.models import User
from club.models import Person

class PersonSignalTest(TestCase):
    def test_person_created_when_user_is_created(self):
        user = User.objects.create_user(
            username='testuser',
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='test1234'
        )
        person = Person.objects.get(user=user)
        self.assertEqual(person.names, 'Juan')
        self.assertEqual(person.surnames, 'Pérez')
        self.assertEqual(person.email, 'juan@example.com')
