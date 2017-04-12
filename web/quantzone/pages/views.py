from django.shortcuts import render, reverse, HttpResponse

from nodes.models import Subject, Node, NodeRelation

from graphviz import Digraph


# Create your views here.
def index_view(request):
    subjects = Subject.objects.all().order_by('pk')
    return render(request, 'index.html', {'subjects': subjects})


def landing_view(request, landing_id):
    subjects = Subject.objects.all().order_by('pk')
    tpl_str = u'landings/lp_{}.html'.format(landing_id)
    return render(request, tpl_str, {'subjects': subjects})


def svg_view(request):

    def get_color(type_tag):
        if type_tag == 1:
            return "#33CC66"
        elif type_tag == 2:
            return "#6699FF"
        else:
            return "##FFFFFF"

    dot = Digraph(comment='The math table')

    dot.attr('graph', size="9, 4")
    dot.attr('graph', ratio="fill")
    dot.attr('graph', center="true")
    dot.attr('graph', fontsize="20")
    dot.attr('node', style="filled")

    for edge in NodeRelation.objects.all().order_by('pk'):
        if str(edge.parent.subject_tag) == 'Математика' and str(edge.child.subject_tag) == 'Математика':
            dot.node(edge.parent.title, edge.parent.title, color=get_color(edge.parent.type_tag))
            dot.node(edge.child.title, edge.child.title, color=get_color(edge.child.type_tag))
            dot.edge(edge.parent.title, edge.child.title)

    dot.format = 'svg'
    return HttpResponse(dot.pipe(), 'image/svg+xml')


def graph_view(request):
    return render(request, 'graph.html', {'s': reverse('svg_view')})
