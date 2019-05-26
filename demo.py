#!python3

########################################################
# Import
########################################################

import dot_utils as dt

########################################################
# Trial Data
########################################################

# taken from a demo boost test suite

boost_tests_string = rb"""
digraph G {rankdir=LR;
tu1[shape=ellipse,peripheries=2,fontname=Helvetica,color=green,label="test module name"];
{
tu2[shape=Mrecord,fontname=Helvetica,color=green,label="test_suite1|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(6)"];
tu1 -> tu2;
{
tu65536[shape=Mrecord,fontname=Helvetica,color=green,label="test_case1|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(8)"];
tu2 -> tu65536;
tu65537[shape=Mrecord,fontname=Helvetica,color=green,label="test_case2|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(10)"];
tu2 -> tu65537;
tu65538[shape=Mrecord,fontname=Helvetica,color=green,label="test_liba|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(16)"];
tu2 -> tu65538;
}
tu3[shape=Mrecord,fontname=Helvetica,color=green,label="test_suite2|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(19)"];
tu1 -> tu3;
{
tu65539[shape=Mrecord,fontname=Helvetica,color=green,label="test_case3|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(21)"];
tu3 -> tu65539;
tu65540[shape=Mrecord,fontname=Helvetica,color=green,label="test_case4|C:\Users\colinrawlings\Desktop\test_cmake_tools\test\test_suite1.cpp(23)"];
tu3 -> tu65540;
}
}
}
"""

########################################################
# Main
########################################################


if __name__ == '__main__':

    nodes = dt.parse_dot_string(boost_tests_string)

    root = dt.get_root_node(nodes['tu65537'])

    dt.print_sub_graph(root, 0)