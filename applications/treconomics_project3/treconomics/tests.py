"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from experiment_configuration import experiment_setups


def test_permutations(experiment, verbose=False):
    """
    Given an experiment object (through parameter experiment), returns a boolean value indicating whether or not the
    correct set of permutations can be produced. This is determined by the number of topics utilised for the given
    experiment. The get_rotations() and get_rotation_topic() methods are used to test the functionality.

    If the list of topics produced for a given iteration are all correct, True is returned.
    Set verbose=True for a detailed printout of the test as it is being run.
    """
    topics = experiment.topics
    no_topics = len(topics)  # The total number of topics used for the given experiment.
    no_permutations = experiment.n  # The total number of possible permutations.

    if verbose:
        print "Topics: {0} (total of {1})".format(topics, no_topics)
        print "Total permutations: {0}".format(no_permutations)
        print

    for i in range(0, no_permutations):
        rotations = experiment.get_rotations(i)

        if verbose:
            print "Permutation {0} ({1})".format(i, rotations)

        for k in range(0, no_topics):
            rotation_topic = experiment.get_rotation_topic(i, k)

            if verbose:
                print "\tTopic {0} at permutation list position {1}".format(rotation_topic, k)

            if experiment.get_rotations(i)[k] == experiment.get_rotation_topic(i, k):
                if verbose:
                    print "\t\tPASS"
            else:
                if verbose:
                    print "\t\tFAIL"
                return False

    if verbose:
        print "Permutation check PASSED"

    return True


class PermutationTest(TestCase):
    def test_permutations(self):
        # Tests each experiment's topic permutations in turn.
        # Experiments are obtained from experiment_configuration.experiment_setups.
        for experiment in experiment_setups:
            self.assertEquals(test_permutations(experiment), True)