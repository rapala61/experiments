from termcolor import colored






# Custom string.punctuation
DIRTY_CHARS = r"""!"#$%&()*+,./:;<=>?@[\]^_`{|}~\d"""
DEFAULT_SEARCH_TIMES = 1000


def show_result(result):
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

    if result.get('profile'):
        print(
            'Took {:.2f} milliseconds to find word or suggest matches'.format(result.get('profile') * 1000))
