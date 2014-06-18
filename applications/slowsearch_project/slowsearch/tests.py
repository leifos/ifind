from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User

inappropriate_names = ['fuck', 'tits', 'ass']


class UserRegTests(TestCase):

    def test_for_inappropriate_language(self):
        new_user = User.objects.create_user(username='fuckwit', email='test@test.com', password='test')

        inappropriate = False

        for n in inappropriate_names:
            if n in new_user.username:
                inappropriate = True
                break

        self.assertFalse(inappropriate)