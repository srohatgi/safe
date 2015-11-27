__author__ = 'sumeet'

from nose2.tools import *
import safe


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_basic():
    print "I RAN!"


test_basic.setup = setup
test_basic.teardown = teardown

