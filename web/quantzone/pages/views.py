from django.shortcuts import render, reverse, HttpResponse

from nodes.models import Subject, Node, NodeRelation

import json
import networkx as nx
from networkx.readwrite import json_graph
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
    all_node_relations = NodeRelation.objects.all()

    dg = nx.DiGraph()

    for relation in all_node_relations:
        dg.add_edge(str(relation.parent), str(relation.child))

    labels = []
    nx.set_node_attributes(dg, 'labels', labels)
    # 0 - не рисуем
    visiable = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 1, 1, 1, 1,
                0, 1, 1, 0, 1, 1, 1, 1, 1, 1,
                0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                0, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                1, 1, 1, 1, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 0, 1, 1, 1, 1, 1,
                1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
                0, 1, 1, 1, 0, 0]
    # 0 - ничего, 1 - понятие, 2 - метод, 3 - раздвоить вершину
    colors = [0, 1, 1, 2, 3, 1, 2, 1, 1, 1,
              0, 1, 1, 1, 1, 1, 0, 2, 0, 2,
              1, 1, 2, 1, 2, 1, 0, 1, 3, 1,
              3, 1, 2, 2, 1, 0, 2, 1, 1, 2,
              0, 2, 2, 0, 1, 2, 2, 1, 1, 2,
              0, 2, 1, 1, 1, 2, 0, 2, 0, 1,
              2, 1, 2, 1, 2, 2, 3, 2, 2, 1,
              2, 1, 0, 1, 1, 1, 1, 1, 2, 2,
              0, 2, 1, 1, 2, 1, 0, 1, 0, 1,
              1, 2, 2, 2, 2, 1, 1, 0, 2, 0,
              2, 1, 2, 0, 1, 1, 1, 2, 1, 1,
              1, 1, 2, 1, 2, 0, 1, 1, 2, 2,
              0, 1, 1, 1, 0, 0]

    i = 0
    for node in dg.nodes():
        dg[node]['color'] = colors[i]
        dg[node]['vis'] = visiable[i]
        i += 1
        print(dg[node])

    # for edge in dg.edges():
    #     print(type(edge))

    def get_color(x):
        if x == 1:
            return "#33CC66"
        elif x == 2:
            return "#6699FF"
        else:
            return "#FFFFFF"

    dot = Digraph(comment='The math table')

    dot.attr('graph', size="6,4")
    dot.attr('graph', ratio="fill")
    dot.attr('node', style="filled")

    i = 0
    for node in dg.nodes():
        print(node)
        if visiable[i] != 0:
            dot.node(str(i), node, color=get_color(colors[i]))
        i += 1

    for edge in dg.edges():
        if edge[1] != 'color' and edge[1] != 'vis':
            print(str(dg.nodes().index(edge[0])), str(dg.nodes().index(edge[1])))
            dot.edge(str(dg.nodes().index(edge[0])), str(dg.nodes().index(edge[1])))

    dot.format = 'svg'
    return HttpResponse(dot.pipe(), 'image/svg+xml')


def graph_view(request):
    return render(request, 'graph.html', {'s': reverse('svg_view')})
