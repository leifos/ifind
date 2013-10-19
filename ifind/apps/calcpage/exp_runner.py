_author__ = 'rose'
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("experiments.cfg")
url = config.get('experiment','url')

print "url from config file is ", url

