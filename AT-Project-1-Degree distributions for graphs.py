"""
For your first project, you will write Python code 
that creates dictionaries corresponding to some 
simple examples of graphs. You will also implement 
two short functions that compute information about 
the distribution of the in-degrees for nodes in 
these graphs.
"""

EX_GRAPH0 = {0 : set([1, 2]), 
             1 : set([]), 
             2 : set([])
            }

EX_GRAPH1 = {0 : set([1, 4, 5]), 
             1 : set([2, 6]), 
             2 : set([3]),
             3 : set([0]),
             4 : set([1]),
             5 : set([2]),
             6 : set()
            }

EX_GRAPH2 = {0 : set([1, 4, 5]), 
             1 : set([2, 6]), 
             2 : set([3, 7]),
             3 : set([7]),
             4 : set([1]),
             5 : set([2]),
             6 : set(),
             7 : set([3]),
             8 : set([1, 2]),
             9 : set([0, 3, 4, 5, 6, 7])
            }


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns 
    a dictionary corresponding to a complete directed 
    graph with the specified number of nodes.
    """
    if num_nodes > 0:
        graph = {}
        nodes = [n for n in range(num_nodes)]
        for node in range(num_nodes):
            graph[node] = set()
            for edge in nodes:
                if edge != node:
                    graph[node].add(edge)
        return graph
    else:
        return {}
    
    
def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a 
    dictionary) and computes the in-degrees for the 
    nodes in the graph.
    """
    res = {}
    for node in digraph.keys():
        res[node] = 0
    for indegrees in digraph.values():
        for indegree in indegrees:
            if indegree not in res.keys():
                res[indegree] = 1
            res[indegree] += 1
    return res
   

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a 
    dictionary) and computes the unnormalized distribution 
    of the in-degrees of the graph. 
    """
    indegree = compute_in_degrees(digraph)
    distribution = {}
    for count in indegree.values():
        if count not in distribution.keys():
            distribution[count] = 0
        distribution[count] += 1
    return distribution
    
    
    
    
    