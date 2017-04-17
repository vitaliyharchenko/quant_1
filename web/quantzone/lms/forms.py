from django import forms
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from .models import Group, StudentGroupRelation


class GroupForm(forms.ModelForm):
    """
    Form for update all group detail
    """
    class Meta:
        model = Group
        fields = '__all__'


class StudentGroupRelationForm(forms.ModelForm):
    """
    Form edit single studentgroup relation
    """
    class Meta:
        model = StudentGroupRelation
        exclude = ('group',)


# http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html
class BaseStudentsFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no student, that in group twice
        """
        if any(self.errors):
            return

        duplicates = False
        students = []

        for form in self.forms:
            if form.cleaned_data:
                student = form.cleaned_data['student']

                # Check that no student duplicate
                if student:
                    if student in students:
                        duplicates = True
                    students.append(student)

                if duplicates:
                    raise forms.ValidationError(
                        'Учащийся попал в список дважды.',
                        code='duplicate_links'
                    )

StudentsFormSet = formset_factory(StudentGroupRelationForm, formset=BaseStudentsFormSet, can_delete=True)
