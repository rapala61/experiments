"""Find words using a Trie data structure

This is an experimental script meant to practice the use of the Trie
data structure. It works by ingesting all the words inside the included text.txt file.
It let's the user get a match (with some metadata about the word) or
a partial match with suggestions.

"""

import os
import re
import random
import string

from functools import reduce
from helpers import util
from termcolor import colored
from time import perf_counter

class Node:


    def __init__(self, value=None, isWord=False, prefix=''):
        self.value = value
        self.prefix = prefix
        self.isWord = isWord
        self.map = dict()
        self.count = 0

        if isWord:
            self.count += 1

    def increase_counter(self):
        self.count += 1 # O(1)


class Trie:


    def __init__(self):
        self.root = Node()

    # Gets suggestions, sorts them by occurrance
    # and returns total suggestions
    def get_suggestions(self, node, total=1):
        suggestions_dict = self.sort_suggestions(
            self.search_suggestions(node), total)
        return list(suggestions_dict)

    # Gets the top suggestions by amount of
    # times the word appears in the text
    def sort_suggestions(self, words=[], total=3):
        suggestions = {}
        count = len(words)
        weights = list(words)
        weights.sort(reverse=True)
        total = total if total <= count else count
        for i in range(total):
            suggestions[words.get(weights[i])] = weights[i]
        return suggestions

    # search by traversing down to all word leafs from the
    # last prefix character node matched
    def search_suggestions(self, node):
        paths = node.map
        isWord = node.isWord
        prefix = node.prefix
        count = node.count
        words = {}

        # if the node is valid
        if node:
            if isWord:
                words[count] = prefix
            else:
                for char_key in paths:
                    words.update(self.search_suggestions(
                        paths.get(char_key)))
        return words

    def search(self, word):
        s_start = perf_counter()
        nodes = []
        search_suggestions = False
        suggestions = []
        current_node = self.root
        found = ''

        for char in word:
            found_node = current_node.map.get(char)
            if found_node is None:
                search_suggestions = True
                break
            else:
                current_node = found_node
                nodes.append(current_node)

        if not len(nodes):
            return {"match": found, "suggestions": []}
        else:
            last_node = nodes[-1]

            if not last_node.isWord:
                search_suggestions = True

            found = reduce(lambda x, y: x + y, map(lambda x: x.value, nodes))

            # I think this has something to do to the predecessor problem,
            # van Emde Boas trees and all that fun stuff. For now, let's do it
            # the naive way
            if search_suggestions:
                # current_node is the node of the last matching character
                # we are going to get suggestions based on this node's map
                if len(current_node.map) > 0:
                    suggestions = self.get_suggestions(current_node, 3)

        s_end = perf_counter()
        print(
            'Took {:.2f} milliseconds to find word or suggest matches'.format((s_end-s_start)*1000))

        return {"match": found, "isWord": last_node.isWord, "suggestions": suggestions, "used": last_node.count}

    def add_word(self, word):
        # store word length to know
        # which char node to mark "isWord"
        word_length = len(word)
        # Start searching at root
        current_node = self.root
        # Store prefix for each node to make
        # it easier to traverse later
        prefix = ''
        # For each character find if it exists in the trie
        # if not, add it as a child node
        # if it's, skip and point to it's node
        for idx, char in enumerate(word, start=1):
            char = char.lower()
            prefix += char
            # If we can't find a match in the hash table,
            # proceed to create the node and add to hash table
            if current_node.map.get(char) is None:
                # Is this char the end of the word?
                if idx == word_length:
                    # Save the node with "isWord" = True
                    current_node.map[char] = Node(char.lower(), True, prefix)
                else:
                    # save the new node in the hash table
                    current_node.map[char] = Node(char.lower(), False, prefix)
                # move node pointer to new node
                current_node = current_node.map.get(char)
            # If found (Best case scenario)
            else:
                node = current_node.map.get(char)
                if node.isWord:
                    node.increase_counter()

                # just point to it's node
                current_node = node


#  Main

# o(1)
trie = Trie()
# o(1)
words = set()
# o(1)
longest_word_len = 0
# o(1)
longest_word = ''
# o(1)
with open(os.path.abspath('./text/text.txt')) as lines:
    ingest_start = perf_counter()
    # o(l) where l are lines in the text file
    for line in lines:
        # o(w)
        no_spaces = line.strip()
        if len(no_spaces) < 1:
            continue

        clean_str = re.sub('[{}]'.format(util.DIRTY_CHARS), "", no_spaces)
        tokens = clean_str.split(' ')

        for word in tokens:
            word_length = len(word)
            words.add(word)
            if longest_word_len < word_length:
                longest_word_len = word_length
                longest_word = word
            trie.add_word(word)
    ingest_end = perf_counter()
    print("Took {:.2f} milliseconds to add all the words in the text file".format((ingest_end-ingest_start)*1000))

print('longest word = {}\nlength longest word = {}\ntotal unique words = {:,}'.format(longest_word, longest_word_len, len(words)))

# o(1)
i_word = ''
# o(1)
print('{}'.format(colored("Type 'exit' to quit.", "red")))

# o(m) where m is the count of words typed while using the script
while i_word != 'exit':
    # o(1)
    i_word = input("\nType a word (or part of it) to see if it's contained in the text:  ")
    # str.strip = o(w) where 'w' is the length of i_word
    # See: https://stackoverflow.com/a/55114114/1522524
    # str.lower = o(w)
    # total = o(2w)
    i_word = i_word.strip().lower()

    # o(1)
    if i_word == 'exit':
        # o(1)
        print(colored('Bye!', "blue"))
        continue

    # TBD
    result = trie.search(i_word)

    # o(1)
    if result.get('isWord'):
        # o(1)
        print('{} is in the text! It is used {:,} times'.format(
            # o(1)
            colored(
                result.get('match'), "green", attrs=["bold"]),
            # o(1)
            result.get('used')))
    # o(1)
    elif not result.get('match'):
        # o(1)
        print('We did not find a match, sorry!')
    else:
        # o(1)
        print('We found a partial match: {}! Did you mean {}?'.format(
            colored(result.get('match'), "red", attrs=["bold"]), colored(', '.join(result.get('suggestions')), "grey", attrs=["bold"])))
