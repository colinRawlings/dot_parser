#!python3

########################################################
# Imports
########################################################

from .xdot_parser.lexer import DotLexer
from .xdot_parser.parser import DotParser, DotNode

########################################################
# Functions
########################################################

def parse_dot_string(dot_string):
    """

    parsers and stores edges into nodes parents and children
    attributes

    :param dot_string: bytes
    :return: nodes
    """

    lexer = DotLexer(buf=dot_string)
    parser = DotParser(lexer)

    parser.parse()

    nodes = parser.nodes
    edges = parser.edges

    for edge in edges:
        src_id = edge.src_id
        dst_id = edge.dst_id

        src_node = nodes[edge.src_id]
        dst_node = nodes[edge.dst_id]

        src_node.children[dst_id] = dst_node
        dst_node.parents[src_id] = src_node

    return nodes

def print_sub_graph(node, indent):
    """

    :param node:
    :param indent:
    :return:
    """

    if not isinstance(node, DotNode):
        raise ValueError("Expected a DotNode")

    print(' '*indent + '-' + node.id + ': ' + node.attrs['label'].decode('utf-8'))

    if node.children:
        indent+=1

        print(' '*indent+'|')

        for node_id in node.children:
            print_sub_graph(node.children[node_id], indent)

def get_root_node(node):
    """

    :param node:
    :return:
    """

    if not isinstance(node, DotNode):
        raise ValueError("Expected a DotNode")

    if not node.parents:
        return node

    parent_ids = list(node.parents.keys())

    if len(parent_ids)> 1:
        raise ValueError("Not a tree: multiple parents")

    return get_root_node(node.parents[parent_ids[0]])
