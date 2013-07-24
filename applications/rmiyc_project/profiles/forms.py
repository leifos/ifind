from django.forms import ModelForm
from ifind.models.game_models import UserProfile, User



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'age', 'gender', 'school', 'city', 'country']
