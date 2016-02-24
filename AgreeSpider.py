#!/usr/bin/env python
#coding=utf-8

import sys
import re
import myjson
from datetime import datetime
import  time 
from lxml import etree
from UrlOpener import UrlOpener

main_page = "http://www.galgamer.net/bbs/"


def get_channels(data):

	tree = etree.HTML(data)

	channel_divs = tree.xpath("//div[@class='left']/h2/a")

	for channel_div in channel_divs:
		print channel_div.
		print channel_div.get("href")



	return


def main():

	url_opener = UrlOpener()

	data = url_opener.open_url(main_page)

	channels = get_channels(data)

	return


main()
