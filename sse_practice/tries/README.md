# Overview

This is an experimental script meant to practice the use of the Trie
data structure. [This](https://medium.com/basecs/trying-to-understand-tries-3ec6bede0014) post is a good read about it.

# Disclaimer

What this script is **not**:
- A good example of the "best" implementation of the data structure.
- Modular or reusable, in fact, there is plenty of non DRY code, I know.
- Efficient or inefficient on purpose. No Time and Space complexity analysis has been run against this script.

What this script is (IMO):
- A good first step into practicing how to implement a solution
    using Tries as a data structure.
- First iteration after pseudocode
- Missing more comments
- Fun

# How To Use

```
    $ python find.py
    length longest word = 25
    total unique words = 8799
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
