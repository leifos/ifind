from django import forms
from gold_digger.models import UserProfile, ScanningEquipment, Vehicle, DiggingEquipment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat password")

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    one = ScanningEquipment.objects.get(pk=1)
    two = DiggingEquipment.objects.get(pk=1)
    three = Vehicle.objects.get(pk=1)

    equipment = forms.ModelChoiceField(queryset=ScanningEquipment.objects.all(), widget=forms.HiddenInput(), initial=one.pk)
    vehicle = forms.ModelChoiceField(queryset=DiggingEquipment.objects.all(), widget=forms.HiddenInput(), initial=two.pk)
    tool = forms.ModelChoiceField(queryset=Vehicle.objects.all(), widget=forms.HiddenInput(), initial=three.pk)

    class Meta:
        model = UserProfile
        fields = ('picture', 'location')