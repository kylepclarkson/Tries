
from tree.Tree import Tree

class TrieEntry:

    def __init__(self, key, startIdx, endIdx):
        self.key = key
        self.startIdx = startIdx
        self.endIdx = endIdx


class Trie(Tree):

    __slots__ = '_tree', '_word_count', '_word_dict'
    # TODO handle insertion pos is root. 
    def __init__(self):
        super(Trie, self).__init__(TrieEntry(chr(0), 0, 0))
        self._word_count = 0
        self._word_dict = {}
        # ASCII null termination character. Used to denote end of string.
        self._TERMINATION_CHARACTER = chr(0)

    def insert(self, word):
        '''
        :param word: The word to insert into the tree.
        :return:
        '''
        # Insert word into trie dictionary.
        self._word_count += 1
        word += self._TERMINATION_CHARACTER
        self._word_dict[self._word_count] = word

        pos = self.find_insertion_position(self.root(), word)

        pos_entry = pos.element()
        start = pos_entry.startIdx
        pos_str = self._word_dict[pos_entry.key]
        # find end index where word[start:end] matches string stored in pos.
        end = start
        while (word[start:end] == pos_str[start:end]):
            end+=1

        # create new child of pos to store remainder of existing word.
        self._add(pos, TrieEntry(pos_entry.key, end, pos_entry.endIdx))
        # create new child of pos to store remainder of new word.
        self._add(pos, TrieEntry(self._word_count, end, len(word)))
        # update pos to contain the shared substring between existing and new word.
        pos_entry.endIdx = end


    def find_insertion_position(self, pos, input_string):
        '''
        :param pos: Search for insertion at this position.
        :param string: The string to insert into the trie.
        :return: The position to insert string into.
        '''
        for child in self.children(pos):
            # The string for this position.
            pos_str = self._word_dict[child.element().key]
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
