#!/usr/bin/env python

import argparse
from selenium import webdriver

def take_screenshot(driver,args):
    driver.set_window_size(args.width,args.height)
    driver.get(args.webpage)
    driver.save_screenshot(args.filename)


def main():

    #initialize phantomjs driver
    driver = webdriver.PhantomJS()

    parser = argparse.ArgumentParser(description="Take screenshots of web pages")
    parser.add_argument("-s", "--screenshot")
    parser.add_argument("-w", "--width", type=int,default=800,
                        help="browser width (default=800)")
    parser.add_argument("-H", "--height", type=int, default=600,
                        help="browser height (default=600)")
    parser.add_argument("--clipwidth", type=int, default=200,
                        help="width of clipped thumbnail (default=200)")
    parser.add_argument("--clipheight", type=int, default=150,
                        help="height of clipped thumbnail (default=150)")
    parser.add_argument("-wp", "--webpage", type=str,
                        help="webpage address")
    parser.add_argument("-f", "--filename", type=str, default="screen.png",
                        help="file name of saves screenshot (default=screen.png)")
    args = parser.parse_args()

    #TODO put required args into a group!
    if not args.webpage and args.filename:
        parser.print_help()
        driver.quit()
        return
    if args.screenshot:
        take_screenshot(driver,args)

    driver.quit()







if __name__ == '__main__' : main()
