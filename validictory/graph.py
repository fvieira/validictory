class Graph(dict):

    def add_node(self, *nodes):
        for node in nodes:
            self[node] = set()

    def add_edge(self, source, sink):
        self[source].add(sink)

    def add_edges(self, edges):
        for source, sink in edges:
            self[source].add(sink)

    def has_cycle(self):
        """Return True if this graph has a cycle"""
        # All edges in the graph
        edges = set().union(*[v for k,v in self.items()])

        # Set of all nodes with no incoming edges
        sources = [k for k,v in self.items() if k not in edges]

        while len(sources) != 0:
            node = sources.pop()
            edges = self[node]

            # Remove the edges
            nodes = list(edges)
            self[node].clear()

            # We need the set of all edges to determine if the node is a sink
            all_edges = set().union(*[v for k,v in self.items()])

            for node in nodes:
                print node
                if node not in all_edges:
                    sources.append(node)

        # All edges in the graph
        edges = set().union(*[v for k,v in self.items()])

        # if graph has edges then graph has a cycle
        if edges:
            return True
        else:
            return False
