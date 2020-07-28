# Overview

This is an experimental script meant to practice the use of the Trie
data structure. [This](https://medium.com/basecs/trying-to-understand-tries-3ec6bede0014) post is a good read about it.

# Performance Profile

The search time for the characters below was profiled by taking the average of running each search **10,000 times**. The discrepancy in times (e.g. the "c" char) are due to the amount of words that start
with that character in the text. The higher the amount, the more nodes the DFS algorithm has to visit starting from the "a".

| Function | input	| Naive ~ time (ms) | W/ optimizations ~ time (ms) |
|---|---|---|---|
| adding all the words in the [.txt](./text/text.txt) file | 16,217 lines| 700|
| search | a| 0.9 |
| search | e| 0.7 |
| search | i| 0.8 |
| search | o| 0.25 |
| search | u| 0.3 |
| search | b| 0.4 |
| search | c| 1.3 |
| search | d| 0.8 |
| search | f| 0.55 |
| search | g| 0.3 |
| search | h| 0.5 |
| search | j| 0.1 |
| search | k| 0.1 |
| search | l| 0.3 |
| search | m| 0.6 |
| search | n| 0.2 |
| search | p| 1 |
| search | q| 0.05 |
| search | r| 0.6 |
| search | s| 1 |
| search | t| 0.4 |
| search | v| 0.2 |
| search | w| 0.2 |
| search | x| 0 |
| search | y| 0 |
| search | z| 0 |

# Disclaimer

**Status**: Prototype

- There are plenty of opportunities to DRY code.
- Some Time and Space complexity analysis has been done, but no substantive optimizations have been applied.
- It's a good first step into practicing how to implement a solution using Tries as a data structure.

# How To Use

### Prerequisites

> Use of pyenv to manage multiple Python versions is recommended

- Navigate to the `tries` directory.
- Run `pipenv install`

### CLI

- Run `python find.py`
- Type the word you are searching for at the prompt, e.g. "hi":
    ```
    Type a word (or part of it) to see if it's contained in the text:  hi
    ```
- The script will attempt to locate the word and give you some info on it.
- Type `exit` to quit.
    ```
    Type a word (or part of it) to see if it's contained in the text:  exit
    Bye!
    ```

#### Example
```
    $ python find.py
    length longest word = 25
    total unique words = 8,799
    Type 'exit' to quit.

    Partial Match:

        Type a word (or part of it) to see if it's contained in the text:  hi
        We found a partial match: hi! Did you mean highly?

    Match:

        Type a word (or part of it) to see if it's contained in the text:  the
        the is in the text! It is used 13,036 times

    No Match:

        Type a word (or part of it) to see if it's contained in the text:  12
        We did not find a match, sorry!
```

# Technical details

Used Python 3.8.3

# License
GNU General Public License v3.0 or later

See [COPYING](../../COPYING) to see the full text.
