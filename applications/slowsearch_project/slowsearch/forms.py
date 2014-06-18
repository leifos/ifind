__author__ = 'Craig'
from django.contrib.auth.models import User
from slowsearch.models import UKDemographicsSurvey, Experience
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


SEX_CHOICES = (('N', 'Not Indicated'),
              ('M', 'Male'), ('F', 'Female'))

YES_CHOICES = (('', 'Not Specified'),
              ('Y', 'Yes'), ('N', 'No'))

YES_NO_CHOICES = (
    ('Y', 'Yes'), ('N', 'No'))

YEAR_CHOICES = (('', 'Not Specified'),
               ('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'),
               ('5', 'Fifth Year'), ('6', 'Completed'))

EXPERIENCE_CHOICES = (('A', 'Agree'), ('U', 'Unsure'), ('D', 'Disagree'))


class UKDemographicsSurveyForm(forms.ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value=100, min_value=0, required=False)
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
    terms = forms.BooleanField(required=True, initial=False,
                               label="I have read and agree to the above terms and conditions",
                               error_messages={'required': 'You must accept the terms and conditions'},)


class FinalQuestionnaireForm(forms.ModelForm):
    # level of ease of use of AB Search App
    ease = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='The search engine was '
                                                                                           'easy to use:')

    # level of boredom experienced by user when using AB Search App
    boredom = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I quickly became bored '
                                                                                              'while using the search '
                                                                                              'engine:')

    # level of rage experienced by user when using AB Search App
    rage = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was enraged by the search'
                                                                                           ' engine:')

    # level of frustration experienced by user when using AB Search App
    frustration = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was frustrated by '
                                                                                                  'the search engine:')

    # level of excitement experienced by user when using AB Search App
    excitement = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was excited while'
                                                                                                 'using the search'
                                                                                                 ' engine:')

    # level of indifference experienced by user when using AB Search App
    indifference = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was indifferent '
                                                                                                   'to the search '
                                                                                                   'engine:')

   # level of confusion experienced by user when using AB Search App
    confusion = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was confused by the'
                                                                                                ' search engine:')

    # level of anxiety experienced by user when using AB Search App
    anxiety = forms.ChoiceField(widget=forms.RadioSelect(), choices=EXPERIENCE_CHOICES, label='I was anxious when '
                                                                                              'using the search '
                                                                                              'engine:')

    # any additional comments the user wishes to add about their experience of the AB Search App
    comment = forms.CharField(widget=forms.Textarea, label='Please add any other comments you may have about '
                                                           'Slowsearch:')

    class Meta:
        model = Experience
        exclude= ('user',)