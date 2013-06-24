__author__ = 'leif'

def convert_url_to_filename(url):
    """Take a url string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    >>> convert_url_to_filename("http://www.google.com")
    www-google-com
    >>> convert_url_to_filename("http://www.dcs.gla.ac.uk/~leif/index.html")
    www-dcs-gla-ac-uk-leif-index-html
    """

    pass


if '__name__' == '__main__':
    import doctest
    test_results = doctest.testmod()
    print test_results

