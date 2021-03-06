#!/usr/bin/env python
#coding=utf-8

import urllib2
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
                if self.debug:
                    print "UrlOpener: open url, url=%s" % (url)
                data = urllib2.urlopen(url, timeout=10).read()
                return data
            except Exception, ex:
                if self.debug:
                    print "UrlOpener: open url error, error=%s retry_time=%d url=%s" % (str(ex), try_num, url)
                try_num = try_num + 1

        if self.debug:
            print "UrlOpener: open url error, url=" + url
            
        return None

if __name__ == '__main__':

    url_opener = UrlOpener(debug=True)

    data = url_opener.open_url("http://www.baidu.com")
    print data

    data = url_opener.open_url("http://www.baidu.com333")
