'''
Created on 23/01/2014

@author: MMPE
'''

import collections
#try: range = range; range = None
#except NameError: pass
#try: str = unicode; unicode = None
#except NameError: pass
import numpy as np

def Branch():
    return collections.defaultdict(Branch)


class Tree(dict):
    def __init__(self, graph, root=None):
        dict.__init__(self)
        assert isinstance(graph, UndirectedGraph)
        self.graph = graph
        if root is not None:
            self[root] = Tree(graph)


    def add(self, node):
        self[node] = Tree(self.graph)
        return self[node]

    def to_lst(self):
        return self._to_lst()

    def _to_lst(self, parent=None):
        lst = []
        for n in sorted(self.keys()):
            if parent is not None:
                lst.append((parent, n, self.graph.relations[parent][n]))
            lst.extend(self[n]._to_lst(n))
        return lst

    def to_str(self):
        return self._to_str()

    def _to_str(self, parent=None, level=0):
        s = ""
        for n in sorted(self.keys()):
            if self.graph and parent and self.graph.relations[parent][n]:
                s += "- "*level + "%s(%s)\n" % (n, self.graph.relations[parent][n])
            else:
                s += "- "*level + "%s\n" % n
            s += self[n]._to_str(n, level + 1)
        return s

class Forest(Tree):
    def __init__(self, graph):
        dict.__init__(self)
        assert isinstance(graph, UndirectedGraph)
        self.graph = graph
        self.no_trees = 0


    def add(self, tree):
        id = self.no_trees
        self.no_trees += 1
        self[id] = tree

    def _to_str(self, parent=None, level=0):
        return "".join([t.to_str() for t in self.values()])

    def _to_lst(self, parent=None):
        lst = []
        for t in self.values():
            lst.extend(t._to_lst())
        return lst


class UndirectedGraph(object):
    def __init__(self):
        self.nodes = set()
        self.relations = Branch()
        self.edges = collections.defaultdict(list)

    def add_edge(self, a, b, relation=None):
        self.nodes.add(a)
        self.nodes.add(b)
        if not isinstance(relation, (tuple, list)):
            relation = (relation, relation)
        self.relations[a][b] = relation[1]
        self.relations[b][a] = relation[0]
        self.edges[a].append(b)
        self.edges[b].append(a)

    def forest(self, roots):
        self._visited = set()
        forest = Forest(self)
        for root in roots:
            if root not in self._visited:
                forest.add(self.tree(root, self._visited))
        return forest

    def tree(self, root, visited=set()):
        tree = Tree(self, root)
        self._visited = visited.copy()
        self.fill_tree(tree, root)
        return tree

    def fill_tree(self, tree, root):
        self._visited.add(root)
        tree[root]
        for c in self.edges[root]:
            if c not in self._visited:
                tree[root].add(c)
                self.fill_tree(tree[root], c)


#    def forest_str(self, roots):
#        return "".join([root + "\n" + self._tree_str(root, self.tree(root)[root], 1) for root in roots])
#
#
#
#    def tree_str(self, tree):
#        root = tree.keys()[0]
#        return root + "\n" + self._tree_str(root, tree[root], 1)
#
#
#    def _tree_str(self, root, branch, level):
#        s = ""
#        if branch:
#            for r, b in branch.items():
#                s += "- "*level + "%s(%s)\n" % (r, self.relations[root][r])
#                s += self._tree_str(r, b, level + 1)
#        return s
#
#    def forest_list(self, roots):
#        forest_list = []
#        for root in roots:
#            pass

#    def tree_list(self, root):
#        return self._tree_list(None, root, self.tree(root), [])
#
#    def _tree_list(self, parent, node, branch, lst):
#        if branch:
#            for r, b in branch.items():
#                lst.append((node, r, self.relations[node][r]))
#                self._tree_list(node, r, b, lst)
#        return lst




