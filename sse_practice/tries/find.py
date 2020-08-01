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
        # o(1) --
        self.value = value
        self.prefix = prefix
        self.isWord = isWord
        self.map = dict()
        self.count = 0

        if isWord:
            self.count += 1
        # o(1) -- end

    # o(1)
    def increase_counter(self):
        self.count += 1


class Trie:


    def __init__(self):
        self.root = Node()

    # Gets suggestions, sorts them by occurrance
    # and returns total suggestions
    def get_suggestions(self, node, total=1):
        # TBD
        suggestions_dict = self.sort_suggestions(
            # o(c²)
            self.search_suggestions(node), total)
        # o(1)
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
    # last matched prefix character node
    # o(1) + o(c)*o(c-1) = o(1) + o(c²-c) = o(c²)
    def search_suggestions(self, node):
        # o(1) --
        paths = node.map
        isWord = node.isWord
        prefix = node.prefix
        count = node.count
        words = {}
        # o(1) -- end

        # if the node is valid
        if node:
            # o(1)
            if isWord:
                words[count] = prefix
            else:
                # o(c) where "c" is the number of child nodes
                for char_key in paths:
                    # o(1)
                    words.update(
                        # o(c-1)
                        self.search_suggestions(
                            paths.get(char_key)))
        # o(1)
        return words


    def search(self, word):
        # o(1) --
        s_start = perf_counter()
        nodes = []
        search_suggestions = False
        suggestions = []
        current_node = self.root
        found = ''
        profile = 0.0
        # o(1) -- end

        # o(w)
        for _chr in word:
            # o(1) --
            mapped_node = current_node.map.get(_chr)
            if mapped_node is None:
                search_suggestions = True
                break
            else:
                current_node = mapped_node
                nodes.append(current_node)
            # o(1) -- end

        # o(1)
        if not len(nodes):
            # o(1) --
            s_end = perf_counter()
            profile = s_end-s_start

            return {
                "match": found,
                "isWord": False,
                "suggestions": suggestions,
                "profile": profile}
            # o(1) -- end


        else:
            # o(1) --
            last_node = nodes[-1]

            if not last_node.isWord:
                search_suggestions = True
            # o(1) -- end

            # o(p log p) where p is the length of the matched prefix
            found = reduce(lambda x, y: x + y, map(lambda x: x.value, nodes))

            # I think this has something to do to the predecessor problem,
            # van Emde Boas trees and all that fun stuff. For now, let's do it
            # the naive way
            # o(1)
            if search_suggestions:
                # current_node is the node of the last matching character
                # we are going to get suggestions based on this node's map
                # o(1)
                if len(current_node.map) > 0:
                    # TBD
                    suggestions = self.get_suggestions(current_node, 3)

        # o(1) --
        s_end = perf_counter()
        profile = s_end-s_start

        return {"match": found, "isWord": last_node.isWord, "suggestions": suggestions, "used": last_node.count, "profile": profile}
        # o(1) -- end

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
        for idx, _chr in enumerate(word, start=1):
            # o(1), it's constant because it will always lowercase
            # only one char
            _chr = _chr.lower()

            # o(1) --
            prefix += _chr
            # If we can't find a match in the hash table,
            # proceed to create the node and add to hash table
            if current_node.map.get(_chr) is None:
                # Is this char the end of the word?
                if idx == word_length:
                    # Save the node with "isWord" = True
                    current_node.map[_chr] = Node(_chr.lower(), True, prefix)
                else:
                    # save the new node in the hash table
                    current_node.map[_chr] = Node(_chr.lower(), False, prefix)
                # move node pointer to new node
                current_node = current_node.map.get(_chr)
            # If found (Best case scenario)
            else:
                node = current_node.map.get(_chr)
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
    # o(ls) where ls are lines in the text file
    for line in lines:
        # o(l) where "l" is the line length
        _line = line.strip()
        # o(1)
        if len(_line) < 1:
            continue

        # o(l)
        clean_line = re.sub('[{}]'.format(util.DIRTY_CHARS), "", _line)
        # o(l)
        word_tokens = clean_line.split(' ')
        # o(ws) where "ws" is the number of word tokens per line
        for word in word_tokens:
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
        # o(log n) + o(1) where n is the amount of times we searched for a match
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
