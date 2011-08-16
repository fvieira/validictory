import unittest
from validictory.schemas import Graph

class GraphTest(unittest.TestCase):

    def test_add_node(self):
        gr = Graph()
        gr.add_node("Hello")
        self.assertIn("Hello", gr)

    def test_add_nodes(self):
        gr = Graph()
        gr.add_node("Hello", "Goodbye")
        self.assertIn("Hello", gr)
        self.assertIn("Goodbye", gr)

    def test_bad_add_edge(self):
        gr = Graph()
        with self.assertRaises(KeyError):
            gr.add_edge("Hello", "Goodbye")

    def test_add_edge(self):
        gr = Graph()
        gr.add_node("foo", "bar")
        gr.add_edge("foo", "bar")
        self.assertIn("bar", gr["foo"])

    def test_add_edges(self):
        gr = Graph()
        with self.assertRaises(KeyError):
            gr.add_edge("Hello", "Goodbye")

    def test_no_cycle(self):
        gr = Graph()
        gr.add_node("foo", "bar")
        gr.add_edge("foo", "bar")
        self.assertFalse(gr.has_cycle())


    def test_has_cycle(self):
        gr = Graph()
        gr.add_node("foo", "bar")
        gr.add_edge("foo", "bar")
        gr.add_edge("bar", "foo")
        self.assertTrue(gr.has_cycle())
