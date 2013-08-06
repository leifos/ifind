from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
#from ifind.models.game_model_functions import populate
from ifind.models.deployment_population_script import populate


from configuration import  STATIC_PATH
import argparse
import os


def main():

    parser = argparse.ArgumentParser(description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=bool,default=False, help="")
    parser.add_argument("-cn", "--category_name", type=str, help="The name of the category")
    parser.add_argument("-fn", "--file_name", type=str, help="The name of the file where the urls are stored in")
    parser.add_argument("-hss", "--halved_screen_shot", default=True, type=bool, help="")
    parser.add_argument("-icl", "--is_command_line", default=False, type=bool, help="")
    args = parser.parse_args()
    if not args.file_name and args.category_name:
        parser.print_help()
        return 2

    else:
        import doctest
        test_results = doctest.testmod()
        print test_results
        if not test_results.failed:
            if args.is_command_line:
                populate(args.file_name, args.category_name, args.append, args.halved_screen_shot)
                print "Category and pages have been populated"
            else:
                populate2(os.getcwd() + '/data/research', 'research', False, True ,os.path.join(STATIC_PATH,'imgs/research.jpg'))
                populate2(os.getcwd() + '/data/about_glasgow', 'about glasgow', False, True , os.path.join(STATIC_PATH,'imgs/about_glasgow.jpg'))
                populate2(os.getcwd() + '/data/undergraduate', 'undergraduate', False, True ,os.path.join(STATIC_PATH,'imgs/undergraduate.jpg'))
                populate2(os.getcwd() + '/data/postgraduate', 'postgraduate', False, True ,os.path.join(STATIC_PATH,'imgs/postgraduate.jpg'))
                populate2(os.getcwd() + '/data/alumni', 'alumni', False, True ,os.path.join(STATIC_PATH,'imgs/alumni.png'))
                populate2(os.getcwd() + '/data/studentlife', 'student life', False, True, os.path.join(STATIC_PATH,'imgs/student_life.jpg'),)
        return 0

if __name__ == '__main__':
    main()
