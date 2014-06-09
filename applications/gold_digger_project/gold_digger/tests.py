"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase

from gold_digger import forms


class RegistrationFormTests(TestCase):
    """
    Test the default registration forms.
    """
    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.

        """
        # Create a user so we can verify that duplicate usernames aren't
        # permitted.
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {'data': {'username': 'foobar',
                      'email': 'foo@example.com',
                      'password1': 'foo'},
            'error': ('username', [u"This value must contain only letters, numbers and underscores."])},
            # Already-existing username.
            {'data': {'username': 'alice',
                      'email': 'alice@example.com',
                      'password1': 'secret'},
            'error': ('username', [u"A user with that username already exists."])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.UserForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            #self.assertEqual(form.errors[invalid_dict['error'][0]],
            #                 invalid_dict['error'][1])

        #form = forms.UserForm(data={'username': 'foo',
        #                                    'email': 'foo@example.com',
        #                                    'password1': 'foo',
        #                                    'password2': 'foo'})
        #self.failUnless(form.is_valid())



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
