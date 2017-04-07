from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def template(request):
    return render(request, 'template.html')
