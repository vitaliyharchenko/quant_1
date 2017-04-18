from django import forms

from dal import autocomplete

from .models import SubjectTag, Node, NodeRelation


class SubjectsSelectForm(forms.Form):

    choices_list = SubjectTag.objects.all().values_list('pk', 'title')

    choices = forms.MultipleChoiceField(
        choices=choices_list,
        widget=forms.CheckboxSelectMultiple,
        label='Отображаемые предметы',
        required=False
    )


class NodeCreateForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = '__all__'


class NodeRelationCreateForm(forms.ModelForm):
    class Meta:
        model = NodeRelation
        fields = '__all__'
        widgets = {
            'parent': autocomplete.ModelSelect2(url='nodes:node-autocomplete'),
            'child': autocomplete.ModelSelect2(url='nodes:node-autocomplete')
        }
