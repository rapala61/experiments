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
import sys

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
        profile = 0.0

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
        profile = s_end-s_start

        return {"match": found, "isWord": last_node.isWord, "suggestions": suggestions, "used": last_node.count, "profile": profile}

    # o(1) + (o(w) * o(1))
    def add_word(self, word):
        # o(1) --
        # store word length to know
        # which char node to mark "isWord"
        word_length = len(word)
        # Start searching at root
        current_node = self.root
        # Store prefix for each node to make
        # it easier to traverse later
        prefix = ''
        # o(1) -- end

        # For each character find if it exists in the trie
        # if not, add it as a child node
        # if it's, skip and point to it's node
        # o(w), word length
        for idx, char in enumerate(word, start=1):
            # o(1), it's constant because it will always lowercase
            # only one char
            char = char.lower()

            # o(1) --
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
            # o(1) -- end


#  Initialize

# o(1) --
trie = Trie()
words = set()
longest_word_len = 0
longest_word = ''
# o(1) -- end

# Ingest words into Trie

# o(1)
with open(os.path.abspath('./text/text.txt')) as lines:
    ingest_start = perf_counter()
    # o(l) where l are lines in the text file
    for line in lines:
        # o(w)
        no_spaces = line.strip()
        # o(1)
        if len(no_spaces) < 1:
            continue

        # o(ll) where "ll" is the line char length
        clean_str = re.sub('[{}]'.format(util.DIRTY_CHARS), "", no_spaces)
        # o(ll)
        tokens = clean_str.split(' ')
        # o(ln) where "ln" is the number of word tokens per line
        for word in tokens:
            # o(1) --
            word_length = len(word)
            words.add(word)
            if longest_word_len < word_length:
                longest_word_len = word_length
                longest_word = word
            # o(1) -- end

            # o(1) + (o(w) * o(1))
            trie.add_word(word)
    # o(1)
    ingest_end = perf_counter()
    # o(1)
    print('Took {:.2f} milliseconds to add all the words in the text file'.format((ingest_end-ingest_start)*1000))
# o(1)
print('longest word = {}\nlength longest word = {}\ntotal unique words = {:,}'.format(longest_word, longest_word_len, len(words)))


# Start CLI menu or Profile of the script by searching N times

# o(1) --
i_word = ''
args = sys.argv
args_len = len(args)
search_times = util.DEFAULT_SEARCH_TIMES
result = {}
# o(1) -- end

if args_len > 1:
    # o(1)
    profiles = []
    # input word
    # o(2w)
    i_word = args[1].strip().lower()

    # o(1) --
    if args_len == 3:
        i_times = int(args[2])
        search_times = i_times if i_times else search_times

    print(f'searching for "{i_word}" {search_times} times\n')
    # o(1) -- end

    # o(n), the amount of times we are profiling
    for _ in range(0, search_times):
        # TBD
        result = trie.search(i_word)
        # o(1)
        profiles.append(result.get('profile'))
    # o(1)
    if len(profiles) > 1:
        # o(log n) + o(1)
        result['profile'] = profile_avg = reduce(
            lambda x, y: x+y, profiles) / len(profiles)
    # o(1)
    util.show_result(result)

else:
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
        util.show_result(result)
