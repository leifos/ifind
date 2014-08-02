__author__ = 'Craig'
from django.contrib.auth.models import User
from slowsearch.models import UKDemographicsSurvey, Experience, UserProfile
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat Password')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None


    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'condition', 'user_since', 'queries_submitted', 'links_visited')

SEX_CHOICES = (('N', 'Not Indicated'),
              ('M', 'Male'), ('F', 'Female'))

YES_CHOICES = (('', 'Not Specified'),
              ('Y', 'Yes'), ('N', 'No'))

YES_NO_CHOICES = (
    ('Y', 'Yes'), ('N', 'No'))

YEAR_CHOICES = (('', 'Not Specified'),
               ('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'),
               ('5', 'Fifth Year'), ('6', 'Completed'), ('7', 'Postgraduate'))

EXPERIENCE_CHOICES = (('A', 'Agree'), ('U', 'Unsure'), ('D', 'Disagree'))


class UKDemographicsSurveyForm(forms.ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value=100, min_value=18, required=False)
    sex = forms.CharField(max_length=1, widget=forms.Select(choices=SEX_CHOICES), label="Please indicate your sex.",
                          required=False)
    education_undergrad = forms.CharField(widget=forms.Select(choices=YES_CHOICES),
                                          label="Are you undertaking, or have you obtained, an undergraduate degree?",
                                          required=False)
    education_undergrad_major = forms.CharField(widget=forms.TextInput(attrs={'size': '60', 'class': 'inputText'}),
                                                label="If yes, what is/was your subject area?", required=False)
    education_undergrad_year = forms.CharField(widget=forms.Select(choices=YEAR_CHOICES),
                                               label="What year are you in?", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
            print "clean age"
        return cleaned_data

    class Meta:
        model = UKDemographicsSurvey
        exclude = ('user',)


# checkbox for user validation
class RegValidation(forms.Form):
    terms = forms.BooleanField(label="I have read and agree to the Study Information and I have had the "
                               "opportunity to ask any questions via email*",
                               error_messages={'required': 'You must accept the terms and conditions'}, )
    questions = forms.BooleanField(required=True, initial=False,
                                   label="I understand that I am able to ask questions about this study at any time*",
                                   error_messages={'required': 'You must accept the terms and conditions'}, )
    name = forms.BooleanField(required=True, initial=False,
                              label="I understand that my name will not appear in any published document relating"
                              " to research conducted as part of this study*",
                              error_messages={'required': 'You must accept the terms and conditions'}, )
    info = forms.BooleanField(required=True, initial=False,
                              label="I am willing for anonymous data from my search sessions and questionnaires that "
                                    "I have submitted may be quoted in papers, journal articles and books that may be "
                                    "written by the researchers*",
                              error_messages={'required': 'You must accept the terms and conditions'}, )
    agree = forms.BooleanField(required=True, initial=False,
                               label="I agree to take part in this study*",
                               error_messages={'required': 'You must accept the terms and conditions'}, )

    age = forms.BooleanField(required=True, initial=False, label="I certify that I am aged 18 or over*",
                             error_messages={'required': 'You must be 18 or over to participate in the experiment'},)

    notify = forms.BooleanField(required=False, initial=False,
                                label="I would like to be notified by email of the outcome of this experiment",
                                error_messages={'required': 'You must accept the terms and conditions'}, )


class FinalQuestionnaireForm(forms.ModelForm):
    # level of ease of use of AB Search App
    ease = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I found that I could easily'
                                                                                           ' find what I was looking for'
                                                                                           ' with the search engine')

    # level of boredom experienced by user when using AB Search App
    boredom = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I found that it took an '
                                                                                              'overly long time for the '
                                                                                              'search engine to show me '
                                                                                              'my results ')

    # level of rage experienced by user when using AB Search App
    frustration = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='Navigating with the '
                                                                                                  'interface on the '
                                                                                                  'search engine '
                                                                                                  'frustrated me')

    # level of visual pleasantry
    visuals = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='The search engine '
                                                                                                 'displayed my results '
                                                                                                 'in a manner pleasing '
                                                                                                 'to the eye ')

    # level of indifference experienced by user when using AB Search App
    indifference = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I found the search '
                                                                                                   'engine no different '
                                                                                                   'to any other search'
                                                                                                   ' engine I have '
                                                                                                   'used ')

   # level of confusion experienced by user when using AB Search App
    confusion = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I found it difficult '
                                                                                                'to work out how to '
                                                                                                'use the search engine'
                                                                                                ' interface ')

    # any additional comments the user wishes to add about their experience of the AB Search App
    comment = forms.CharField(widget=forms.Textarea, label='Please add any other comments you may have about '
                                                           'the search engine:')

    class Meta:
        model = Experience
        exclude= ('user',)