

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File
from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle
from gold_digger.forms import UserForm, UserProfileForm
from game import yieldgen, cuegen, mine
import collections

class ModelTest(TestCase):


    def test_user_profile_data(self):
        """
        Check if UserProfile object is created with appropriate  data
        """
        user_info = {'username': 'guybrush',
                 'email': 'guy@monkey.island',
                 'password': 'secret'}

        new_user = User.objects.create_user(**user_info)
        user_profile = UserProfile()
        user_profile.user = new_user

        scan = ScanningEquipment.objects.get_or_create(name="Oil Lamp", modifier=0.2, image='icons/Scan/Oil Lamp.png', price=1, description="It won't allow you to see much but it's better than going in blind!", store_val=20)[0]
        dig = DiggingEquipment.objects.get_or_create(name='Spoon', modifier=0.3, time_modifier=5, image='icons/Tools/Spoon.png', price=1, description="What am I supposed to do with this?", store_val=30)[0]
        move = Vehicle.objects.get_or_create(name='Boots', modifier=10, image='icons/Vehicle/Boots.png', price=1, description="Two boots is better than no boots!")[0]
        user_profile.equipment = scan
        user_profile.tool = dig
        user_profile.vehicle = move

        self.assertEqual(user_profile.user.username, 'guybrush')
        self.assertEqual(new_user.email, 'guy@monkey.island')
        self.failUnless(new_user.check_password('secret'))
        self.failIf(not new_user.is_active)
        self.failIf(not user_profile.equipment)
        self.failIf(not user_profile.tool)
        self.failIf(not user_profile.vehicle)
        self.assertEqual(user_profile.gold, 100)
        self.assertEqual(user_profile.games_played, 0)
        self.assertEqual(user_profile.game_overs, 0)
        self.assertEqual(user_profile.mines, 0)



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


class CueTest(TestCase):

    def test_appropriate_cue(self):

        test_array = [3, 11, 18, 25, 33, 39]
        maxgold = 42
        scan = 1

        cue_array = cuegen.make_cue(test_array, scan, maxgold)

        self.assertEqual(cue_array[0], 0)
        self.assertEqual(cue_array[1], 1)
        self.assertEqual(cue_array[2], 2)
        self.assertEqual(cue_array[3], 3)
        self.assertEqual(cue_array[4], 4)
        self.assertEqual(cue_array[5], 5)

    def test_cue_function(self):

        test_array = [3, 11, 18, 25, 33, 39]
        scan = 1
        maxgold = 42

        for t in test_array:
            a = cuegen.cue_function(scan, maxgold)
            self.assertEqual(t+a, t)



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


    def test_positive(self):

        c = yieldgen.CaliforniaQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

        c = yieldgen.YukonQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

        c = yieldgen.BrazilQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

        c = yieldgen.SouthAfricaQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

        c = yieldgen.ScotlandQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

        c = yieldgen.VictoriaQuadraticYieldGenerator(depth=10, max=100, min=0)
        yield_array = c.make_yields()
        for y in yield_array:
            self.failIf(y < 0)

    def test_mine(self):

        user_info = {'username': 'guybrush2',
                 'email': 'guy@monkey.island2',
                 'password': 'secret2'}

        new_user = User.objects.create_user(**user_info)
        user_profile = UserProfile()
        user_profile.user = new_user

        scan = ScanningEquipment.objects.get_or_create(name="Oil Lamp", modifier=0.2, image='icons/Scan/Oil Lamp.png', price=1, description="It won't allow you to see much but it's better than going in blind!", store_val=20)[0]
        dig = DiggingEquipment.objects.get_or_create(name='Spoon', modifier=0.3, time_modifier=5, image='icons/Tools/Spoon.png', price=1, description="What am I supposed to do with this?", store_val=30)[0]
        move = Vehicle.objects.get_or_create(name='Boots', modifier=10, image='icons/Vehicle/Boots.png', price=1, description="Two boots is better than no boots!")[0]
        user_profile.equipment = scan
        user_profile.tool = dig
        user_profile.vehicle = move

        accuracy = 0.2
        max_gold = 100
        gen = yieldgen.ScotlandQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        m = mine.Mine(gen, accuracy, user_profile)

        for block in m.blocks:
            self.failIf(block.cue == None)
            self.failIf(block.gold == None)
            self.failIf(block.dug == True)
            self.failIf((block.pos/10)>=1)
            self.failIf((block.pos/10)<=-1)