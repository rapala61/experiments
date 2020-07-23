# Overview

This is an experimental script meant to practice the use of the Trie
data structure. [This](https://medium.com/basecs/trying-to-understand-tries-3ec6bede0014) post is a good read about it.

# Disclaimer

**Status**: Prototype

- There are plenty of opportunities to DRY code.
- No formal Time and Space complexity analysis has been run against this script.
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
