# this module on GitHub:
"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import ceil, log
from random import choice
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        if self._root is None:
            self._root = BSTNode(item)

        current = self._root
        parent = None

        while current:
            parent = current
            if item < current.data:
                current = current.left
            else:
                current = current.right

        if item < parent.data:
            parent.left = BSTNode(item)
        else:
            parent.right = BSTNode(item)

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = newItem
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(self) + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = []
        for vert in self.inorder():
            if low <= int(vert) <= high:
                lst.append(int(vert))

        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = list(self.inorder())

        for vert in self.inorder():
            self.remove(vert)

        while len(nodes) != 0:
            mid = ceil((len(nodes)-1)/2)
            element = nodes[mid]
            self.add(nodes[mid])
            nodes.remove(element)

        return self

    def demo_bst(self, path, num_words):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def get_words(path):
            """Get words from a file at given path."""
            words, wordlist = [], []
            with open(path, "r", encoding='utf-8') as file:
                for line in file:
                    words.append(line.strip())

            for _ in range(1000):
                wordlist.append(choice(words))

            return wordlist

        def create_searchlist(wordlist):
            """Create a list of words to be searched."""
            searchlist = []
            for _ in range(num_words):
                searchlist.append(choice(wordlist))

            return searchlist

        def create_ordered_bst(wordlist):
            """Create a tree of 1000 ordered words."""
            tree = LinkedBST()
            wordlist = sorted(wordlist)
            for word in wordlist:
                tree.add(word)

            return tree

        def create_unordered_bst(wordlist):
            """Create a tree of 1000 unordered words."""
            tree = LinkedBST()
            for word in wordlist:
                tree.add(word)

            return tree

        def list_search_time(wordlist, searchlist):
            """Search necessary words in a built-in list."""
            found = 0
            start = time.time()

            for word in searchlist:
                for wrd in wordlist:
                    if wrd == word:
                        found += 1
                if found == len(searchlist):
                    break

            return time.time() - start

        def ordered_bst_search_time(or_tree, searchlist):
            """Search time in ordered tree."""
            start = time.time()
            for word in searchlist:
                or_tree.find(word)

            return time.time() - start

        def unordered_bst_search_time(unor_tree, searchlist):
            """Search time in unordered tree."""
            start = time.time()
            for word in searchlist:
                unor_tree.find(word)

            return time.time() - start

        def rebalanced_tree_search(tree, searchlist):
            """Rebalance an unordered tree and calculate its search time."""
            tree = tree.rebalance()
            start = time.time()
            for word in searchlist:
                tree.find(word)

            return time.time() - start

        words = get_words(path)
        time.sleep(1)
        searchlist = create_searchlist(words)
        or_tree = create_ordered_bst(searchlist)
        unor_tree = create_unordered_bst(searchlist)
        print(
            f"Searched for {num_words} words in trees and a list of 1000 words.")

        print(f"Built-in list: {list_search_time(words, searchlist)}")
        print(
            f"Binary search tree (alphabetized, unbalanced): \
{ordered_bst_search_time(or_tree, searchlist)}")
        print(
            f"Binary search tree (unalphabetized, unbalanced): \
{unordered_bst_search_time(unor_tree, searchlist)}")
        print(
            f"Binary search tree (unalphabetized, balanced): \
{rebalanced_tree_search(or_tree, searchlist)}")


if __name__ == "__main__":
    print("How many words should be searched? (up to 992): ", end="")
    num_words = int(input())
    print("Enter path to file with dictionary: ", end="")
    path = input()
    tree = LinkedBST()
    tree.demo_bst(path, num_words)
