__author__ = 'leif'
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect

from survey.forms import clean_to_zero


SEX_CHOICES = ( ('N', 'Not Indicated'),
                ('M', 'Male'), ('F', 'Female')
)

YES_CHOICES = ( ('', 'Not Specified'),
                ('Y', 'Yes'), ('N', 'No')
)

YES_NO_CHOICES = (
    ('Y', 'Yes'), ('N', 'No')
)

STANDING_CHOICES = ( ('', 'Not Specified'),
                     ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior')
)

YEAR_CHOICES = ( ('', 'Not Specified'),
                 ('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'),
                 ('5', 'Fifth Year'), ('6', 'Completed')
)

ABILITY_CHOICES = ( ('0', 'Not Specified'), ('1', '1 - Novice'), ('2', '2'), ('3', '3'),
                    ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7 - Expert')  )


class AnitaConsent(models.Model):
    user = models.ForeignKey(User)
    agreed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class AnitaConsentForm(ModelForm):
    agreed = forms.BooleanField(label="Do you consent to participate in the study?", required=True)

    def clean(self):
        cleaned_data = super(AnitaConsentForm, self).clean()
        agreed = cleaned_data.get("agreed")
        if not agreed:
            raise forms.ValidationError("Consent not given.")
        return cleaned_data

    class Meta:
        model = AnitaConsent
        exclude = ('user',)


class AnitaDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    # sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    status = models.CharField(max_length=100, default="")
    work = models.CharField(max_length=100, default="")
    level = models.CharField(max_length=3, default="")
    search_freq = models.IntegerField(default=0,
                                      help_text="How many times per week do you conduct searches for information (please enter a whole number)?")
    search_ability = models.CharField(default="", max_length=1)

    def __unicode__(self):
        return self.user.username


ED_CHOICES = ( ('', 'Not Specified'),
               ('GED', 'High School or GED'), ('ASS', "Associate's"), ('BCA', "Bachelor's"), ('MAS', "Master's"),
               ('PHD', "Doctorate")
)

STATUS_CHOICES = ( ('', 'Not Specified'),
                   ('staff', 'Staff'), ('undergrad', 'Undergraduate Student'), ('postgrad', 'Graduate Student')
)


class AnitaDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).", max_value=100, min_value=0, required=False)
    # sex = forms.CharField(max_length=1, widget=forms.Select(choices=SEX_CHOICES), label="Please indicate your sex.", required=False)
    status = forms.CharField(widget=forms.Select(choices=STATUS_CHOICES), label="What is your status at UNC?",
                             required=False)
    work = forms.CharField(widget=forms.TextInput(attrs={'size': '60', 'class': 'inputText'}),
                           label="Please provide your occupation/major:", required=False)
    level = forms.CharField(max_length=3, widget=forms.Select(choices=ED_CHOICES),
                            label="Please indicate the highest degree you've earned:", required=False)
    search_freq = forms.IntegerField(
        label="How many times per week do you conduct searches for information (please enter a whole number)?",
        max_value=10000, min_value=0, required=False)
    search_ability = forms.CharField(max_length=1, widget=forms.Select(choices=ABILITY_CHOICES),
                                     label="How would you rate your online search ability?", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0

        if not cleaned_data.get("search_freq"):
            cleaned_data["search_freq"] = 0

        return cleaned_data

    class Meta:
        model = AnitaDemographicsSurvey
        exclude = ('user',)


LIKERT_CHOICES = ( (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Strongly Agree')  )


class AnitaPreTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_interested = models.IntegerField(default=0)
    apt_know = models.IntegerField(default=0)
    apt_clear_what = models.IntegerField(default=0)
    apt_info_diff = models.IntegerField(default=0)
    apt_sys_diff = models.IntegerField(default=0)
    apt_clear_how = models.IntegerField(default=0)
    apt_clear_steps = models.IntegerField(default=0)
    apt_difficult_finish = models.IntegerField(default=0)
    apt_task_diff = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPreTaskSurveyForm(ModelForm):
    apt_interested = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                       label="I am interested in this topic.", required=False)
    apt_know = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES, label="I know a lot about this topic.",
                                 required=False)
    apt_clear_what = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                       label="It is clear what information I need to complete the task.",
                                       required=False)
    apt_info_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I think it will be difficult to find relevant items for this task.",
                                      required=False)
    apt_sys_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                     label="I think it will be difficult to search for information using this system.",
                                     required=False)
    apt_clear_how = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="It is clear how much information I need to complete the task.",
                                      required=False)
    apt_clear_steps = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                        label="It is clear which steps I need to take to complete this task.",
                                        required=False)
    apt_difficult_finish = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                             label="I think it will be difficult to determine when I have enough information to finish the task.",
                                             required=False)
    apt_task_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="Overall, I think this will be a difficult task.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPreTaskSurvey
        exclude = ('user', 'task_id', 'topic_num')


