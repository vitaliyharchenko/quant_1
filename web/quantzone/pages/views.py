from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def styleguide(request):
    return render(request, 'styleguide.html')


def email_styleguide(request):
    current_site = get_current_site(request)
    return render(request, 'email/email_styleguide.html', {'domain': current_site.domain})
