import unittest

from trie.Trie import Trie

class TestTrie(unittest.TestCase):


    def test_create_trie_1(self):
        trie = Trie()
        trie.insert_word("meet")
        trie.insert_word("met")
        trie.insert_word("meat")
        trie.insert_word("maybe")
        trie.insert_word("may")
        trie.insert_word("adam")
        print(f'tree size: {len(trie)}')
        for level in trie.level_traversal():
            print(level)

    def test_tree_search(self):
        trie = Trie()
        trie.insert_word("meet")
        trie.insert_word("met")
        trie.insert_word("meat")
        trie.insert_word("maybe")
        trie.insert_word("may")
        trie.insert_word("adam")

        self.assertIsNotNone(trie.find_word("meet"))
        self.assertIsNotNone(trie.find_word("may"))
        self.assertIsNone(trie.find_word("mep"))

