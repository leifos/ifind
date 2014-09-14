import sys
from sim_user import SimulatedUser
from config_readers.simulation_config_reader import SimulationConfigReader

def main(config_filename):
    
    config_reader = SimulationConfigReader(config_filename)
    
    for configuration in config_reader:
        user = SimulatedUser(search_context=configuration.user.search_context,
                             decision_maker=configuration.user.decision_maker,
                             logger=configuration.logger,
                             document_classifier=configuration.user.document_classifier,
                             snippet_classifier=configuration.user.snippet_classifier)
        
        while not configuration.logger.is_finished():
            user.decide_action()
        
        configuration.output.save()

        user.report()

def usage(script_name):
    """
    Prints the usage message to the output stream.
    """
    print "Usage: {0} [configuration_filename]".format(script_name)

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        usage(sys.argv[0])
    else:
        main(sys.argv[1])