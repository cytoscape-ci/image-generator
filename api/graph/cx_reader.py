import graph_tool.all as gt

import logging
import math

SUPPORTED_IMAGE_TYPE = ['ps', 'pdf', 'svg', 'png']

LAYOUT_ALGORITHMS = ['sfdp', 'fruchterman_reingold', 'arf']

# TODO: Use color brewer
NODE_COLOR_MAP = {
    # Human
    '9606': [0, 0.9, 1, 1.0],
    # Yeast
    '4932': [1.0, 0, 0, 1.0],
    # Mouse
    '10090': [0, 0.9, 0, 1.0],
    # Fly
    '7215': [0.5, 0.5, 1, 1.0]
}

# Mappings from Gene Type to Node Shape
NODE_SHAPE_MAP = {
    # Protein coding
    'protein-coding': 'double_circle',
    'pseudo': 'pentagon',
    'ncRNA': 'square',
    'rRNA': 'square',
    'snRNA': 'square',
    'snoRNA': 'square',
    'tRNA': 'square',
    'unknown': 'triangle',
    'other': 'triangle'
}


DEF_COLOR = [127.0/255.0, 205.0/255.0, 187.0/255.0, 1.0]
DEF_SHAPE = 'circle'


class GraphGenerator:

    @staticmethod
    def get_graph(cx_data):

        logging.warning(type(cx_data))

        g = gt.Graph()

        # For label
        g.vertex_properties['label'] = g.new_vertex_property('string')
        g.vertex_properties['tax_id'] = g.new_vertex_property('string')
        g.vertex_properties['type_of_gene'] = g.new_vertex_property('string')

        nodes = []
        edges = []
        species = {}
        node_type = {}

        for entry in cx_data:
            if 'nodes' in entry:
                for n in entry['nodes']:
                    nodes.append(n)
            elif 'edges' in entry:
                for e in entry['edges']:
                    edges.append(e)
            elif 'nodeAttributes' in entry:
                for na in entry['nodeAttributes']:
                    attr_name = na['n']
                    # logging.warn(attr_name)
                    if attr_name == 'tax_id':
                        pointer = str(na['po'])
                        species[pointer] = na['v']
                    elif attr_name == 'type_of_gene':
                        pointer = str(na['po'])
                        node_type[pointer] = na['v']

        vmap = {}

        for node in nodes:
            v = g.add_vertex()
            node_id = node['@id']
            if 'n' in node:
                g.vertex_properties['label'][v] = node['n']
                if str(node_id) in species:
                    g.vertex_properties['tax_id'][v] = species[str(node_id)]
                if str(node_id) in node_type:
                    g.vertex_properties['type_of_gene'][v] = node_type[str(node_id)]
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

    generate_color_map(g)

    vertex_color = g.new_vertex_property('vector<double>', val=[0, 0, 0, 0])
    vertex_size = g.new_vertex_property('double', val=25)
    vertex_font_size = g.new_vertex_property('int', val=10)
    vertex_font_family = g.new_vertex_property('string', 'helvatica')
    vertex_text_position = g.new_vertex_property('double', val=(math.pi*(2.0/8.0)))
    vertex_text_color = g.new_vertex_property('vector<double>', val=[0.5,
                                                                     0.5, 0.5, 0.9])

    # Edge properties
    edge_color = g.new_edge_property('vector<double>', val=[0.179, 0.203,
                                                            0.210, 0.9])
    edge_pen_width = g.new_edge_property('double', val=5)
    edge_end_marker = g.new_edge_property('string', val='none')

    gt.graph_draw(g, pos=pos,
                  vertex_color=vertex_color,
                  vertex_fill_color=g.vertex_properties['fill_color'],
                  vertex_shape=g.vertex_properties['shape'],
                  # vertex_text=g.vertex_properties['label'],
                  vertex_font_size=vertex_font_size,
                  vertex_font_family=vertex_font_family,
                  vertex_text_position=vertex_text_position,
                  vertex_text_color=vertex_text_color,
                  vertex_size=vertex_size,

                  edge_color=edge_color,
                  edge_pen_width=edge_pen_width,
                  edge_end_marker=edge_end_marker,
                  output_size=(1600, 1600), output=file_name)

    return file_name


def generate_color_map(g):
    g.vertex_properties['fill_color'] = g.new_vertex_property('vector<double>')
    g.vertex_properties['shape'] = g.new_vertex_property('string')

    prop_names = g.vertex_properties.keys()

    logging.warn("---------------------- V props --------------------")
    logging.warn(prop_names)

    if 'tax_id' in prop_names:
        for v in g.vertices():
            tax_id = g.vertex_properties['tax_id'][v]
            gene_type = g.vertex_properties['type_of_gene'][v]

            if tax_id in NODE_COLOR_MAP:
                g.vertex_properties['fill_color'][v] = NODE_COLOR_MAP[tax_id]
            else:
                g.vertex_properties['fill_color'][v] = DEF_COLOR

            if gene_type in NODE_SHAPE_MAP:
                g.vertex_properties['shape'][v] = NODE_SHAPE_MAP[gene_type]
            else:
                g.vertex_properties['shape'][v] = DEF_SHAPE
    else:
        for v in g.vertices():
            g.vertex_properties['fill_color'][v] = DEF_COLOR


def render_graphviz(g, file_name):
    gt.graphviz_draw(g,
                     vcolor='#0055FF',
                     elen=10,
                     layout='dot',
                     output=file_name,
                     size=(30, 30),
                     vsize=1,
                     penwidth=4,
                     vprops={
                         'label': g.vertex_properties['label'],
                         'labeljust': 'b',
                         'labelloc': 'b',
                         'labeldistance': 7.5,
                         'labelangle': 75
                     })
