import unittest
from tree.Tree import Tree

class TestTree(unittest.TestCase):

    def test_create_tree_0(self):
        t = Tree(None)
        self.assertEqual(t.root().element(), None)
        
    def test_create_tree_1(self):
        # A tree with only a root.
        t = Tree()
        self.assertEqual(len(t), 1)

    def test_create_tree_2(self):
        # A tree with root, three children.
        t = Tree('r')
        t._add(t.root(), 'a')
        t._add(t.root(), 'b')
        t._add(t.root(), 'c')
        self.assertEqual(t.height(), 1)
        self.assertEqual(len(t), 4)

    def test_create_tree_3(self):
        t = Tree()
        a = t._add(t.root(), 'a')
        t._add(t.root(), 'b')
        t._add(t.root(), 'c')
        t._add(a, 'aa')
        self.assertEqual(t.height(), 2)
        # Single child node of node a contains value 'aa' as element.
        self.assertEqual(t.children(a)[0].element(), 'aa')

    def test_bfs_1(self):
        t = Tree('a')
        b = t._add(t.root(), 'b')
        t._add(b, 'd')
        c = t._add(t.root(), 'c')
        t._add(c, 'e')
        f = t._add(c, 'f')
        t._add(f, 'g')
        self.assertEqual([x.element() for x in t.bfs()],
                         ['a','b','c','d','e','f','g'])


    def test_add_between(self):

        t = Tree('r')
        r = t.root()
        a = t.add(r, 'a')
        b = t.add(a, 'b')
        c = t.add(a, 'c')
        d = t.add(a, 'd')
        e = t.add_between(r, a, 'e')
        f = t.add(e, 'f')
        self.assertEqual([x.element() for x in t.bfs()],
              ['r', 'e', 'a', 'f', 'b', 'c', 'd'])
        self.assertEqual(len(t), 7)
        self.assertEqual(t.height(), 3)

    def test_level_order(self):
        t = Tree('r')
        r = t.root()
        a = t.add(r, 'a')
        b = t.add(a, 'b')
        c = t.add(a, 'c')
        d = t.add(a, 'd')
        e = t.add_between(r, a, 'e')
        f = t.add(e, 'f')

        self.assertEqual([[x.element() for x in level] for level in t.level_traversal()],
                         [['r'], ['e'], ['a','f'], ['b', 'c', 'd']])

if __name__ == '__main__':
    unittest.main()
