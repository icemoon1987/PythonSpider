#!/usr/bin/env python
#coding=utf-8

import urllib
from datetime import datetime
import  time 

class UrlOpener(object):

    def __init__(self, retry_gap=5, retry_times=3, debug=False):
        self.retry_gap = retry_gap
        self.retry_times = retry_times
        self.debug = debug
        return

    def open_url(self, url):

        try_num = 0

        while try_num < self.retry_times:
            try:
                data = urllib.urlopen(url).read()
                return data
            except Exception, ex:
                if self.debug:
                    print "UrlOpener: open url error, retry_time=%d url=%s" % (try_num, url)
                try_num = try_num + 1

        if self.debug:
            print "UrlOpener: open url error, url=" + url
            
        return None



