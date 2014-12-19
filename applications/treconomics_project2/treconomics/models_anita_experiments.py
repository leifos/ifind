__author__ = 'leif'
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, CheckboxInput, Textarea
from models_experiments import clean_to_zero


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


ABILITY_CHOICES = ( (1,'Novice'), (2,''), (3,''), (4,''),(5,''),(6,''), (7,'Expert')  )


class AnitaDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0,help_text="Please provide your age (in years).")
    #sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    work = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="")
    search_freq = models.CharField(max_length=30, default="")
    search_ability = models.CharField(max_length=30, default="")

    def __unicode__(self):
        return self.user.username

class AnitaDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value = 100, min_value=0, required=False)
    #sex = forms.CharField(max_length=1, widget=forms.Select(choices=SEX_CHOICES), label="Please indicate your sex.", required=False)
    status =forms.CharField(widget=forms.TextInput( attrs={'size':'60', 'class':'inputText'}), label="What is your status at UNC?", required=False)
    work =forms.CharField(widget=forms.TextInput( attrs={'size':'60', 'class':'inputText'}), label="What is your major? What is your occupation?", required=False)
    search_freq = forms.CharField( widget=forms.TextInput( attrs={'size':'5', 'class':'inputText'}), label="How many times per week do you conduct searches for information?", required=False)

    search_ability  = forms.ChoiceField(widget=RadioSelect, choices = ABILITY_CHOICES, label="How would you rate your onine search ability?", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
            print "clean age"
        return cleaned_data

    class Meta:
        model = AnitaDemographicsSurvey
        exclude = ('user',)



LIKERT_CHOICES = ( (1,'Strongly Disagree'), (2,''), (3,''), (4,''),(5,''),(6,''), (7,'Strongly Agree')  )

class AnitaPreTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_interested  = models.IntegerField(default=0)
    apt_know  = models.IntegerField(default=0)
    apt_clear_what  = models.IntegerField(default=0)
    apt_info_diff  = models.IntegerField(default=0)
    apt_sys_diff  = models.IntegerField(default=0)
    apt_clear_how  = models.IntegerField(default=0)
    apt_clear_steps  = models.IntegerField(default=0)
    apt_difficult_finish  = models.IntegerField(default=0)
    apt_task_diff  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username




class AnitaPreTaskSurveyForm(ModelForm):
    apt_interested = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I am interested in this topic.", required=False)
    apt_know = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I know a lot about this topic.", required=False)
    apt_clear_what = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="It is clear what information I need to complete the task.", required=False)
    apt_info_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I think it wil be difficult to find relevant items for this task.", required=False)
    apt_sys_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I think it will be difficult to search for information using this system.", required=False)
    apt_clear_how = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="It is clear how much information I need to complete the task.", required=False)
    apt_clear_steps = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="It is clear which steps I need to take to complete this task.", required=False)
    apt_difficult_finish = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I think it will be difficult to determine when I have enough information to finish the task.", required=False)
    apt_task_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="Overall, I think this will be a difficult task.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPreTaskSurvey
        exclude = ('user','task_id','topic_num')


class AnitaPostTask1Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_satisfied_amount  = models.IntegerField(default=0)
    apt_satisfied_steps  = models.IntegerField(default=0)
    apt_work_fast  = models.IntegerField(default=0)
    apt_difficult_enough  = models.IntegerField(default=0)
    apt_time_pressure  = models.IntegerField(default=0)
    apt_search_diff  = models.IntegerField(default=0)
    apt_hurried  = models.IntegerField(default=0)
    apt_satisfied_systems  = models.IntegerField(default=0)
    apt_doing_well  = models.IntegerField(default=0)
    apt_found_enough  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask1SurveyForm(ModelForm):
    apt_satisfied_amount = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I am satisfied with the amount of information I found for the search topic.", required=False)
    apt_satisfied_steps = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I am satisfied with the steps I took to find information about the search topic.", required=False)
    apt_work_fast = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I needed to work fast to complete this task.", required=False)
    apt_difficult_enough = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I thought it was difficult to determine when I had enough information to finish the task.", required=False)
    apt_time_pressure = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I felt time pressure when completing this task.", required=False)
    apt_search_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I thought it was difficult to search for information on this topic.", required=False)
    apt_hurried = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I felt hurried or rushed when completing this task.", required=False)
    apt_satisfied_systems = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I am satisfied with how the system performed for this task.", required=False)
    apt_doing_well = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="While I was working on this task, I thought about how well I was doing on the task.", required=False)
    apt_found_enough  = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I found enough information about the search topic.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask1Survey
        exclude = ('user','task_id','topic_num')


#
class AnitaPostTask2Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_accurate  = models.IntegerField(default=0)
    apt_quick_results  = models.IntegerField(default=0)
    apt_more_info  = models.IntegerField(default=0)
    apt_time_left  = models.IntegerField(default=0)
    apt_quick_task  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask2SurveyForm(ModelForm):
    apt_accurate = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="It was important to me to complete this task accurately.", required=False)
    apt_quick_results = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="The system retrieved and displayed search results pages quickly.", required=False)
    apt_more_info = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="While I was working on this task, I thought about how much information I had already found and how much more I still needed.", required=False)
    apt_time_left = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="While I was working on this task, I thought about how much time I had left on the task. ", required=False)
    apt_quick_task = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="It was important to me to complete this task quickly.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask2Survey
        exclude = ('user','task_id','topic_num')


#
class AnitaPostTask3Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_system_relevance  = models.IntegerField(default=0)
    apt_system_download  = models.IntegerField(default=0)
    apt_finding_diff  = models.IntegerField(default=0)
    apt_all_info = models.IntegerField(default=0)
    apt_task_diff  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask3SurveyForm(ModelForm):
    apt_system_relevance = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="This system provided me with a great deal of relevant information.", required=False)
    apt_system_download = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="The system displayed the individual news articles quickly.", required=False)
    apt_finding_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I thought it was difficult to find relevant information on this topic.", required=False)
    apt_all_info = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I found all of the information about the search topic in the search system.", required=False)
    apt_task_diff = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="Overall, I thought this was a difficult task.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask3Survey
        exclude = ('user','task_id','topic_num')



class AnitaExit1Survey(models.Model):
    user = models.ForeignKey(User)
    ae_use_freq  = models.IntegerField(default=0)
    ae_complex  = models.IntegerField(default=0)
    ae_easy  = models.IntegerField(default=0)
    ae_integrated = models.IntegerField(default=0)
    ae_inconsistent  = models.IntegerField(default=0)
    ae_learn_quickly  = models.IntegerField(default=0)
    ae_cumbersome = models.IntegerField(default=0)
    ae_confident  = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class AnitaExit1SurveyForm(ModelForm):
    ae_use_freq = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I think that I would like to use this system frequently.", required=False)
    ae_complex = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I found the system unnecessarily complex.", required=False)
    ae_easy = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I thought the system was easy to use.", required=False)
    ae_integrated = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I found the various functions in the system to be well integrated.", required=False)
    ae_inconsistent = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I thought this system was too inconsistent.", required=False)
    ae_learn_quickly = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I would imagine that most people would learn to use this system very quickly.", required=False)
    ae_cumbersome = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I found the system very cumbersome to use.", required=False)
    ae_confident = forms.ChoiceField(widget=RadioSelect,  choices = LIKERT_CHOICES, label="I felt very confident using the system.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit1Survey
        exclude = ('user',)