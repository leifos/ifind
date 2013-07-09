from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from ifind.models.game_model_functions import populate
import argparse
import os


def main():

    parser = argparse.ArgumentParser(description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=bool,default=False, help="")
    parser.add_argument("-cn", "--category_name", type=str, default='engineering', help="The name of the category")
    parser.add_argument("-fn", "--file_name",default= os.getcwd() + '/data/urls.txt', type=str, help="The name of the file where the urls are stored in")
    parser.add_argument("-hss", "--halved_screen_shot", default=True, type=bool, help="")
    args = parser.parse_args()
    if not args.file_name and args.category_name:
        parser.print_help()
        return 2

    else:
        import doctest
        test_results = doctest.testmod()
        print test_results
        if not test_results.failed:
            populate(args.file_name, args.category_name, args.append, args.halved_screen_shot)
            print "Category and pages have been populated"
        return 0

if __name__ == '__main__':
    main()