class AnitaPostTask0Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_satisfied_amount = models.IntegerField(default=0)
    apt_satisfied_steps = models.IntegerField(default=0)
    apt_work_fast = models.IntegerField(default=0)
    apt_difficult_enough = models.IntegerField(default=0)
    apt_time_pressure = models.IntegerField(default=0)


    def __unicode__(self):
        return self.user.username


class AnitaPostTask0SurveyForm(ModelForm):
    apt_satisfied_amount = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                             label="I am satisfied with the amount of information I found for the search topic.",
                                             required=False)
    apt_satisfied_steps = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                            label="I am satisfied with the steps I took to find information about the search topic.",
                                            required=False)
    apt_work_fast = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I needed to work fast to complete this task.", required=False)
    apt_difficult_enough = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                             label="I thought it was difficult to determine when I had enough information to finish the task.",
                                             required=False)
    apt_time_pressure = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                          label="I felt time pressure when completing this task.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask0Survey
        exclude = ('user', 'task_id', 'topic_num')


class AnitaPostTask1Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_search_diff = models.IntegerField(default=0)
    apt_hurried = models.IntegerField(default=0)
    apt_satisfied_systems = models.IntegerField(default=0)
    apt_doing_well = models.IntegerField(default=0)
    apt_found_enough = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask1SurveyForm(ModelForm):
    apt_search_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                        label="I thought it was difficult to search for information on this topic.",
                                        required=False)
    apt_hurried = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                    label="I felt hurried or rushed when completing this task.", required=False)
    apt_satisfied_systems = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                              label="I am satisfied with how the system performed for this task.",
                                              required=False)
    apt_doing_well = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                       label="While I was working on this task, I thought about how well I was doing on the task.",
                                       required=False)
    apt_found_enough = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                         label="I found enough information about the search topic.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask1Survey
        exclude = ('user', 'task_id', 'topic_num')


#
class AnitaPostTask2Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_accurate = models.IntegerField(default=0)
    apt_quick_results = models.IntegerField(default=0)
    apt_more_info = models.IntegerField(default=0)
    apt_time_left = models.IntegerField(default=0)
    apt_quick_task = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask2SurveyForm(ModelForm):
    apt_accurate = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                     label="It was important to me to complete this task accurately.", required=False)
    apt_quick_results = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                          label="The system retrieved and displayed search results pages quickly.",
                                          required=False)
    apt_more_info = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I thought about how much information I had already found and how much more I still needed.",
                                      required=False)
    apt_time_left = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I thought about how much time I had left on the task. ", required=False)
    apt_quick_task = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                       label="It was important to me to complete this task quickly.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask2Survey
        exclude = ('user', 'task_id', 'topic_num')


#
class AnitaPostTask3Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_system_relevance = models.IntegerField(default=0)
    apt_system_download = models.IntegerField(default=0)
    apt_finding_diff = models.IntegerField(default=0)
    apt_all_info = models.IntegerField(default=0)
    apt_task_diff = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask3SurveyForm(ModelForm):
    apt_system_relevance = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                             label="This system provided me with a great deal of relevant information.",
                                             required=False)
    apt_system_download = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                            label="The system displayed the individual news articles quickly.",
                                            required=False)
    apt_finding_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                         label="I thought it was difficult to find relevant information on this topic.",
                                         required=False)
    apt_all_info = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                     label="I found all of the information about the search topic in the search system.",
                                     required=False)
    apt_task_diff = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="Overall, I thought this was a difficult task.", required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask3Survey
        exclude = ('user', 'task_id', 'topic_num')


