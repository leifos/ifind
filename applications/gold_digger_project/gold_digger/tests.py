

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File
from gold_digger.models import UserProfile
from gold_digger.forms import UserForm, UserProfileForm
from game import Yieldgen, Cuegen


class ModelTest(TestCase):

    user_info = {'username': 'guybrush',
                 'email': 'guy@monkey.island',
                 'password': 'secret'}


    def test_user_profile_data(self):
        """
        Check if UserProfile object is created with appropriate  data
        """

        new_user = User.objects.create_user(**self.user_info)
        user_profile = UserProfile.objects.create(user=new_user, picture='something.gif', location='Here')

        self.assertEqual(new_user.username, 'guybrush')
        self.assertEqual(new_user.email, 'guy@monkey.island')
        self.failUnless(new_user.check_password('secret'))
        self.failIf(not new_user.is_active)
        self.assertEquals(user_profile.id, new_user.id)



    def test_image_addition(self):
        """
        This adds the image in the wrong spot
        """

        new_user = User.objects.create_user(**self.user_info)

        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.picture = File(open("static/glasgow.gif"))
        user_profile.location = "NYC"
        user_profile.save()

        p = UserProfile.objects.get(id=1).picture.path

        self.failUnless(open(p), 'file not found')

class FormTests(TestCase):

    def test_clean_password(self):
        """
        This test fails if a form with two different passwords is valid
        """

        form = UserForm(data={'username': 'guybrush',
                              'email': 'guy@monkey.island',
                              'password': 'secret',
                              'password2': 'foo'})

        self.failIf(form.is_valid())


class GameTest(TestCase):

    def test_random_yield(self):
        """
        Test if the random_yield(depth) method returns an array of (depth) values.
        """

        depth = 10
        r = Yieldgen.random_yield(depth)
        count = 0

        for y in r:
            count += 1

        self.assertEqual(count, depth)

    def test_constant_yield(self):
        """
        Test if the constant_yield(depth) method returns an array of (depth) values,
        and that they are all the same.
        """

        depth = 10
        c = Yieldgen.constant_yield(depth)
        count = 0
        comp = c[0]

        for y in c:
            count += 1
            self.failIf(comp != y)

        self.assertEqual(count, depth)

    def test_linear_yield(self):
        """
        Test if the linear_yield(depth) method returns an array of (depth) values,
        and that the values are appropriately produced according to the linear function devised.
        """

        b = Yieldgen.b
        m = Yieldgen.m

        depth = 10
        c = Yieldgen.linear_yield(depth)
        count = 0

        for y in c:

            x = (y-b)/m
            self.assertEqual(x, count)
            count += 1

        self.assertEqual(count, depth)

    def test_cue_span(self):
            """
            Test if Cuegen assigns the appropriate due to the yield values
            """

            max = yieldgen.b
            rangecue = cuegen.cue_range

            array_list = []

            count = 0

            for r in rangecue:
                cue_list = []
                for x in range(max, 0, -1):

                    cue_list.append(x)
                    if x == rangecue:
                        count = 0
                        array_list.append(cue_list)
                        break
                    else:
                        count += 1






        # cue_patterns = cuegen.cue_patterns
        #
        # span = cuegen.cue_function(accuracy)
        # upper_limit = yield_array[0] + span
        # lower_limit = yield_array[0] - span
        #
        # cue = random.randint(lower_limit, upper_limit)
        # x = cuegen.cue_range
        #
        # max = yieldgen.b
        #
        # index = 0
        # countcue = 5
        #
        # array = []
        # for d in range(max, 0, -1):
        #     array.append(d)


