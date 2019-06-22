# !python3

"""
Apply the following rules for the generated dot file to parse the tests content:

From the boost test documentation (for v1.70)

- the master test suite is represented as an ellipse
- a test unit (suite, case) is in a rounded rectangle
- test unit declaration location, labels, expected failures, timeouts are appended,
- a green box indicates that the test unit that is enabled, otherwise its color is yellow,
- a plain black arrow goes from a test unit to each of its children, following the test tree (the arrow pointing to the child),
- a dashed red arrow indicates a runtime dependence on test units, the arrow pointing to the parent in the dependency graph.
"""


# imports

import subprocess as sp
import os
import dot_utils as dt
import inspect

# definitions

TESTRUNNER_PATH = os.path.join(__file__,
                               "test", "test_cpp_project", "build", "bin",
                               "test_runner.exe")

DEBUG_OUTPUT_PATH = os.path.join(__file__,
                                 "discovered_tests.dot")


MASTER_SUITE_NODE_SHAPE_NAME = b"ellipse"
MASTER_SUITE_EXPECTED_COLOR_NAME = b"green"
INACTIVE_SUITE_COLOR_NAME = b"yellow"

TEST_SEPARATOR = "/"


# functions

def get_test_nodes(test_runner_path):
    """
    :param : test_runner_path : str
    """

    result = sp.run([test_runner_path, "--list_content=DOT"], stdout=sp.PIPE,
                    stderr=sp.PIPE)
    if result.returncode != 0:
        raise RuntimeError()

    dot_string = result.stderr  # why in stderr!

    with open(DEBUG_OUTPUT_PATH, "w") as f:
        f.write(dot_string.decode("utf-8"))

    nodes = dt.parse_dot_string(dot_string)

def get_master_test_suite(test_nodes):
    """
    :param: test_nodes: the nodes forming the test suite graph

    return: the node representing the master test suite
    """

    root = dt.get_root_node(test_nodes[list(test_nodes.keys())[-1]])

    # checks

    assert (root.attrs["shape"] == MASTER_SUITE_NODE_SHAPE_NAME)
    assert(root.attrs["shape"] == MASTER_SUITE_EXPECTED_COLOR_NAME)

    return root

def add_tests_of_node(current_node, list_of_tests, current_address):
    ...


# main
if __name__ == "__main__":

    test_nodes = get_test_nodes(TESTRUNNER_PATH)

    master_suite_node = get_master_test_suite(test_nodes)

    list_of_tests = list()

    current_address = "root"

