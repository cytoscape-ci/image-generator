import graph_tool.all as gt

import logging
import math

SUPPORTED_IMAGE_TYPE = ['ps', 'pdf', 'svg', 'png']

LAYOUT_ALGORITHMS = ['sfdp', 'fruchterman_reingold', 'arf']


class GraphGenerator:

    @staticmethod
    def get_graph(cx_data):

        logging.warning(type(cx_data))

        g = gt.Graph()

        # For label
        g.vertex_properties['label'] = g.new_vertex_property('string')

        nodes = []
        edges = []

        for entry in cx_data:
            if 'nodes' in entry:
                for n in entry['nodes']:
                    nodes.append(n)
            elif 'edges' in entry:
                for e in entry['edges']:
                    edges.append(e)

        vmap = {}

        for node in nodes:
            v = g.add_vertex()
            node_id = node['@id']
            if 'n' in node:
                g.vertex_properties['label'][v] = node['n']
            vmap[node_id] = v

        for edge in edges:
            source = vmap[edge['s']]
            target = vmap[edge['t']]
            e = g.add_edge(source, target)

        return g

    @staticmethod
    def get_image(g, img_type='png', layout=None, renderer=None):

        # Check file type
        if img_type in SUPPORTED_IMAGE_TYPE:
            logging.info('Output file type is ' + img_type)
        else:
            raise ValueError('Image type not supported: ' + img_type)

        file_name = '/app/images/graph.' + img_type

        if renderer is None:
            render(g, file_name, layout)
        else:
            render_graphviz(g, file_name)

        return file_name


def get_pos(g, algorithm='sfdp'):
    if algorithm is 'sfdp':
        return gt.sfdp_layout(g)
    elif algorithm is 'arf':
        return gt.arf_layout(g, max_iter=2000)


def render(g, file_name, layout):
    # Perform Layout
    pos = get_pos(g, algorithm=layout)

    vertex_color = g.new_vertex_property('vector<double>', val=[0, 0, 0, 0])
    vertex_fill_color = g.new_vertex_property('vector<double>', val=[0, 0.5, 0.9, 0.7])
    vertex_font_size = g.new_vertex_property('int', val=6)
    vertex_text_position = g.new_vertex_property('double', val=(math.pi*(2.0/8.0)))
    vertex_text_color = g.new_vertex_property('vector<double>', val=[0.2, 0.2, 0.2, 0.8])

    # Edge properties
    edge_color = g.new_edge_property('vector<double>', val=[0.179, 0.203, 0.210, 0.7])
    edge_pen_width = g.new_edge_property('double', val=1)
    edge_end_marker = g.new_edge_property('string', val='none')


    gt.graph_draw(g, pos=pos,
                  vertex_color=vertex_color,
                  vertex_fill_color=vertex_fill_color,
                  vertex_text=g.vertex_properties['label'],
                  vertex_font_size=vertex_font_size,
                  vertex_text_position=vertex_text_position,
                  vertex_text_color=vertex_text_color,

                  edge_color=edge_color,
                  edge_pen_width=edge_pen_width,
                  edge_end_marker=edge_end_marker,
                  output_size=(1000, 1000), output=file_name)

    return file_name


def render_graphviz(g, file_name):
    gt.graphviz_draw(g,
                     vcolor='#00688B',
                     elen=10,
                     layout='dot',
                     output=file_name,
                     size=(50, 50),
                     vsize=2,
                     penwidth=10)
