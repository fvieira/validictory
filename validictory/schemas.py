import json
import os
from validictory import SchemaError


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

def find_schemas(schema):
    """Return a list of all schemas referenced in this schema

    Schemas can only be in the following properties
    - items
    - extends

    Why not type? Type is for basic types. If you want an object to validate
    against an existing schema, use extends
    """
    reserved_names = [
        "date-time", "date", "time", "utc-millisec", "regex", "color", "style",
        "phone", "uri", "email", "ip-address", "ipv6", "host-name", "string",
        "number", "integer", "boolean", "object", "array", "null", "any",
        ]

    def find(schema, found):

        # Find references to schemas
        for option, constraints in schema.items():
            if not option in ["extends", "items"]:
                continue

            # Make a list of constraints if we don't have one
            if not isinstance(constraints, list):
                constraints = [constraints]

            # Schema names have to be strings
            for constraint in constraints:
                if (isinstance(constraint, basestring)
                    and constraint not in reserved_names):
                    found.append(constraint)

        # Rescursivly search schema for schema references
        for v in schema.values():
            if isinstance(v, dict):
                found.extend(find(v, found))
            if isinstance(v, list):
                for node in v:
                    if isinstance(node, dict):
                        found.extend(find(node, found))

        return found

    return find(schema, [])


def load_schemas(directory):
    """Return a directory of schemas. Schema names will be the relative path
    of the schema from this directory
    """
    schemas = {}

    for root, dirs, files in os.walk(directory):

        # Remove hidden folders
        for hidden in [d for d in dirs if d.startswith(".")]:
            dirs.remove(hidden)

        for schema in [f for f in files if f.endswith(".json")]:
            path = os.path.join(root, schema)
            schemas[path] = json.load(open(path))

    return schemas


def load(directory):

    # Load schemas into a dictionary
    schemas = load_schemas(directory)

    # Figure out dependecies
    gr = Graph()

    for title, schema in schemas.items():
        gr.add_node(title)
        for dependency in find_schemas(schema):

            # Make sure that dependency exists
            if dependency not in schemas:
                raise SchemaError(("{} schema depends on missing "
                                   "schema {}".format(title, dependency))

            gr.add_edge(title, dependency)

    # Throw SchemaException if graph has cycles
    if gr.has_cycle():
        raise SchemaError("Circular dependency detected")

    #

    return schemas
