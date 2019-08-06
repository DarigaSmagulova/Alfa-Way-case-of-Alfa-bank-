import datetime as dt
from django import forms
from .models import *
class AddQuiz(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title"]
    def save(self, commit=True):
        get,created = Quiz.objects.get_or_create(title=self.cleaned_data['title'])
        return get


class AddQuestions(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["content"]


class AddResponse(forms.ModelForm):
    class Meta:
        model = Response
        exclude = ['score']