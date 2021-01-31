
from tree.Tree import Tree

class Entry:

    def __init__(self, key, startIdx, endIdx):
        self.key = key
        self.startIdx = startIdx
        self.endIdx = endIdx


class Trie:

    __slots__ = '_tree', '_count', '_words'

    # ASCII null termination character. Used to denote end of string.
    NIL = chr(0)

    def __init__(self):
        self._tree = Tree(None)
        # Root of tree.
        self._tree._add(None)
        self._count = 0
        self._words = {}

    def insert(self, word):
        """ Insert word into trie. """
        self._count += 1
        self._words[self._count] = word

    def find_insertion_position(self, pos, string):
        '''
        :param pos: Search for insertion at this position.
        :param string: The string to insert into the trie.
        :return: The position to insert string into.
        '''
        for children in self._tree.children(pos):
            pass
            '''
            TODO for each child node, check if string[0] matches first character of
            the string "stored" at the child node
            '''