class AnitaExit1Survey(models.Model):
    user = models.ForeignKey(User)
    ae_use_freq = models.IntegerField(default=0)
    ae_complex = models.IntegerField(default=0)
    ae_easy = models.IntegerField(default=0)
    ae_integrated = models.IntegerField(default=0)
    ae_inconsistent = models.IntegerField(default=0)
    ae_learn_quickly = models.IntegerField(default=0)
    ae_cumbersome = models.IntegerField(default=0)
    ae_confident = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaExit1SurveyForm(ModelForm):
    ae_use_freq = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                    label="I think that I would like to use this system frequently.", required=False)
    ae_complex = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                   label="I found the system unnecessarily complex.", required=False)
    ae_easy = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                label="I thought the system was easy to use.", required=False)
    ae_integrated = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I found the various functions in the system to be well integrated.",
                                      required=False)
    ae_inconsistent = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                        label="I thought this system was too inconsistent.", required=False)
    ae_learn_quickly = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                         label="I would imagine that most people would learn to use this system very quickly.",
                                         required=False)
    ae_cumbersome = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                      label="I found the system very cumbersome to use.", required=False)
    ae_confident = forms.ChoiceField(widget=RadioSelect, choices=LIKERT_CHOICES,
                                     label="I felt very confident using the system.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit1Survey
        exclude = ('user',)


EXTENT_CHOICES = ( (1, 'Not at all'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Very much')  )


class AnitaExit2Survey(models.Model):
    user = models.ForeignKey(User)
    ae_time_extent = models.IntegerField(default=0)
    ae_time_reasonable = models.TextField(default="")
    ae_time_process = models.TextField(default="")
    ae_time_amount_found = models.TextField(default="")
    ae_time_amount_read = models.TextField(default="")
    ae_time_pressure_points = models.TextField(default="")

    def __unicode__(self):
        return self.user.username


class AnitaExit2SurveyForm(ModelForm):
    ae_time_extent = forms.ChoiceField(widget=RadioSelect, choices=EXTENT_CHOICES,
                                       label="To what extent did the amount of time you had to complete these task influence your performance?",
                                       required=False)
    ae_time_reasonable = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                         label="Do you think the time you had to complete these tasks was reasonable? Please explain.",
                                         required=False)
    ae_time_process = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                      label="Did the time you had to complete the tasks impact the process you used to complete the tasks (e.g., steps, thought process)? Please explain.",
                                      required=False)
    ae_time_amount_found = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                           label="Did the time you had to complete the tasks impact the amount of information you found? Please explain.",
                                           required=False)
    ae_time_amount_read = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                          label="Did the time you had to complete the tasks impact the extent to which you read the information that you found? Please explain.",
                                          required=False)
    ae_time_pressure_points = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                              label="At what point(s) during the search tasks did you feel time pressure, if any? Please explain.",
                                              required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit2Survey
        exclude = ('user',)


class AnitaExit3Survey(models.Model):
    user = models.ForeignKey(User)
    ae_speed_compare = models.TextField(default="")
    ae_speed_process = models.TextField(default="")
    ae_speed_amount_found = models.TextField(default="")
    ae_speed_amount_read = models.TextField(default="")

    def __unicode__(self):
        return self.user.username


class AnitaExit3SurveyForm(ModelForm):
    ae_speed_compare = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                       label="How did the speed of this system compare to others you have used? Please explain.",
                                       required=False)
    ae_speed_process = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                       label="Did the system speed impact the process you used to complete the tasks (e.g., steps, thought process)? Please explain.",
                                       required=False)
    ae_speed_amount_found = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                            label="Did the system speed impact the amount of information you found for the tasks? Please explain.",
                                            required=False)
    ae_speed_amount_read = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
                                           label="Did the system speed impact the extent to which you read the information that you found? Please explain.",
                                           required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit3Survey
        exclude = ('user',)