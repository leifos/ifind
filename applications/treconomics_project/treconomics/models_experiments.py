__author__ = 'leif'

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
#import models_experiments
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, CheckboxInput, Textarea

SEX_CHOICES = ( ('N','Not Indicated'),
    ('M','Male'), ('F','Female')
)

YES_CHOICES = ( ('','Not Specified'),
    ('Y','Yes'),('N','No')
)

YES_NO_CHOICES = (
    ('Y','Yes'),('N','No')
)

STANDING_CHOICES = ( ('','Not Specified'),
    ('Freshman','Freshman'),('Sophomore','Sophomore'),('Junior','Junior'),('Senior','Senior') 
)

YEAR_CHOICES = ( ('','Not Specified'),
    ('1','First Year'), ('2','Second Year'), ('3','Third Year'), ('4','Fourth Year') ,('5','Fifth Year')  ,('6','Completed')
)


class UKDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0,help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1,default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_undergrad_year = models.CharField(max_length=1,default="")

    def __unicode__(self):
        return self.user.username

class UKDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value = 100, min_value=0, required=False)
    sex = forms.CharField(max_length=1, widget=forms.Select(choices=SEX_CHOICES), label="Please indicate your sex.", required=False)
    education_undergrad =forms.CharField( widget=forms.Select(choices=YES_CHOICES), label="Are you undertaking, or have you obtained, an undergraduate degree?", required=False)
    education_undergrad_major = forms.CharField(widget=forms.TextInput( attrs={'size':'60', 'class':'inputText'}), label="If yes, what is/was your subject area?", required=False)
    education_undergrad_year = forms.CharField( widget=forms.Select(choices=YEAR_CHOICES), label="What year are you in?", required=False)
    
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
            print "clean age"
        return cleaned_data

    class Meta:
        model = UKDemographicsSurvey
        exclude = ('user',)

class USDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0,help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1,default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_standing = models.CharField(max_length=30, default="")

    def __unicode__(self):
        return self.user.username

class USDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value = 100, min_value=0, required=False)
    sex = forms.CharField(max_length=1, widget=forms.Select(choices=SEX_CHOICES), label="Please indicate your sex.", required=False)
    education_undergrad =forms.CharField( widget=forms.Select(choices=YES_CHOICES), label="Are you undertaking, or have you obtained, an undergraduate degree?", required=False)
    education_undergrad_major = forms.CharField(widget=forms.TextInput( attrs={'size':'60', 'class':'inputText'}), label="If yes, what is/was your subject area?", required=False)
    education_standing = forms.CharField( widget=forms.Select(choices=STANDING_CHOICES), label="What is your class standing?", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
            print "clean age"
        return cleaned_data

    class Meta:
        model = USDemographicsSurvey
        exclude = ('user',)



NASA_LOW_CHOICES = ( (1,'Very Low'), (2,''), (3,''), (4,''), (5,''), (6,''),  (7,'Very High') )
NASA_PERFECT_CHOICES = ( (1,'Perfect'), (2,''), (3,''), (4,''), (5,''), (6,''), (7,'Failure') )

class NasaSystemLoad(models.Model):
    user = models.ForeignKey(User)
    nasa_mental_demand = models.IntegerField(default=0)
    nasa_physical_demand = models.IntegerField(default=0)
    nasa_temporal = models.IntegerField(default=0)
    nasa_performance = models.IntegerField(default=0)
    nasa_effort = models.IntegerField(default=0)
    nasa_frustration = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


def clean_nasa_data(self):
    cleaned_data = self.cleaned_data
    if not cleaned_data.get("nasa_mental_demand"):
        cleaned_data["nasa_mental_demand"] = 0
    if not cleaned_data.get("nasa_temporal"):
        cleaned_data["nasa_temporal"] = 0
    if not cleaned_data.get("nasa_physical_demand"):
        cleaned_data["nasa_physical_demand"] = 0
    if not cleaned_data.get("nasa_performance"):
        cleaned_data["nasa_performance"] = 0
    if not cleaned_data.get("nasa_effort"):
        cleaned_data["nasa_effort"] = 0
    if not cleaned_data.get("nasa_frusration"):
        cleaned_data["nasa_frustration"] = 0
    return cleaned_data

def clean_to_zero(self):
    cleaned_data = self.cleaned_data
    for item in cleaned_data:
        if not cleaned_data[item]:
            cleaned_data[item] = 0
    return cleaned_data



class NasaSystemLoadForm(ModelForm):
    nasa_mental_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="MENTAL DEMAND: How mentally demanding was it to use this system to complete the search tasks?", required=False )
    nasa_physical_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="PHYSICAL DEMAND: How physically demanding was it to use this system to complete the search tasks?", required=False)
    nasa_temporal = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="TEMPORAL DEMAND: How hurried or rushed did you feel when using this system to complete the search tasks?", required=False)
    nasa_performance = forms.ChoiceField(widget=RadioSelect,  choices = NASA_PERFECT_CHOICES, label="PERFORMANCE: How successful were you using this system to complete the search tasks?", required=False)
    nasa_effort = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="EFFORT: How hard did you have to work to accomplish your level of performance with this system?", required=False)
    nasa_frustration = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="FRUSTRATION: How insecure, discouraged, irrtated, stressed, and annoyed were you while using this system?", required=False)

    def clean(self):
        return clean_nasa_data(self)

    class Meta:
        model = NasaSystemLoad
        exclude = ('user',)

