import colorsys

from django.shortcuts import render, reverse, HttpResponse
from graphviz import Digraph
from nodes.models import NodeRelation, SubjectTag, Node

from .forms import SubjectsSelectForm


# Create svg for graph
def svg_view(request):

    # get info abut what subjects to draw
    try:
        picked = request.GET['picked']
        picked = picked.split(',')
        if picked[0]:
            subjects_list = SubjectTag.objects.filter(id__in=picked)
        else:
            subjects_list = SubjectTag.objects.all()
    except KeyError:
        subjects_list = SubjectTag.objects.all()

    def modify_title(title):
        return title.replace(' ', '\n')

    def get_color(node):
        type_tag = node.type_tag
        subject_tag = node.subject_tag
        subjects_count = subjects_list.count()
        rgb_color = (int(subject_tag.pk*255.0/subjects_count), int(105+int(type_tag)*100.0/2), 255)
        hex_color = '#%02x%02x%02x' % rgb_color
        return hex_color

    dot = Digraph(comment='The math table')

    dot.attr('graph', size="8, 4,5")
    dot.attr('graph', ratio="fill")
    dot.attr('graph', center="true")
    dot.attr('graph', fontsize="20")
    dot.attr('node', style="filled")

    for edge in NodeRelation.objects.all().order_by('pk'):
        if edge.parent.subject_tag in subjects_list and edge.child.subject_tag in subjects_list:
            dot.node(edge.parent.title, modify_title(edge.parent.title), color=get_color(edge.parent))
            dot.node(edge.child.title, modify_title(edge.child.title), color=get_color(edge.child))
            dot.edge(edge.parent.title, edge.child.title)

    dot.format = 'svg'
    return HttpResponse(dot.pipe(), 'image/svg+xml')


# General view for graph
def graph_view(request):

    node_list = Node.objects.all()
    edge_list = NodeRelation.objects.all()

    if request.method == "POST":
        subjects_form = SubjectsSelectForm(request.POST or None)
        if subjects_form.is_valid():
            picked = subjects_form.cleaned_data.get('choices')
            if len(picked) != 0:
                node_list = node_list.filter(subject_tag__in=picked)
                edge_list = edge_list.filter(parent__subject_tag__in=picked)
            picked_str = ','.join(picked)
            svg_url = '{url}?picked={picked}'.format(url=reverse('nodes:svg_view'), picked=picked_str)
    else:
        subjects_form = SubjectsSelectForm()
        svg_url = reverse('nodes:svg_view')

    context = {
        'svg_url': svg_url,
        'subject_form': subjects_form,
        'node_list': node_list,
        'edge_list': edge_list
    }

    return render(request, 'nodes/graph.html', context)


def create_nodes(request):
    return render(request, 'nodes/create.html')
