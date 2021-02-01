

class TreeADT:
    """Abstract class for Tree data structure. """

    # === Nest Position class (Container for node) ===
    class Position:
        """An abstracting representing a node of the tree. """

        def element(self):
            raise NotImplementedError()

        def __eq__(self, other):
            raise NotImplementedError()

        def __ne__(self, other):
            return not (self == other)

    # === Abstract methods to be implemented by subclass ===
    def root(self):
        raise NotImplementedError()

    def parent(self, pos):
        raise NotImplementedError()

    def children(self, pos):
        # Generate an iteration of Positions representing pos' children.
        raise NotImplementedError()

    def num_children(self, pos):
        raise NotImplementedError()

    def __len__(self):
        """Number of elements in tree."""
        raise NotImplementedError()

    # === Class methods ===
    def is_root(self, pos):
        return self.root() == pos

    def is_leaf(self, pos):
        return self.num_children(pos) == 0

    def is_empty(self):
        return len(self) == 0

    def height(self, pos=None):
        """ Return height of tree rooted at pos."""
        if pos is None:
            pos = self.root()
        if self.is_leaf(pos):
            return 0
        else:
            return 1 + max(self.height(c) for c in self.children(pos))

""" 
 ================ The Tree data structure. ================
 
 Implements from Tree interface defined above.
 Each node stores an element, a reference to its parent, and a dictionary for its children,
    where a key is the node of the child and the value the edge.  
 
 The user is allowed to access Position instances publicly, while Node instances are private and
    used within the data structure only. Functions _validate and _make_position handle converting
    a position to a node instance and a node to a position instance respectively. 
 ==========================================================
"""


