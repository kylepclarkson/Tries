
from tree.Tree import Tree

class TrieEntry:

    def __init__(self, key, startIdx, endIdx):
        self.key = key
        self.startIdx = startIdx
        self.endIdx = endIdx

    def __repr__(self):
        return f'key: {self.key} [{self.startIdx},{self.endIdx}]'

class Trie(Tree):

    __slots__ = '_tree', '_word_count', '_word_dict'
    def __init__(self):
        super(Trie, self).__init__()
        self._word_count = 0
        self._word_dict = {}
        # ASCII null termination character. Used to denote end of string.
        self._TERMINATION_CHARACTER = chr(0)

    def insert(self, input_word):
        '''
        :param input_word: The word to insert into the tree.
        :return:
        '''

        input_word += self._TERMINATION_CHARACTER
        self._word_dict[self._word_count] = input_word
        # The position to insert input_word at within the trie.
        pos = self.find_insertion_position(self.root(), input_word)

        # Special case, add at root.
        if pos == self.root():
            self.add(pos, TrieEntry(self._word_count, 0, len(input_word)))
        else:
            start = pos.element().startIdx
            pos_str = self._word_dict[pos.element().key]
            # find end index where input_word[start:end] matches string stored in pos.
            end = start
            while input_word[start:end+1] == pos_str[start:end+1]:
                end += 1

            if end == pos.element().endIdx:
                # The string at pos fully matches insertion word, create a single new position as a child of pos..
                self.add(pos, TrieEntry(self._word_count, end, len(input_word)))
            else:
                # The string at pos partially matches input_word, add a position between pos and its parent.
                # This between position contains the string that matches between the two.
                # insert new position between pos and its parent.
                new_pos = self.add_between(self.parent(pos), pos,
                                           TrieEntry(pos.element().key, pos.element().startIdx, end))
                # update previous start index.
                pos.element().startIdx = end
                # insert new position as child of between position. This position contains the string
                # that does not match the string at pos and input_word.
                self.add(new_pos, TrieEntry(self._word_count, end, len(input_word)))

        self._word_count += 1

    def find_insertion_position(self, pos, input_word):
        '''
        Determines the position in the trie to insert a new word.
        :param pos: Search for insertion at this position.
        :param input_word: The string to insert into the trie.
        :return: The position to insert input_word at.
        '''
        for child in self.children(pos):
            # The string for this position.
            pos_str = self._word_dict[child.element().key]
            start = child.element().startIdx
            end = child.element().endIdx

            if pos_str[start] == input_word[start]:
                # This child's string matches the the input at the start position.
                if pos_str[start:end] == input_word[start:end]:
                    # A full match, continue searching for the insertion position.
                    return self.find_insertion_position(child, input_word)
                else:
                    # A partial match, insert at this position.
                    return child
        # no child contains a matching string, insert at the position.
        return pos
