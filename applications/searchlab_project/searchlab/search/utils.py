import string


def check_input(input_string):
    """
    Takes a unicode string, encodes it to ascii
    whilst stripping out the punctuation.

    Returns cleaned string or None if string
    contains nothing/spaces.

    """
    # encode to ascii, ignoring non ascii chars
    s = input_string.encode('ascii', 'ignore')

    # remove all punctuation
    s = s.translate(string.maketrans("",""), string.punctuation)

    # set to None if just spaces
    if s.isspace():
        s = None

    return s