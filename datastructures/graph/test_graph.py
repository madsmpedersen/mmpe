'''
Created on 23/01/2014

@author: MMPE
'''
import unittest
from mmpe.datastructures.graph.graph import UndirectedGraph, Tree


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            self.g.add_edge(a, b, c)

    def test_add_edge(self):
        self.assertTrue('Ellen' in  self.g.edges['Mads'])


    def test_add_edge_relation(self):

        self.assertTrue('Ellen' in  self.g.edges['Mads'])
        self.assertEqual(self.g.relations['Mads']['Ellen'], 'child')
        self.assertEqual(self.g.relations['Ellen']['Mads'], 'dad')
        self.assertEqual(self.g.tree('Mads').to_str(), """Mads
- Agnes(parent-child)
- Ellen(child)
- Per(dad)
- - Magnus(parent-child)
- - Marie(daughter)
- Sine(Wife)
""")

    def test_tree2str(self):
        g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            g.add_edge(a, b)
        self.assertEqual(g.tree('Mads').to_str(), """Mads
- Agnes
- Ellen
- Per
- - Magnus
- - Marie
- Sine
""")


    def test_tree_list(self):
        self.assertEqual(self.g.tree('Mads').to_lst(), [('Mads', 'Agnes', 'parent-child'),
                                                        ('Mads', 'Ellen', 'child'),
                                                        ('Mads', 'Per', 'dad'),
                                                        ('Per', 'Magnus', 'parent-child'),
                                                        ('Per', 'Marie', 'daughter'),
                                                        ('Mads', 'Sine', 'Wife'),
                                                        ])


    def test_tree_list2(self):
        g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            g.add_edge(a, b)
        self.assertEqual(g.tree('Mads').to_lst(), [('Mads', 'Agnes', None),
                                                   ('Mads', 'Ellen', None),
                                                   ('Mads', 'Per', None),
                                                   ('Per', 'Magnus', None),
                                                   ('Per', 'Marie', None),
                                                   ('Mads', 'Sine', None),
                                                   ])


    def test_forest_to_str(self):
        self.assertEqual(self.g.forest(['Mads', 'Hans']).to_str(), """Mads
- Agnes(parent-child)
- Ellen(child)
- Per(dad)
- - Magnus(parent-child)
- - Marie(daughter)
- Sine(Wife)
Hans
- Inger(Wife)
""")

    def test_forest_to_lst(self):
        self.assertEqual(self.g.forest(['Mads', 'Hans']).to_lst(), [
                                                                    ('Mads', 'Agnes', 'parent-child'),
                                                                    ('Mads', 'Ellen', 'child'),
                                                                    ('Mads', 'Per', 'dad'),
                                                                    ('Per', 'Magnus', 'parent-child'),
                                                                    ('Per', 'Marie', 'daughter'),
                                                                    ('Mads', 'Sine', 'Wife'),
                                                                    ('Hans', 'Inger', 'Wife'),
                                                                    ])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_add_edge']
    unittest.main()
