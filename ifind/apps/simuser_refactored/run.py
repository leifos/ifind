import sys
from sim_user import SimulatedUser
from config_reader.reader import ConfigReader

def main(config_filename):
    config_reader = ConfigReader(config_filename)
    components = config_reader.get_components_dictionary()
    
    user = SimulatedUser(search_context=components['search_context'],
                         decision_maker=components['decision_maker'],
                         logger=components['logger'],
                         document_classifier=components['document_classifier'],
                         snippet_classifier=components['snippet_classifier'])
    
    while not components['logger'].is_finished():
        user.decide_action()
    
    user.save_relevance_judgments('test.out')

if __name__ == '__main__':
    if len(sys.argv) < 2 and len(sys.argv) > 2:
        print 'You need to supply a configuration file, too'
    else:
        main(sys.argv[1])