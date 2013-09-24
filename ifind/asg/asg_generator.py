__author__ = 'leif'

import random

class YieldGenerator(object):
    # creates a patch and the payoffs in the patch
    def __init__(self, max_yield=3):
        self.max_yield = max_yield

    def get_yields(self, size=10):
        """
        returns a list of integers that denote the number of points in each doc
        :param size: number of documents
        :return:
        """
        pass

class HighYieldGenerator(YieldGenerator):
    
    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yl = []
        for i in range(n):
            yl.append(3)

        return yl

class MediumYieldGenerator(YieldGenerator):
    
    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yl = []
        for i in range(n):
            yl.append(2)

        return yl

class LowYieldGenerator(YieldGenerator):
    
    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yl = []
        for i in range(1):
            yl.append(random.randint(0,self.max_yield))

        return yl


class RandomYieldGenerator(YieldGenerator):

    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yl = []
        for i in range(n):
            yl.append(random.randint(0,self.max_yield))

        return yl


class ConstantLinearYieldGenerator(YieldGenerator):

    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yl = []
        for i in range(n):
            yl.append(1)

        return yl



class TestYieldGenerator(YieldGenerator):

    def __init__(self, max_yield=3):
        YieldGenerator.__init__(self, max_yield)
        self.count = 0

    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yls = []
        yls.append([3,3,3,2,2,2,1,1,1,0])
        yls.append([2,2,2,2,1,0,1,0,1,0])
        yls.append([1,0,2,0,0,0,1,0,0,0])

        yl = yls[ (self.count % 3) ]
        self.count += 1

        return yl


class TestHighYieldGenerator(YieldGenerator):

    def __init__(self, max_yield=3):
        YieldGenerator.__init__(self, max_yield)
        self.count = 0

    def get_yields(self, n=10):
        """
        :param n: number of yields to be generated i.e. length of document result list
        :return: list of n integers (i.e. the yeilds)
        """
        yls = []
        yls.append([3,3,3,2,2,2,1,1,1,0])
        yls.append([3,2,3,2,2,2,1,0,0,0])
        yls.append([3,3,1,1,1,0,0,0,0,0])
        yls.append([3,3,2,3,1,2,1,1,1,0])
        yls.append([3,3,3,3,0,0,0,0,0,0])

        yl = yls[ (self.count % 5) ]
        self.count += 1

        return yl



class CueGenerator(object):

    def __init__(self, cue_length = 10, gain = 10, hintfactor = 0.5):
        """
        :param cue_length:
        :return:
        """
        self.cue_length = cue_length
        self.gain = gain
        self.hintfactor = hintfactor

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            ll.append('o'*self.cue_length)

        return ll

    def __str__(self):
        return 'CueGenerator - Default'

class FixedCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            hintspace = self.hintfactor*self.gain
            ll.append('x'*hintspace)
            ll.append('.'*(self.cue_length-hintspace))
            ll = random.shuffle(ll)
        return ll

class VariableCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        ygain = 0
        ytotal = 0
        for i in range(len(yield_list)):
            ygain += yield_list[i]
        ymean = ygain / len(yield_list)
        for i in range(len(yield_list)):
            ytotal += ((yield_list[i]-ymean)*(yield_list[i]-ymean))
        ysd = ytotal / len(yield_list)
        hintspace = random.gauss(ymean, ysd)
        ll.append('x'*hintspace)
        ll.append('.'*(self.cue_length-hintspace))
        ll = random.shuffle(ll)
        return ll

class LowInfoCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            if random.randint(0,20) < 7:
                ll.append('o'*self.cue_length)
            else:
                ll.append('x'*self.cue_length)

        return ll

class MedInfoCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            if random.randint(0,10) < 7:
                ll.append('o'*self.cue_length)
            else:
                ll.append('x'*self.cue_length)

        return ll

class LowInfoCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            if random.randint(0,7) < 7:
                ll.append('o'*self.cue_length)
            else:
                ll.append('x'*self.cue_length)

        return ll

class GainBasedCueGenerator(CueGenerator):

    def get_labels(self, n=10, yield_list = None):
        """
        :param n: number of labels to be generated
        :param yield_list: list of n strings (i.e. snippet labels)
        :return:
        """
        ll = []
        for i in range(n):
            g = yield_list[i]
            x = int(g) * 5 + random.randint(3,10)
            dots = self.cue_length - int(x)
            if dots < 0:
                dots = 0

            ll.append('x'*x + '_'*dots)

        return ll

    def __str__(self):
        return 'GainBasedCueGenerator'