class NasaQueryLoad(NasaSystemLoad):

    def __unicode__(self):
        return self.user.username

class NasaQueryLoadForm(ModelForm):
    nasa_mental_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="MENTAL DEMAND: How mentally demanding was it to query?", required=False)
    nasa_physical_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="PHYSICAL DEMAND: How physically demanding was it to query?", required=False)
    nasa_temporal = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="TERMPORAL DEMAND: How hurried or rushed did you feel when querying?", required=False)
    nasa_performance = forms.ChoiceField(widget=RadioSelect,  choices = NASA_PERFECT_CHOICES, label="PERFORMANCE: How successful were your queries?", required=False)
    nasa_effort = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="EFFORT: How hard did you have to work to query?", required=False)
    nasa_frustration = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="FRUSTRATION: How insecure, discouraged, irrtated, stressed, and annoyed were you while issuing queries?", required=False)

    def clean(self):
        return clean_nasa_data(self)

    class Meta:
        model = NasaQueryLoad
        exclude = ('user',)



class NasaNavigationLoad(NasaSystemLoad):

    def __unicode__(self):
        return self.user.username

class NasaNavigationLoadForm(ModelForm):
    nasa_mental_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="MENTAL DEMAND: How mentally demanding was it to navigate through the search results?", required=False)
    nasa_physical_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="PHYSICAL DEMAND: How physically demanding was it to navigate through the search results?", required=False)
    nasa_temporal = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="TERMPORAL DEMAND: How hurried or rushed did you feel when navigating through the search resutls?", required=False)
    nasa_performance = forms.ChoiceField(widget=RadioSelect,  choices = NASA_PERFECT_CHOICES, label="PERFORMANCE: How successful was your navigation through the search results?", required=False)
    nasa_effort = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="EFFORT: How hard did you have to work to navigate through the search results?", required=False)
    nasa_frustration = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="FRUSTRATION: How insecure, discouraged, irrtated, stressed, and annoyed were you while navigating through the search results?", required=False)

    def clean(self):
        return clean_nasa_data(self)

    class Meta:
        model = NasaNavigationLoad
        exclude = ('user',)


class NasaAssessmentLoad(NasaSystemLoad):

    def __unicode__(self):
        return self.user.username

class NasaAssessmentLoadForm(ModelForm):
    nasa_mental_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="MENTAL DEMAND: How mentally demanding was it to assess and judge documents for relevance?", required=False)
    nasa_physical_demand = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="PHYSICAL DEMAND: How physically demanding was it to assess and judge documents for relevance?", required=False)
    nasa_temporal = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="TERMPORAL DEMAND: How hurried or rushed did you feel when assessing and judging documents for relevance?", required=False)
    nasa_performance = forms.ChoiceField(widget=RadioSelect,  choices = NASA_PERFECT_CHOICES, label="PERFORMANCE: How successful were you at assessing and judging documents for relevance?", required=False)
    nasa_effort = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="EFFORT: How hard did you have to work to assess and judge documents for relevance?", required=False)
    nasa_frustration = forms.ChoiceField(widget=RadioSelect,  choices = NASA_LOW_CHOICES, label="FRUSTRATION: How insecure, discouraged, irrtated, stressed, and annoyed were you while assessing and judgin documents for relevance?", required=False)

    def clean(self):
        return clean_nasa_data(self)

    class Meta:
        model = NasaAssessmentLoad
        exclude = ('user',)

