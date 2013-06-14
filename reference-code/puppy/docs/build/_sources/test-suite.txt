.. _the_puppyir_framework_test_suite:

The PuppyIR Framework Test Suite
======================================

The PuppyIR framework comes with an in-built test suite; for creating unit tests for all its components. The two main tasks are detailed below, briefly, and then discussed in the following sections.

To create a test, where <module> is the name of the Python file the test is for, use the following commands:

::

  $ cd /path/to/framework
  $ python unit.py create <module>

To run all the tests, currently defined in the test suite, use the following commands:

::

  $ cd /path/to/framework
  $ python unit.py run 

Create
------

The **Create** command generates a skeleton python script. This script is placed at a location in the test hierarchy that mirrors where the component being tested is in the framework's hierarchy.

For example, if we wanted to create a test script for our query filter, cool_filter we should use the following commands:

::

  $ cd /path/to/framework
  $ python unit.py puppy/query/filter/cool_filter.py

Our test script would be created in: test/puppy/query/filter/cool_filter.py (relative to our framework directory) - with the following auto-generated code:

::

  from puppy.query.filter.cool_filter import *

  import unittest


  class TestCoolFilter(object):
      pass

  if __name__ == '__main__':
      unittest.main()

It is now ready to be used and it is up to the programmer to write tests for the component in question.

Run
---

The **Run** command searches for all the current test cases and runs each of them in turn. Any issues are reported at the end of this process; nothing is outputted if a test succeeds, so if you run this command and nothing is outputted there are no problems.

If you are using a proxy server, there are two options: 

  1. Either use the in-built proxy system using a ServiceManager or PipelineService (via the config variable) in your tests.
  2. Write a work-around for your tests, or they will fail due to proxy errors (unless, of course, you are testing a component that does not need to go through the proxy server).

Example: Testing the Blacklist Filter
-------------------------------------

To provide an example, the code below shows a test for the Blacklist query filter (this rejects queries with blacklisted words in them). What this code does is check that queries with blacklisted words are actually being rejected and that valid queries are not rejected.

::

  from puppy.query.filter.blacklistfilter import *

  import unittest


  class TestBlacklistfilter(unittest.TestCase):
      def test_main(self):
          t = BlackListFilter(terms='bad')
          self.assertTrue(t.filter(Query('hello')))
          self.assertTrue(t.filter(Query('friends')))
          self.assertFalse(t.filter(Query('bad friends')))
          self.assertFalse(t.filter(Query('bad hello')))


  if __name__ == '__main__':
      unittest.main()