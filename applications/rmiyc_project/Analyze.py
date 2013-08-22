

def get_findability_score():
    from ifind.models.game_models import Page ,Category, UserProfile
    pages = Page.objects.all()
    f = open('findability.txt', 'a')
    for p in pages:
        if p.no_of_queries_issued != 0:
            finability = float(p.no_times_retrieved) / float(p.no_of_queries_issued)
            url = p.url
            f.write('%f,%s\n' % (finability, url))


def calculate_game_played_no():
    from ifind.models.game_models import Page ,Category, UserProfile
    profiles = UserProfile.objects.all()
    countries_list ={}
    for p in profiles:
        if p.country:
            cntry = unicode(p.country.name)
            if cntry not in countries_list:
                countries_list[cntry] = 1
            else:
                countries_list[cntry] += 1
    for key in countries_list:
        print key
        print countries_list[key]


def get_players_ages():
    from ifind.models.game_models import Page ,Category, UserProfile
    profiles = UserProfile.objects.all()
    age_list ={}
    for p in profiles:
        if p.age:
            if p.age not in age_list:
                age_list[p.age] = 1
            else:
                age_list[p.age] += 1
    for key in age_list:
        print key
        print age_list[key]




get_players_ages()