MVP = ( ('M','Mental Demand'), ('P','Physical Demand') )
MVT = ( ('M','Mental Demand'), ('T','Temporal Demand') )
MVS = ( ('M','Mental Demand'), ('S','Performance') )
MVE = ( ('M','Mental Demand'), ('E','Effort') )
MVF = ( ('M','Mental Demand'), ('F','Frustration') )
PVT = ( ('P','Physical Demand'), ('T','Temporal Demand') )
PVS = ( ('P','Physical Demand'), ('S','Performance') )
PVE = ( ('P','Physical Demand'), ('E','Effort')  )
PVF = ( ('P','Physical Demand'), ('F','Frustration') )
TVS = ( ('T','Temporal Demand'), ('S','Performance') )
TVE = ( ('T','Temporal Demand'), ('E','Effort') )
TVF = ( ('T','Temporal Demand'), ('F','Frustration') )
SVE = ( ('S','Performance'), ('E','Effort') )
SVF = ( ('S','Performance'), ('E','Frustration') )
EVF = ( ('E','Effort'), ('E','Frustration') )

class NasaFactorCompare(models.Model):
    nasa_mental_physical = forms.CharField(max_length=1)
    nasa_mental_temporal = forms.CharField(max_length=1)
    nasa_mental_performance = forms.CharField(max_length=1)
    nasa_mental_effort = forms.CharField(max_length=1)
    nasa_mental_frustration = forms.CharField(max_length=1)
    nasa_physical_temporal = forms.CharField(max_length=1)
    nasa_physical_performance = forms.CharField(max_length=1)
    nasa_physical_effort = forms.CharField(max_length=1)
    nasa_physical_frustration = forms.CharField(max_length=1)
    nasa_temporal_performance = forms.CharField(max_length=1)
    nasa_temporal_effort = forms.CharField(max_length=1)
    nasa_temporal_frustration = forms.CharField(max_length=1)
    nasa_performance_effort = forms.CharField(max_length=1)
    nasa_performance_frustration = forms.CharField(max_length=1)
    nasa_effort_frustration = forms.CharField(max_length=1)

