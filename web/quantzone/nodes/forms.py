from django import forms
from .models import SubjectTag


class SubjectsSelectForm(forms.Form):

    choices_list = SubjectTag.objects.all().values_list('pk', 'title')

    choices = forms.MultipleChoiceField(
        choices=choices_list,
        widget=forms.CheckboxSelectMultiple,
        label='Отображаемые предметы',
        required=False
    )
