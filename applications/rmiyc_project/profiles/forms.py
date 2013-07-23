from django.forms import ModelForm
from ifind.models.game_models import UserProfile



class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'school', 'country', 'city']
