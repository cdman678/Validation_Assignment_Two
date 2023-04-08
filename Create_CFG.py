import graphviz
import ast


def create_cfg(code_file_path):

    # Read in the .py file as a string
    with open(code_file_path, 'r') as f:
        code = f.read()

    # Parse the code to get the abstract syntax tree
    tree = ast.parse(code)

    # Create a new graph
    graph = graphviz.Digraph()

    counter = 0

    # Generate nodes and edges
    def traverse_tree(node, parent_node_name):
        nonlocal counter
        counter += 1
        node_name = f"Node_{counter}"

        # Determine what the node is based off of the ast parsing
        label = type(node).__name__

        # Add the node to the graph
        graph.node(node_name, label=label)

        # Add an edge from the parent node to this node
        # We need to check if there is a parent node (via parameter)
        if parent_node_name:
            graph.edge(parent_node_name, node_name)

        # Recursively visit child nodes
        for child_node_name, child_node in ast.iter_fields(node):
            if isinstance(child_node, list):
                for i, child in enumerate(child_node):
                    traverse_tree(child, node_name)
            elif isinstance(child_node, ast.AST):
                traverse_tree(child_node, node_name)

    # Start the recursive call
    traverse_tree(tree, None)

    return graph.source


# Sample 1 - A slightly more complex calculator with a GUI
graph = graphviz.Source(create_cfg("Simple-Calculator-1/Simple Calculator by Python.py"))
graph.render('CFG_Output-1', format='png', cleanup=True)

# Sample 2 - A very simple CLI based calculator
graph = graphviz.Source(create_cfg("Simple-Calculator-2/calculator.py"))
graph.render('CFG_Output-2', format='png', cleanup=True)
