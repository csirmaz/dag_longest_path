
class DAGLongestPath:
    """Calculate the longest path in a directed acyclic graph (DAG) in terms of node weights
    
    Use this class to get (one of) the paths with the largest sum of node weights
    in a directed acyclic graph (DAG). After constructing the empty object,
    use `add_node(label, weight)` and `add_edge(label1, label2)` to build the graph, 
    and then call `longest_path` to retrieve the path and the sum of the weights.
    This latter operation is destructive and will delete the graph.
    """
    
    def __init__(self):
        """Construct a new empty graph."""
        self.nodes = {}  # Dictionary {<label>:<weight>, ...}
        self.edges = {}  # Dictionary of sets dict{ <source_label>: set{<target_label>, ...}, ...}
        self.rev_edges = {}  # Dictionary of sets
        self.unseen_sources = set()  # Labels of all nodes not processed yet that have no incoming edges
        self.longest_in_weight = {}  # Dictionary {<label>:<weight>, ...}
        self.longest_in_route = {}   # Dictionary {<label>:[<label>, ...], ...}
        self.longest_route = None;   # The longest route (in weights) we have seen
        self.longest_route_weight = None;  # The larges weight we have seen
    
    def add_node(self, label, weight):
        """Add a node to a graph.
        
        # Arguments
            label: a scalar label for the node
            weight: a nonnegative number
        """
        if weight < 0: raise ValueError("weight cannot be negative")
        self.nodes[label] = weight
        self.edges[label] = set()
        self.rev_edges[label] = set()
        self.unseen_sources.add(label)
        
    def add_edge(self, source, target):
        """Add an edge to a graph.
        
        # Arguments
            source: the label of the source node; it should already exist in the graph
            target: the label of the target node; it should already exist in the graph
        """
        if source not in self.nodes: raise ValueError("source {} not a node".format(source))
        if target not in self.nodes: raise ValueError("target {} not a node".format(target))
        self.edges[source].add(target)
        self.rev_edges[target].add(source)
        self.unseen_sources.discard(target)
        
    def __del_edges_from(self, source):
        """Private method to delete all outgoing edges from a node."""
        targets = self.edges[source]
        self.edges[source] = set()
        for target in targets:
            self.rev_edges[target].discard(source)
            if len(self.rev_edges[target]) == 0: # no incoming edges
                self.unseen_sources.add(target)
                
    def __print(self):
        """Private method to print information about the graph."""
        print("Nodes, Edges")
        for id, w in self.nodes.items():
            print("  {}{} = {} -> {}".format(
                's' if id in self.unseen_sources else ' ', 
                id, 
                w,
                ",".join([str(x) for x in self.edges[id]])
            ))
        print("Rev-Edges")
        for id, source in self.rev_edges.items():
            print("  {} <- {}".format(id, ",".join([str(x) for x in source])))
        print("Longest in")
        for id, w in self.nodes.items():
            print("  {} : {} = {}".format(
                id,
                str(self.longest_in_weight.get(id, 0)),
                ",".join([str(x) for x in self.longest_in_route.get(id, [])])
            ))        
        print("")
        
        
    def longest_path(self):
        """Return the longest path in the graph in terms of the node weights.
        
        Warning: This operation is destructive and will delete the graph.
        
        # Returns
            An array of the route (array of labels), and the sum of the weights along the route.
        """
        while len(self.unseen_sources) > 0:
            sourcenode = self.unseen_sources.pop()
            
            new_weight = self.longest_in_weight.get(sourcenode, 0) + self.nodes[sourcenode]
            new_route = self.longest_in_route.get(sourcenode, []) + [sourcenode]

            if len(self.edges[sourcenode]) == 0: # no outgoing edges; isolated node
                if self.longest_route is None or self.longest_route_weight < new_weight:
                    self.longest_route = new_route
                    self.longest_route_weight = new_weight
                continue
            
            # There are outgoing edges            
            for target in self.edges[sourcenode]:
                
                if self.longest_in_weight.get(target, 0) < new_weight:
                    self.longest_in_weight[target] = new_weight
                    self.longest_in_route[target] = new_route
                
            self.__del_edges_from(sourcenode)
                
        return (self.longest_route, self.longest_route_weight)


if __name__ == '__main__':

    dag = DAGLongestPath()
    for i in range(6): dag.add_node(i, i)
    dag.add_edge(3, 5)
    dag.add_edge(2, 5)
    dag.add_edge(2, 4)
    dag.add_edge(1, 2)
    print(dag.longest_path())
