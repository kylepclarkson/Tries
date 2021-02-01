
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

    def insert(self, word):
        '''
        :param word: The word to insert into the tree.
        :return:
        '''
        # Insert word into trie dictionary.
        word += self._TERMINATION_CHARACTER
        self._word_dict[self._word_count] = word

        pos = self.find_insertion_position(self.root(), word)
        print(f'insert {word}. entry found: {pos.element()}')
        if pos == self.root():
            self.add(pos, TrieEntry(self._word_count, 0, len(word)))
        else:
            start = pos.element().startIdx
            pos_str = self._word_dict[pos.element().key]
            # find end index where word[start:end] matches string stored in pos.
            end = start+1
            while word[start:end] == pos_str[start:end]:
                end += 1
            end -= 1
            if end == pos.element().endIdx:
                # The string at pos fully matches insertion word, create a single new position.
                self.add(pos, TrieEntry(self._word_count, start, end))
            else:
                # The string at pos does not fully match, add an between node and new node.
                # insert new node between pos and its parent.
                new_pos = self.add_between(self.parent(pos), pos,
                                           TrieEntry(pos.element().key, pos.element().startIdx, end))
                # update previous start index.
                pos.element().startIdx = end
                # insert new node for remainder of new word.
                self.add(new_pos, TrieEntry(self._word_count, end, len(word)))
            """
                TODO
                if substring at pos fully matches the corresponding substring of the new word,
                    just create a new node for the remainder of the new word.
                Otherwise, need to preform add_between operation, with new node containing the matching substring.
            """


            # create new child of pos to store remainder of existing word.
            # self.add(pos, TrieEntry(pos_entry.key, end-1, pos_entry.endIdx))
            # # create new child of pos to store remainder of new word.
            # self.add(pos, TrieEntry(self._word_count, end-1, len(word)))
            # # update pos to contain the shared substring between existing and new word.
            # pos.element().endIdx = end-1


        self._word_count += 1

    def find_insertion_position(self, pos, input_string):
        # TODO double check insertion logic.
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
                # print(f'start: {type(start)} end: {type(end)}')
                # String at this position fully matches part of
                # input string, continue search for position.
                if pos_str[start:end] == input_string[start:end]:
                    return child
                    # return self.find_insertion_position(child, input_string)

                return self.find_insertion_position(child, input_string)

        # insert at this position
        return pos
