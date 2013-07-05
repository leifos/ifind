__author__ = 'arazzouk'
from ifind.models.game_models import Achievement


def main():
    Achievement(name='Tenderfoot', level_of_achievement=0, desc='', badge_icon=None, xp_earned =0).save()
    Achievement(name='Vaquero', level_of_achievement=5000, desc='', badge_icon=None, xp_earned =0).save()
    Achievement(name='Wrangler', level_of_achievement=25000, desc='', badge_icon=None, xp_earned =0).save()
    Achievement(name='Caballero', level_of_achievement=100000, desc='', badge_icon=None, xp_earned =0).save()
    Achievement(name='Gunfighter', level_of_achievement=500000, desc='', badge_icon=None, xp_earned =0).save()


if __name__ == '__main__':
    main()
