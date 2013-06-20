__author__ = 'leifos'
__date__ = '2013-06-20'

import sys

def usage(argv):
    '''
    Prints the script's usage details to the console.
    '''
    print "Usage:"
    print "  %s url name height width " % (argv[0])


def take_screenshot(url, name='img.jpg', width=600, height=400):
    '''
        Args: takes a valid url string,
        the name of the file the screen is to be saved as
        width of the screen shot in pixels
        height of the screen shot in pixels

        Returns:
            None
    '''


def is_url_valid(url):
    """
    Args:
        url: a url string
    Returns:
        True if it is a valid url string, else False
    """

    pass


def main(argv = None):
    '''
    '''
    if argv is None:
        argv = sys.argv

    url = None
    name = "img.jpg"
    width = 600
    height = 400
    # extract args from command line
    if len(argv) >= 2:
        url = argv[1]

        take_screenshot(url,)
        return 0
    else: # Invalid number of command-line arguments, print usage
        usage(argv)
        return 2

if __name__ == '__main__':
    sys.exit(main())