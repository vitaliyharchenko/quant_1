from .models import Node, NodeRelation

from dal import autocomplete

from django import forms


class NodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Node.objects.none()

        qs = Node.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)
        print(qs)
        return qs


class NodeRelationForm(forms.ModelForm):
    class Meta:
        model = NodeRelation
        fields = '__all__'
        widgets = {
            'parent': autocomplete.ModelSelect2(url='nodes:node-autocomplete'),
            'child': autocomplete.ModelSelect2(url='nodes:node-autocomplete')
        }
