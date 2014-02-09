from django.forms import ModelForm
from ifind.models.game_models import UserProfile, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'city', 'country']  # profile_pic + school
