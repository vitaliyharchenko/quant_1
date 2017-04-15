from django.shortcuts import render, reverse, HttpResponse
from graphviz import Digraph
from nodes.models import NodeRelation


# Create svg for graph
def svg_view(request):

    def modify_title(title):
        return title.replace(' ', '\n')


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
            dot.node(edge.parent.title, modify_title(edge.parent.title), color=get_color(edge.parent.type_tag))
            dot.node(edge.child.title, modify_title(edge.child.title), color=get_color(edge.child.type_tag))
            dot.edge(edge.parent.title, edge.child.title)

    dot.format = 'svg'
    return HttpResponse(dot.pipe(), 'image/svg+xml')


def graph_view(request):
    return render(request, 'graph.html', {'s': reverse('nodes:svg_view')})
