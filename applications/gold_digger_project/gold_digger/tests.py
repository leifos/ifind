

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File
from gold_digger.models import UserProfile
from gold_digger.forms import UserForm, UserProfileForm
from game import yieldgen, cuegen
import collections


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
        r = yieldgen.RandomYieldGenerator(depth)
        yield_array = r.make_yields()
        count = 0

        for y in yield_array:
            count += 1

        self.assertEqual(count, depth)

    def test_constant_yield(self):
        """
        Test if the constant_yield(depth) method returns an array of (depth) values,
        and that they are all the same.
        """

        depth = 10
        c = yieldgen.ConstantYieldGenerator(depth)
        yield_array = c.make_yields()
        count = 0
        comp = yield_array[0]

        for y in yield_array:
            count += 1
            self.failIf(comp != y)

        self.assertEqual(count, depth)

    def test_linear_yield(self):
        """
        Test if the linear_yield(depth) method returns an array of (depth) values,
        and that the values are appropriately produced according to the linear function devised.
        """

        depth = 10
        l = yieldgen.LinearYieldGenerator(depth)
        yield_array = l.make_yields()
        count = 0

        b = l.max
        m = yieldgen.m

        for y in yield_array:

            x = (y-b)/m
            self.assertEqual(x, count)
            count += 1

        self.assertEqual(count, depth)

    def test_quadratic_yield(self):
        """
        Test if QuadraticYieldGenerator(depth) return an appropriate array of yields
        """
        test_array = []
        depth = 10

        for x in range(depth):
            a = -1.8    # The steepness of the curve
            x1 = 0      # The gold is never negative
            x2 = depth
            y = a*(x - x1)*(x-x2)
            rounded = int(round(y))
            test_array.append(rounded)


        q = yieldgen.QuadraticYieldGenerator(depth)
        yield_array = q.make_yields()

        compare = lambda xc, yc: collections.Counter(xc) == collections.Counter(yc)
        same = compare(test_array, yield_array)
        self.assertEqual(same, True)

    def test_exponential_yield(self):
        """
        Test if the ExponentialYieldGenerator(depth) method returns an array of (depth) values,
        and that:
        - The first value of the array is 0
        - The second value is the maximum amount of gold
        """

        depth = 10
        r = yieldgen.ExponentialYieldGenerator(depth)
        yield_array = r.make_yields()
        count = 0
        max = r.max

        for y in yield_array:
            count += 1

        self.assertEqual(count, depth)
        self.assertEqual(0, yield_array[0])
        self.assertEqual(max, yield_array[1])

    def test_cubic_yield(self):
        """
        Test if CubicYieldGenerator(depth) returns an appropriate array of yields
        """
        test_array = []
        depth = 10

        for x in range(depth):
            a = 0.5
            c = 0
            y = int(round(pow((a*x), 3) + c*x))
            test_array.append(y)

        c = yieldgen.CubicYieldGenerator(depth)
        yield_array = c.make_yields()

        compare = lambda xc, yc: collections.Counter(xc) == collections.Counter(yc)
        same = compare(test_array, yield_array)
        self.assertEqual(same, True)