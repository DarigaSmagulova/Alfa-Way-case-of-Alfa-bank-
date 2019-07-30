from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from DH.models import Employee_levels

from speciality.models import Speciality
from .models import Profile
#from #datetimewidget.widgets import DateTimeWidget
import datetime as dt
from soft_skills.models import Skill


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'speciality']

    def save(self, request, commit=True):
        a = Speciality.objects.all()
        for i in a:
            if self.cleaned_data['speciality'] == i.__str__():
                print(i)
                for j in i.skill.all():
                    form, created = Skill.objects.get_or_create(
                        name=j.name, type='hard'
                    )
                    form.user.add(request.user)

# class DateForm(forms.Form):
#     date = forms.DateTimeField(
#         input_formats=['%d/%m/%Y %H:%M'],
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control datetimepicker-input',
#             'data-target': '#datetimepicker1'
#         })
#     )
class NewTopicForm(forms.ModelForm):
    time_choices = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(9,18)]
    test_date = forms.DateField(widget=forms.DateInput),
    test_time=forms.TimeField(widget=forms.Select(choices=time_choices))
    #     (attrs={
    #     'class': 'form-control datetimepicker-input'})
    # )
    #test_date=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'DateForm'}), help_text='Choose date when you want to pass your exam')
    class Meta:
        model = Employee_levels
        fields = ["test_date", "test_time"]
