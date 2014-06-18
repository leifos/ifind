from django import forms
from badsearch.models import UserProfile, Demographics
from django.contrib.auth.models import User

GENDER_CHOICES = (('N', 'Not Indicated'),
                  ('M', 'Male'), ('F', 'Female'))

YES_CHOICES = (('', 'Not Indicated'),
               ('Y', 'Yes'), ('N', 'No'))

YEAR_CHOICES = (('', 'Not Specified'),
                ('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'),
                ('5', 'Fifth Year'), ('6', 'Completed'))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class DemographicsForm(forms.ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value=100, min_value=0, required=False)
    sex = forms.CharField(max_length=1, widget=forms.Select(choices=GENDER_CHOICES), label="Please indicate your sex.",
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
            cleaned_data["age"] = 18
            print "clean age"
        return cleaned_data

    class Meta:
        model = Demographics
        exclude = ('user',)


class ValidationForm(forms.Form):
    terms = forms.BooleanField(required=True, initial=False,
                               label="I have read and agree to the above terms and conditions",
                               error_messages={'required': 'You must accept the terms and conditions'}, )