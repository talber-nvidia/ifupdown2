#!/usr/bin/python
#
# Copyright 2014-2017 Cumulus Networks, Inc. All rights reserved.
# Author: Roopa Prabhu, roopa@cumulusnetworks.com
#

try:
    import time
    import logging

    from ifupdown.iface import *
    from ifupdown.utils import utils

    from ifupdownaddons.cache import *

    import ifupdown.ifupdownflags as ifupdownflags
except ImportError, e:
    raise ImportError('%s - required module not found' % str(e))


def profile(func):
    def wrap(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        print str(func)
        print (time.time() - started_at)
        return result
    return wrap

class utilsBase(object):
    """ Base class for ifupdown addon utilities """

    def __init__(self, *args, **kargs):
        modulename = self.__class__.__name__
        self.logger = logging.getLogger('ifupdown.' + modulename)

    def write_file(self, filename, strexpr):
        try:
            self.logger.info('writing \'%s\'' %strexpr +
                ' to file %s' %filename)
            if ifupdownflags.flags.DRYRUN:
                return 0
            with open(filename, 'w') as f:
                f.write(strexpr)
        except IOError, e:
            self.logger.warn('error writing to file %s'
                %filename + '(' + str(e) + ')')
            return -1
        return 0

    def read_file(self, filename):
        try:
            self.logger.debug('reading \'%s\'' %filename)
            with open(filename, 'r') as f:
                return f.readlines()
        except:
            return None
        return None

    def read_file_oneline(self, filename):
        try:
            self.logger.debug('reading \'%s\'' %filename)
            with open(filename, 'r') as f:
                return f.readline().strip('\n')
        except:
            return None
        return None

    def sysctl_set(self, variable, value):
        utils.exec_command('%s %s=%s' %
                           (utils.sysctl_cmd, variable, value))

    def sysctl_get(self, variable):
        return utils.exec_command('%s %s' %
                                  (utils.sysctl_cmd,
                                   variable)).split('=')[1].strip()
