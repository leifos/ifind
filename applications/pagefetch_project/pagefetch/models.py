from django.contrib.auth.models import User#, UserProfile
import ifind.models.game_models

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
#post_save.connect(create_user_profile, sender=User)
