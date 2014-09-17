import os

class OutputController(object):
    """
    
    """
    def __init__(self, simulation_configuration, output_configuration):
        self.__simulation_configuration = simulation_configuration
        
        self.__base_directory = output_configuration['@baseDirectory']
        self.__save_interaction_log_flag = output_configuration['@saveInteractionLog']
        self.__save_relevance_judgments_flag = output_configuration['@saveRelevanceJudgments']
        self.__trec_eval_flag = output_configuration['@trec_eval']
        
        self.__interaction_log = []
        
        self.output_indentation = 2  # Controls the level of indentation when outputting results to stdout.
                                     # Publicly facing instance variable - is used by the Component Generators prettify() methods.
    
    def log(self, entry):
        """
        Adds an event to the interaction log.
        """
        self.__interaction_log.append(entry)
    
    def display_config(self):
        """
        Sends a prettified version of the current simulation's configuration to stdout.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        simulation_base_id = self.__simulation_configuration.base_id
        print "SIMULATION '{0}'".format(simulation_base_id)
        
        print "{0}Simulation Configuration:".format(" "*self.output_indentation)
        print self.__simulation_configuration.prettify()

        print "{0}User Configuration ({1}):".format(" "*self.output_indentation, self.__simulation_configuration.user.id)
        print self.__simulation_configuration.user.prettify()
        
    def display_report(self):
        """
        Prints a summary of the results from the simulation to stdout.
        """
        search_context_summary = self.__simulation_configuration.user.search_context.report()
        
        print
        print
        print "{0}Results Summary:".format(" "*self.output_indentation)
        print "{0}{1}".format(search_context_summary, os.linesep)
    
    def save(self):
        """
        Publicly exposed function used for saving all output files to disk.
        Calls a private method for each in turn - whether or not the files are saved is dependent upon the set flags.
        """
        self.__save_interaction_log()
        self.__save_relevance_judgments()
        self.__run_trec_eval()
    
    def __save_interaction_log(self):
        """
        Depending on the status of the interaction log flag, saves the interaction log to disk.
        """
        if self.__save_interaction_log_flag:
            interaction_log_filename = '{0}.log'.format(self.__simulation_configuration.base_id)
            interaction_log_filename = os.path.join(self.__base_directory, interaction_log_filename)
            
            log_file = open(interaction_log_filename, 'w')
            
            for entry in self.__interaction_log:
                log_file.write('{0}{1}'.format(entry, os.linesep))
            
            log_file.close()
    
    def __save_relevance_judgments(self):
        """
        Depending on the status of the relevance judgments flag, saves relevance judgments to disk.
        """
        if self.__save_relevance_judgments_flag:
            search_context = self.__simulation_configuration.user.search_context
            topic = self.__simulation_configuration.topic
            
            relevance_judgments_filename = '{0}.rels'.format(self.__simulation_configuration.base_id)
            relevance_judgments_filename = os.path.join(self.__base_directory, relevance_judgments_filename)
            
            rank = 0
            
            with open(relevance_judgments_filename, 'w') as judgments_file:
                for document in search_context.get_relevant_documents():
                    rank = rank + 1
                    judgments_file.write("{0} Q0 {1} {2} {3} Exp{4}".format(topic.id, document.doc_id, rank, rank, os.linesep))
    
    def __run_trec_eval(self):
        """
        Runs trec_eval over the relevance judgments created by the simulator. Produces a .out file.
        This only runs if the relevance judgments and trec_eval flags are set.
        Assume trec_eval is on your path.
        """
        if self.__save_relevance_judgments_flag and self.__trec_eval_flag:
            relevance_judgments_filename = '{0}.rels'.format(self.__simulation_configuration.base_id)
            relevance_judgments_filename = os.path.join(self.__base_directory, relevance_judgments_filename)
            
            qrels_filename = os.path.abspath(self.__simulation_configuration.topic.qrels_filename)
            
            output_filename = '{0}.out'.format(self.__simulation_configuration.base_id)
            output_filename = os.path.join(self.__base_directory, output_filename)
            
            os.system('trec_eval {0} {1} > {2}'.format(qrels_filename, relevance_judgments_filename, output_filename))