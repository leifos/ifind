

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File
from gold_digger.models import UserProfile


class ModelTest(TestCase):

    user_info = {'username': 'guybrush',
                 'email': 'guy@monkey.island',
                 'password': 'secret'}

    def test_user_profile(self):

        # Check if UserProfile object is created with appropriate data

        new_user = User.objects.create_user(**self.user_info)
        user_profile = UserProfile.objects.create(user=new_user, picture='something.gif', location='Here')

        self.assertEquals(user_profile.id, new_user.id)

    def test_user_profile_data(self):

        # Test if user is active

        new_user = User.objects.create_user(**self.user_info)

        self.assertEqual(new_user.username, 'guybrush')
        self.assertEqual(new_user.email, 'guy@monkey.island')
        self.failUnless(new_user.check_password('secret'))
        self.failIf(not new_user.is_active)

    def test_image_addition(self):

        new_user = User.objects.create_user(**self.user_info)

        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.picture = File(open("static/glasgow.gif"))
        user_profile.location = "NYC"
        user_profile.save()

        p = UserProfile.objects.get(id=1).picture.path

        self.failUnless(open(p), 'file not found')

