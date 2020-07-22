"""Find words using a Trie data structure

This is an experimental script meant to practice the use of the Trie
data structure. It works by ingesting all the words inside the included text.txt file.
It let's the user get a match (with some metadata about the word) or
a partial match with suggestions.

"""

import os
import re
import string
import random
import helpers.util

from functools import reduce
from termcolor import colored, cprint

class Node:


    def __init__(self, value=None, isWord=False):
        self.value = value
        self.isWord = isWord
        self.map = dict()
        self.count = 0

        if isWord:
            self.count += 1

    def increase_counter(self):
        self.count += 1


class Trie:


    def __init__(self, root):
        self.root = root
        self.words = []


    # TODO: I should have a way to return more that 1 suggestion.
    def get_suggestion(self, node, parent_char=''):
        word = parent_char

        if node is None:
            return ''

        paths = node.map
        paths_len = len(paths)

        if not paths_len:
            if not node.isWord:
                # print("Error. Leaf is not marked as word.")
                return ''
            else:
                word += '|'
        else:
            if not node.isWord:
                key = list(paths.keys())[0]
                word += self.get_suggestion(paths.get(key), key)
        return word


    def search(self, word):
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
                    children = self.get_suggestion(current_node)
                    tokens = filter(lambda x: x, children.split('|'))
                    suggestions = list(map(lambda x: found + x if x else '' , tokens))

        return {"match": found, "isWord": last_node.isWord, "suggestions": suggestions, "used": last_node.count}

    def add_word(self, word):
        # store word length to know
        # which char node to mark "isWord"
        word_length = len(word)
        # Start searching at root
        current_node = self.root
        # For each character find if it exists in the trie
        # if not, add it as a child node
        # if it's, skip and point to it's node
        for idx, char in enumerate(word, start=1):
            char = char.lower()
            # If we can't find a match in the hash table,
            # proceed to create the node and add to hash table
            if current_node.map.get(char) is None:
                # Is this char the end of the word?
                if idx == word_length:
                    # Save the node with "isWord" = True
                    current_node.map[char] = Node(char.lower(), True)
                else:
                    # save the new node in the hash table
                    current_node.map[char] = Node(char.lower())
                # move node pointer to new node
                current_node = current_node.map.get(char)
            # If found (Best case scenario)
            else:
                node = current_node.map.get(char)
                if node.isWord:
                    node.increase_counter()

                # just point to it's node
                current_node = node


trie = Trie(Node())
words = set()
longest_word = 0

with open(os.path.abspath('./text/text.txt')) as lines:

    for line in lines:
        no_spaces = line.strip().rstrip()
        if len(no_spaces) < 1:
            continue

        # Custom string.punctuation
        clean_str = re.sub('[{}]'.format(r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~\d"""), "", no_spaces)
        tokens = clean_str.split(' ')

        for word in tokens:
            word_length = len(word)
            words.add(word)
            if longest_word < word_length:
                longest_word = word_length
            trie.add_word(word)

print('length longest word = {}\ntotal unique words = {}'.format(longest_word, len(words)))


i_word = ''
print('{}'.format(colored("Type 'exit' to quit.", "red")))

while i_word != 'exit':
    i_word = input("\nType a word (or part of it) to see if it's contained in the text:  ")
    i_word = i_word.strip()

    if i_word.lower() == 'exit':
        print(colored('Bye!', "blue"))
        continue

    result = trie.search(i_word)

    if result.get('isWord'):
        print('{} is in the text! It is used {:,} times'.format(
            colored(result.get('match'), "green", attrs=["bold"]), result.get('used')))
    elif not result.get('match'):
        print('We did not find a match, sorry!')
    else:
        print('We found a partial match: {}! Did you mean {}?'.format(
            colored(result.get('match'), "red", attrs=["bold"]), colored(', '.join(result.get('suggestions')), "grey", attrs=["bold"])))
