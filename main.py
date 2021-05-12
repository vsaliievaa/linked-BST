"""Module for comparing search times for lists and binary trees."""


import time
from random import choice
from linkedbst import LinkedBST


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
    i, found = 0, 0
    start = time.time()

    for word in searchlist:
        if wordlist[i] == word:
            found += 1
        i += 1
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


if __name__ == "__main__":
    print("How many words should be searched? (up to 992): ", end="")
    num_words = int(input())
    print("Enter path to file with dictionary: ", end="")
    words = get_words(input())
    print("Performing search...")
    time.sleep(1)
    searchlist = create_searchlist(words)
    or_tree = create_ordered_bst(searchlist)
    unor_tree = create_unordered_bst(searchlist)
    print(f"Searched for {num_words} words in trees and a list of 1000 words.")
    print(f"Built-in list: {list_search_time(words, searchlist)}")
    print(
        f"Binary search tree (alphabetized, unbalanced): {ordered_bst_search_time(or_tree, searchlist)}")
    print(
        f"Binary search tree (unalphabetized, unbalanced): {unordered_bst_search_time(unor_tree, searchlist)}")
    print(
        f"Binary search tree (unalphabetized, balanced): {rebalanced_tree_search(or_tree, searchlist)}")