class Tree(TreeADT):
    class _Node:
        """ A nonpublic wrapper for storing a node. """
        __slots__ = '_element', '_parent', '_children'

        def __init__(self, element, parent=None, children=None):
            self._element = element
            self._parent = parent
            self._children = {} \
                if children is None\
                else children

        def __repr__(self):
            return  str(self._element)

    # === An abstract representation of a element in the tree.
    class Position(TreeADT.Position):

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __repr__(self):
            return str(self._node)
    # === End Position Class ===

    # ================ Wrapper Functions ================
    def _validate(self, pos):
        """Unpack node from position, if it is valid.
        Returns _Node object.
        """
        if not isinstance(pos, self.Position):
            raise TypeError("pos must be of Position type. pos type:", type(pos))

        if pos._container is not self:
            raise ValueError('pos does not belong to this container')

        # convention: when removing a node, set its parent to itself.
        if pos._node._parent is pos._node:
            raise ValueError('pos is no longer valid')

        return pos._node

    def _make_position(self, node):
        """Pack node into position instance (or None if no node.)
        Returns Position object.
        """
        return self.Position(self, node) if node is not None else None
    # ================ End wrapper functions ================


    # ================ Constructors ================
    def __init__(self, e=None):
        """ Create tree with root element e. """
        self._root = None
        self.add_root(e)

    def __len__(self) -> int:
        return self._size

    # ================ Accessors functions ================
    def root(self) -> Position:
        """ Return root Position of tree. """
        return self._make_position(self._root)

    def parent(self, pos: Position) -> Position:
        """ Return the Position of pos' parent. """
        node = self._validate(pos)
        return self._make_position(node._parent)

    def children(self, pos: Position) -> list:
        """ Generate the children of Position pos. """
        node = self._validate(pos)
        return [self._make_position(child) for child in node._children.keys()]

    def num_children(self, pos: Position) -> int:
        node = self._validate(pos)
        return len(node._children)

    def is_child(self, pos: Position) -> bool:
        return self.num_children(pos) == 0


    # ================ Insert functions ================
    def add_root(self, e) -> Position:
        """ Place element e at root of empty tree. """
        if self._root is not None:
            raise ValueError('Root exists')

        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def add(self, pos: Position, e) -> Position:
        """ Create new child for Position pos with element e.
        Return the Position of new node.
        """
        parent_node = self._validate(pos)
        self._size += 1
        child = self._Node(e, parent_node)
        # add child to parent node
        parent_node._children[child] = child

        return self._make_position(child)

    def add_between(self, par_pos: Position, child_pos: Position, e) -> Position:
        '''
        Create a new node in between a parent node and a child node.
        :param par_pos:     The parent position.
        :param child_pos:   The child position.
        :param e:           The element to insert
        :return:            The position of the new node.
        '''

        parent_node = self._validate(par_pos)
        child_node = self._validate(child_pos)

        # Check that parent node is indeed parent of child node.
        if child_node._parent != parent_node:
            raise ValueError('parent pos is not parent of child pos:', parent_node._element, child_node._element)

        # remove child node from parent node's children
        del parent_node._children[child_node]
        # create new between node. Link to existing nodes.
        between_node = self._Node(e, parent_node)
        parent_node._children[between_node] = between_node
        between_node._children[child_node] = child_node
        child_node._parent = between_node
        self._size += 1
        return self._make_position(between_node)




    def replace(self, pos: Position, e):
        """ Replace element at Position pos with e.
        Return the old element.
        """
        node = self._validate(pos)
        old = node._element
        node._element = e
        return old

    def remove(self, pos: Position):
        """ Remove the node at Position pos.
        If pos has a single child, make the child's parent pos.
        If pos has more than one child, throw error.
        Return element that was stored at pos.
        """
        node = self._validate(pos)

        if self.num_children(pos) > 1:
            raise ValueError('pos have more than one child:', pos._node._element, list(pos._node._children.values()))

        # node is a leaf node
        if len(node._children) == 0:
            if not node is self._root:
                del node._parent._children[node]    # delete node from children dict.
            node._parent = node     # deprecate node.
            self._size -= 1
            return node._element

        # node is an internal node with one child.
        else:
            child = list(node._children.values())[0]
            # node is root node (i.e. does not have parent.)
            if node is self._root:
                self._root = child
            # node has parent node
            else:
                parent = node._parent
                parent._children[child] = child
                del parent._children[node]  # delete node from children dict.
                print("parent node: ", parent)
                print('parent node children: ', parent._children)

            self._size -= 1
            node._parent = node         # deprecate node.
            return node._element

    def attach_at(self, pos: Position, tree) -> None:
        """ Insert root of 'tree' as child of pos.
            Set tree instance to none after insertion.
        """
        parent_node = self._validate(pos)

        if not type(self) is type(tree):
            raise TypeError(f'Trees are not of same type. Self type: {type(self)}, tree type: {type(tree)}')

        self._size += len(tree)

        if not tree.is_empty():
            root_tree_node = tree._root
            root_tree_node._parent = parent_node
            parent_node._children[root_tree_node] = root_tree_node
            tree._root = None   # set tree instance to none.
            tree._size = 0

    def delete_tree(self):
        if not self.is_empty():
            for pos in self.postorder():
                self.remove(pos)

    # ================ Tree Traversal ================
    def preorder(self):
        """ Generate a preorder traversal of Positions in tree."""
        if not self.is_empty():
            for pos in self._subtree_preorder(self.root()):
                yield pos

    def _subtree_preorder(self, pos: Position):
        """ Generate a preorder traversal of Positions in subtree at pos."""
        yield pos
        for child in self.children(pos):
            for child_child in self._subtree_preorder(child):
                yield child_child

    def postorder(self):
        """ Generate a postorder traversal of Positions in tree."""
        if not self.is_empty():
            for pos in self._subtree_postorder(self.root()):
                yield pos

    def _subtree_postorder(self, pos: Position):
        for child in self.children(pos):
            for child_child in self._subtree_postorder(child):
                yield child_child
        yield pos

    def bfs(self):
        """ Generate a breadth-first iteration of Positions in tree."""
        if not self.is_empty():
            queue = []
            queue.append(self.root())

            while len(queue) != 0:
                pos = queue.pop(0)
                yield pos
                for child in self.children(pos):
                    queue.append(child)

    def dfs(self):
        """ Generate a depth-first iteration of Positions in tree."""
        if not self.is_empty():
            stack = []
            stack.append(self.root())

            while len(stack) != 0:
                pos = stack.pop()
                yield pos
                for child in self.children(pos):
                    stack.append(child)
