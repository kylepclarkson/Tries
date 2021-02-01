import unittest

from trie.Trie import Trie

class TestTrie(unittest.TestCase):


    def test_create_trie_1(self):
        trie = Trie()
        trie.insert("meet")
        trie.insert("met")
        trie.insert("meat")
        trie.insert("maybe")
        # trie.insert("may")
        # trie.insert("adam")
        print(f'tree size: {len(trie)}')
        for level in trie.level_traversal():
            print(level)