class NasaFactorCompareForm(ModelForm):
    nasa_mental_physical = forms.ChoiceField(widget=RadioSelect,  choices = MVP, label="", required=False)
    nasa_performance_frustration = forms.ChoiceField(widget=RadioSelect,  choices = SVF, label="", required=False)
    nasa_mental_temporal = forms.ChoiceField(widget=RadioSelect,  choices = MVT, label="", required=False)
    nasa_physical_effort = forms.ChoiceField(widget=RadioSelect,  choices = PVE, label="", required=False)
    nasa_temporal_performance = forms.ChoiceField(widget=RadioSelect,  choices = TVS, label="", required=False)
    nasa_mental_effort = forms.ChoiceField(widget=RadioSelect,  choices = MVE, label="", required=False)
    nasa_physical_frustration = forms.ChoiceField(widget=RadioSelect,  choices = PVF, label="", required=False)
    nasa_performance_effort = forms.ChoiceField(widget=RadioSelect,  choices = SVE, label="", required=False)
    nasa_temporal_effort = forms.ChoiceField(widget=RadioSelect,  choices = TVE, label="", required=False)
    nasa_mental_frustration = forms.ChoiceField(widget=RadioSelect,  choices = MVF, label="", required=False)
    nasa_physical_performance = forms.ChoiceField(widget=RadioSelect,  choices = PVS, label="", required=False)
    nasa_physical_temporal = forms.ChoiceField(widget=RadioSelect,  choices = PVT, label="", required=False)
    nasa_temporal_frustration = forms.ChoiceField(widget=RadioSelect,  choices = TVF, label="", required=False)
    nasa_mental_performance = forms.ChoiceField(widget=RadioSelect,  choices = MVS, label="", required=False)
    nasa_effort_frustration = forms.ChoiceField(widget=RadioSelect,  choices = EVF, label="", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        for item in cleaned_data:
            if not cleaned_data[item]:
                cleaned_data[item] = 'VVV'
                return cleaned_data

    class Meta:
        model = NasaFactorCompare
        exclude = ('user',)

EFF_CONFIDENT_CHOICES = ( (1,'Totally Unconfident'), (2,''), (3,''), (4,''), (5,'') , (6,''), (7,''), (8,''), (9,''), (10,'Totally Confident')  )

class SearchEfficacy(models.Model):
    user = models.ForeignKey(User)
    efficacy_identify_requirements = models.IntegerField(default=0)
    efficacy_develop_queries = models.IntegerField(default=0)
    efficacy_special_syntax = models.IntegerField(default=0)
    efficacy_evaluate_list = models.IntegerField(default=0)
    efficacy_many_relevant = models.IntegerField(default=0)
    efficacy_enough_results = models.IntegerField(default=0)
    efficacy_like_a_pro = models.IntegerField(default=0)
    efficacy_few_irrelevant = models.IntegerField(default=0)
    efficacy_structure_time = models.IntegerField(default=0)
    efficacy_focus_query = models.IntegerField(default=0)
    efficacy_distinguish_relevant = models.IntegerField(default=0)
    efficacy_competent_effective = models.IntegerField(default=0)
    efficacy_little_difficulty = models.IntegerField(default=0)
    efficacy_allocated_time = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class SearchEfficacyForm(ModelForm):
    efficacy_identify_requirements = forms.ChoiceField(widget=RadioSelect(attrs={'class':'special'}),  choices = EFF_CONFIDENT_CHOICES, label="Identify the major requirements of a search task.", required=False)
    efficacy_develop_queries = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Correctly develop search queries to reflect the requirements.", required=False)
    efficacy_special_syntax = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Use special syntax in advanced searching (e.g., AND, OR, NOT).", required=False)
    efficacy_evaluate_list = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Evaluate the resulting list to monitor the success of my approach.", required=False)
    efficacy_many_relevant = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Develop a search query which will retrieved a large number of appropriate results.", required=False)
    efficacy_enough_results = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Find an adequate number of results.", required=False)
    efficacy_like_a_pro = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Find results similar in quality to those obtained by a professional searcher.", required=False)
    efficacy_few_irrelevant = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Devise a query which will result in a very small percentage of irrelevant itesm on my list.", required=False)
    efficacy_structure_time = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Efficiently structure my time to complete the task.", required=False)
    efficacy_focus_query = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Develop a focused search query that will retrieved a small number of appropriate results.", required=False)
    efficacy_distinguish_relevant = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Distinguish between relevant and irrelevant results.", required=False)
    efficacy_competent_effective = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Complete the search competently and effectively.", required=False)
    efficacy_little_difficulty = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Complete the individual steps of the search with little difficulty.", required=False)
    efficacy_allocated_time = forms.ChoiceField(widget=RadioSelect,  choices = EFF_CONFIDENT_CHOICES, label="Structure my time effectively so that I will finish the search in the allocated time.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SearchEfficacy
        exclude = ('user',)

TOPIC_NOTHING_CHOICES = ( (1,'Nothing'), (2,''), (3,''), (4,''), (5,'I Know Details')  )
TOPIC_NOTATALL_CHOICES = ( (1,'Not at all'), (2,''), (3,''), (4,''), (5,'Very Much')  )
TOPIC_NEVER_CHOICES = ( (1,'Never'), (2,''), (3,''), (4,''), (5,'Very Often')  )
TOPIC_EASY_CHOICES = ( (1,'Very Easy'), (2,''), (3,''), (4,''), (5,'Very Difficult')  )
TOPIC_NOTGOOD_CHOICES = ( (1,'Not Good'), (2,''), (3,''), (4,''), (5,'Very Good')  )
TOPIC_UNSUCCESSFUL_CHOICES = ( (1,'Unsuccessful'), (2,''), (3,''), (4,''), (5,'Successful')  )
TOPIC_FEW_CHOICES = ( (1,'A few of them'), (2,''), (3,''), (4,''), (5,'All of them')  )

class PreTaskTopicKnowledgeSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    topic_knowledge  = models.IntegerField(default=0, help_text="How much do you know about this topic?")
    topic_relevance  = models.IntegerField(default=0)
    topic_interest  = models.IntegerField(default=0)
    topic_searched  = models.IntegerField(default=0)
    topic_difficulty  = models.IntegerField(default=0)


    def __unicode__(self):
        return self.user.username

class PreTaskTopicKnowledgeSurveyForm(ModelForm):
    topic_knowledge = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NOTHING_CHOICES, label="How much do you know about this topic?", required=False)
    topic_relevance = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NOTATALL_CHOICES, label="How relevant is this topic to your life?", required=False)
    topic_interest = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NOTATALL_CHOICES, label="How interested are you to learn more about this topic?", required=False)
    topic_searched = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NEVER_CHOICES, label="Have you ever searched for information related to this topic?", required=False)
    topic_difficulty = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_EASY_CHOICES, label="How difficult do you think it will be to search for information about this topic?", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PreTaskTopicKnowledgeSurvey
        exclude = ('user','task_id','topic_num')

class PostTaskTopicRatingSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    relevance_difficulty  = models.IntegerField(default=0)
    relevance_skill  = models.IntegerField(default=0)
    relevance_system  = models.IntegerField(default=0)
    relevance_success  = models.IntegerField(default=0)
    relevance_number  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class PostTaskTopicRatingSurveyForm(ModelForm):
    relevance_difficulty = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_EASY_CHOICES, label="How difficult was it to find relevant documents?", required=False)
    relevance_skill = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NOTGOOD_CHOICES, label="How would you rate your skill and ability at finding relevant documents?", required=False)
    relevance_system = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_NOTGOOD_CHOICES, label="How would you rate the system's ability at retrieving relevant documents?", required=False)
    relevance_success = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_UNSUCCESSFUL_CHOICES, label="How successful was your search?", required=False)
    relevance_number = forms.ChoiceField(widget=RadioSelect,  choices = TOPIC_FEW_CHOICES, label="How many of the relevant documents do you think you found?", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostTaskTopicRatingSurvey
        exclude = ('user','task_id','topic_num')


class ShortStressSurvey(models.Model):
    user = models.ForeignKey(User)
    stress_confident  = models.IntegerField(default=0)
    stress_alert  = models.IntegerField(default=0)
    stress_others  = models.IntegerField(default=0)
    stress_figure  = models.IntegerField(default=0)
    stress_angry  = models.IntegerField(default=0)
    stress_proficient  = models.IntegerField(default=0)
    stress_irritated  = models.IntegerField(default=0)
    stress_grouchy  = models.IntegerField(default=0)
    stress_reflecting  = models.IntegerField(default=0)
    stress_concerned  = models.IntegerField(default=0)
    stress_committed  = models.IntegerField(default=0)
    stress_annoyed = models.IntegerField(default=0)
    stress_impatient = models.IntegerField(default=0)
    stress_self_conscious  = models.IntegerField(default=0)
    stress_daydreaming = models.IntegerField(default=0)
    stress_control = models.IntegerField(default=0)
    stress_sad = models.IntegerField(default=0)
    stress_active = models.IntegerField(default=0)
    stress_motivated = models.IntegerField(default=0)
    stress_dissatisfied = models.IntegerField(default=0)
    stress_performance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

STRESS_CHOICES = ( (1,'Not at all'), (2,''), (3,''), (4,''), (5,'Extremely')  )


class ShortStressSurveyForm(ModelForm):
    stress_confident = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt confident in my abilities.", required=False)
    stress_alert = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt alert while I was completing these tasks.", required=False)
    stress_others = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I thought about how others have done on these tasks.", required=False)
    stress_figure = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I'm trying to figure myself out.", required=False)
    stress_angry = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt angry while I was completing these tasks.", required=False)
    stress_proficient = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I expected to perform proficiently on these tasks.", required=False)
    stress_irritated = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt irritated while I was completing these tasks.", required=False)
    stress_grouchy = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt grouchy while I was completing these tasks.", required=False)
    stress_reflecting = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I'm reflecting about myself.", required=False)
    stress_concerned = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt concerned about the impression I was making.", required=False)
    stress_committed = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt committed to succeed to these tasks.", required=False)
    stress_annoyed = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt annoyed while I was completing these tasks.", required=False)
    stress_impatient = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt impatient while I was completing these tasks.", required=False)
    stress_self_conscious  = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I feel self-conscious.", required=False)
    stress_daydreaming = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I'm daydreaming about myself.", required=False)
    stress_control = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt in control of things.", required=False)
    stress_sad = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt sad while I was completing these tasks.", required=False)
    stress_active = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt active while I was completing these tasks.", required=False)
    stress_motivated = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt motivated to do these tasks.", required=False)
    stress_dissatisfied = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt dissatisfied while I was completing these tasks.", required=False)
    stress_performance = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I was committed to attaining my performance goals for these search tasks.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = ShortStressSurvey
        exclude = ('user')


class ConceptListingSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    when = models.CharField(max_length=4, default='')
    concepts  = models.TextField(default=0)
    paragraph  = models.TextField(default=0)

    def __unicode__(self):
        return self.user.username


class ConceptListingSurveyForm(ModelForm):
    concepts = forms.CharField(widget=Textarea, label="Please list any concepts that come to mind for this topic. You can list any concepts that you feel are relevant or important.", required=False)
    paragraph = forms.CharField(widget=Textarea, label="Imagine you would like to tell someone you know about what you have learned about this topic. Please compose a paragraph describing the topic and what you learnt about the topic. ", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = ConceptListingSurvey
        exclude = ('user','task_id','topic_num','when')


class PostConceptListingSurvey(ConceptListingSurvey):

    def __unicode__(self):
        return self.user.username

class PostConceptListingSurveyForm(ConceptListingSurveyForm):

    class Meta:
        model = PostConceptListingSurvey
        exclude = ('user','task_id','topic_num')
        
        
        
#
class ModifiedStressSurvey(models.Model):
    user = models.ForeignKey(User)
    stress_confident  = models.IntegerField(default=0)
    stress_alert  = models.IntegerField(default=0)
    stress_irritated  = models.IntegerField(default=0)
    stress_others  = models.IntegerField(default=0)
    stress_angry  = models.IntegerField(default=0)
    stress_proficient  = models.IntegerField(default=0)
    stress_grouchy  = models.IntegerField(default=0)
    stress_concerned  = models.IntegerField(default=0)
    stress_committed  = models.IntegerField(default=0)
    stress_annoyed = models.IntegerField(default=0)
    stress_impatient = models.IntegerField(default=0)
    stress_self_conscious  = models.IntegerField(default=0)
    stress_control = models.IntegerField(default=0)
    stress_sad = models.IntegerField(default=0)
    stress_active = models.IntegerField(default=0)
    stress_motivated = models.IntegerField(default=0)
    stress_dissatisfied = models.IntegerField(default=0)
    stress_performance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username



class ModifiedStressSurveyForm(ModelForm):
    stress_confident = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt confident in my abilities.", required=False)
    stress_alert = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt alert while I was completing these tasks.", required=False)
    stress_irritated = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt irritated while I was completing these tasks.", required=False)
    stress_others = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I thought about how others have done on these tasks.", required=False)
    stress_angry = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt angry while I was completing these tasks.", required=False)
    stress_proficient = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I expected to perform proficiently on these tasks.", required=False)
    stress_grouchy = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt grouchy while I was completing these tasks.", required=False)
    stress_concerned = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt concerned about the impression I was making.", required=False)
    stress_committed = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt committed to succeed to these tasks.", required=False)
    stress_annoyed = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt annoyed while I was completing these tasks.", required=False)
    stress_impatient = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt impatient while I was completing these tasks.", required=False)
    stress_self_conscious  = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt self-conscious.", required=False)
    stress_control = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt in control of things.", required=False)
    stress_sad = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt sad while I was completing these tasks.", required=False)
    stress_active = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt active while I was completing these tasks.", required=False)
    stress_motivated = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt motivated to do these tasks.", required=False)
    stress_dissatisfied = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I felt dissatisfied while I was completing these tasks.", required=False)
    stress_performance = forms.ChoiceField(widget=RadioSelect,  choices = STRESS_CHOICES, label="I was committed to attaining my performance goals for these search tasks.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = ModifiedStressSurvey
        exclude = ('user')