__author__ = 'mickeypash'
import unittest
import logging
import sys
from treconomics.experiment_setup import ExperimentSetup


class TestDefaultExpSetup(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestExpSetup")
        self.es = ExperimentSetup(None, None, delay_results=[0, 5, 2])

    def test_practice_topic(self):
        self.logger.debug("Test Practice Topic")
        e = self.es.get_exp_dict(0, 0)

        self.assertEquals(e['topic'], '367')

    def test_real_topic(self):
        self.logger.debug("Test Real Topic")
        e = self.es.get_exp_dict(1, 0)
        t1 = e['topic']

        e = self.es.get_exp_dict(2, 1)
        t2 = e['topic']

        self.assertEquals(t1, t2)

    def test_result_delay(self):
        self.logger.debug("Test results delay")
        e = self.es.get_exp_dict(1, 0)
        d = e['result_delay']

        self.assertEquals(d, 5)
        e = self.es.get_exp_dict(2, 1)
        d = e['result_delay']

        self.assertEquals(2, 2)


class TestExistingExpSetup(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestExpSetup")
        self.es = ExperimentSetup(None, None, delay_results=9, rpp=10)

    def test_practice_topic(self):
        self.logger.debug("Test Practice Topic")
        e = self.es.get_exp_dict(0, 0)

        self.assertEquals(e['topic'], '367')

    def test_rpp(self):
        self.logger.debug("Test Rpp")
        e = self.es.get_exp_dict(1, 0)
        rpp = e['rpp']
        self.assertEquals(rpp, 10)
        e = self.es.get_exp_dict(2, 1)
        rpp = e['rpp']

        self.assertEquals(rpp, 10)

    def test_result_delay(self):
        self.logger.debug("Test results delay")
        e = self.es.get_exp_dict(1, 0)
        d = e['result_delay']

        self.assertEquals(d, 9)
        e = self.es.get_exp_dict(2, 1)
        d = e['result_delay']

        self.assertEquals(d, 9)


class TestInterfaceSetup(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestInterfaceExpSetup")
        self.es = ExperimentSetup(None, None, interface=[1, 2, 3], practice_interface=37, rpp=10)

    def test_practice_topic(self):
        self.logger.debug("Test Practice Topic")
        e = self.es.get_exp_dict(0, 0)

        self.assertEquals(e['topic'], '367')

    def test_interface_get_practice(self):
        self.logger.debug("Test Interface Get Practice")
        interface = self.es.get_interface(0)
        self.assertEquals(interface, 37)

    def test_interface_get(self):
        self.logger.debug("Test Interface Get")
        interface = self.es.get_interface(1)
        self.assertEquals(interface, 1)
        interface = self.es.get_interface(2)
        self.assertEquals(interface, 2)
        interface = self.es.get_interface(3)
        self.assertEquals(interface, 3)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestExperimentSetup").setLevel(logging.DEBUG)
    unittest.main(exit=False)

    es = ExperimentSetup(None, None)
    es.rotation_type = 1
    for r in range(0, 12):
        for t in range(0, 3):
            des = es.get_exp_dict(t, r)
            print t, r, des['topic'], des['interface']