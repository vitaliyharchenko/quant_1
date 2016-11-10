from django.shortcuts import render
from teaching.models import Subject


# Create your views here.
def index_view(request):
    subjects = Subject.objects.all().order_by('pk')
    return render(request, 'index.html', {'subjects': subjects})


# Create your views here.
def landing_view(request, landing_id):
    subjects = Subject.objects.all().order_by('pk')
    tpl_str = u'landings/lp_{}.html'.format(landing_id)
    return render(request, tpl_str, {'subjects': subjects})
