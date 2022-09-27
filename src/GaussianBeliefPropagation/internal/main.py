from GBP import *


def generate_variable_nodes(num_variable_nodes: int, dims=1) -> List[VariableNode]:
    nodes = []
    for i in range(num_variable_nodes):
        nodes.append(VariableNode(dims, i))
    return nodes


def generate_factor() -> GaussianState:
    factor = GaussianState(2)
    factor.eta = np.array([0.5, 0.5])
    factor.lam = np.array([[1., 0.], [0., 1.]])
    return factor


def connect_variable_nodes_with_factor_nodes(v_nodes: List[VariableNode]) -> List[FactorNode]:
    f_nodes = []
    for i in range(len(v_nodes) - 1):
        factor = generate_factor()
        f_nodes.append(FactorNode(factor, [v_nodes[i], v_nodes[i + 1]]))
    return f_nodes


if __name__ == "__main__":
    variable_nodes = generate_variable_nodes(5)
    factor_nodes = connect_variable_nodes_with_factor_nodes(variable_nodes)
    factor_graph = FactorGraph(variable_nodes, factor_nodes)

    factor_graph.synchronous_iteration()
    factor_graph.synchronous_iteration()
