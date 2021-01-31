
from tree.Tree import Tree

class TrieEntry:

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
        '''
        :param word: The word to insert into the tree.
        :return:
        '''
        # Insert word into trie dictionary.
        self._count += 1
        self._words[self._count] = word
        pos = self.find_insertion_position(self._tree.root(), word)
        start = pos.element().startIdx
        pos_str = self._words[pos.element().key]
        # find end index where word[start:end] matches string stored in pos.
        end = start
        while (word[start:end] == pos_str[start:end]):
            end+=1


        # create new node






    def find_insertion_position(self, pos, input_string):
        '''
        :param pos: Search for insertion at this position.
        :param string: The string to insert into the trie.
        :return: The position to insert string into.
        '''
        for child in self._tree.children(pos):
            # The string for this position.
            pos_str = self._words[child.element().key]
            if pos_str[0] == input_string[0]:
                start = child.element().startIdx
                end = child.element().endIdx
                # String at this position fully matches part of
                # input string, continue search for position.
                if pos_str[start:end] == input_string[start, end]:
                    return self.find_insertion_position(child, input_string)

                return child

        # insert at this position
        return pos
