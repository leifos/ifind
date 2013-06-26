#!/usr/bin/env python
"""
Take & crop screenshots of web pages, save them to disk
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   24/06/2013
Version: 0.1

Usage:
------
    ./capture_screenshot.py [options...]
        -wp,  --webpage         specify an url address
        -w,   --width           width of browser window
        -H,   --height          height of browser window
        -f,   --filename        name of screen shot to be save,
                                use full paths. .jpeg and .png
                                are acceptable formats.
"""
import argparse
from ifind.common.pagecapture import PageCapture

def main():

    parser = argparse.ArgumentParser(
                                description="Take screenshots of web pages")
    parser.add_argument("-w", "--width", type=int,default=800,
                        help="browser width (default=800)")
    parser.add_argument("-H", "--height", type=int, default=600,
                        help="browser height (default=600)")
    parser.add_argument("-wp", "--webpage", type=str,
                        help="webpage address")
    parser.add_argument("-f", "--filename", type=str, default="screen.png",
                        help="filename of saved screenshot (default=screen.png)"
                              "\nexpected format: .jpeg or .png")
    args = parser.parse_args()

    if not args.webpage and args.filename:
        parser.print_help()
        return 2
    else:
        pc = PageCapture(args.webpage,args.width,args.height)
        pc.take_screen_shot(args.filename)
        title = pc.get_page_title()
        print "Screen shot of %s taken and saved to %s." % (title, args.filename)
        return 0

if __name__ == '__main__':
    main()
