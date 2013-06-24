import argparse
from ifind.common.pagecapture import PageCapture

def main():

    parser = argparse.ArgumentParser(description="Take screenshots of web pages")
    parser.add_argument("-w", "--width", type=int,default=800,
                        help="browser width (default=800)")
    parser.add_argument("-H", "--height", type=int, default=600,
                        help="browser height (default=600)")
    parser.add_argument("-wp", "--webpage", type=str,
                        help="webpage address")
    parser.add_argument("-f", "--filename", type=str, default="screen.png",
                        help="filename of saved screenshot (default=screen.png)")
    args = parser.parse_args()

    #TODO put required args into a group!
    if not args.webpage and args.filename:
        parser.print_help()
        return 2
    else:
        pc = PageCapture(args.webpage,800,600)
        pc.take_screen_shot(args.filename, args.height, args.width)
        title = pc.get_page_title
        print "Screen shot of %s taken and saved to %s." % (title, args.filename)
        return 0


if __name__ == '__main__':
    main()
