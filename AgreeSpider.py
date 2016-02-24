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
target_channels = [u"蚁后同人动漫资源区"]

def get_channels(data):

	channels = []

	tree = etree.HTML(data)

	channel_divs = tree.xpath("//div[@class='left']/h2/a")

	for channel_div in channel_divs:
		tmp = channel_div.getchildren()

		if len(tmp) != 1:
			continue

		name = tmp[0].text
		href = channel_div.get("href")

		channels.append((name, main_page + href))

	return channels


def get_max_page(data):
	tree = etree.HTML(data)
	pages = tree.xpath("//div[@class='pages']/a")

	for page in pages:
		href = page.get("href")
		print href
		m = re.match(r'.*page=(.*)', href) 
		num = int(m.group(1))



def process_channel(url, max_page):

	url_opener = UrlOpener(debug=True)
	data = url_opener.open_url(url)
	max_page = get_max_page(data)

	return



def main():

	url_opener = UrlOpener()
	data = url_opener.open_url(main_page)
	channels = get_channels(data)

	for channel_name in target_channels:
		channel_url = None

		for i in range(len(channels)):
			if channel_name == channels[i][0]:
				channel_url = channels[i][1]

		if channel_url != None:
			try:
				channel_result = process_channel(channel_url, 30)
			except Exception, ex:
				print str(ex)

	return


main()
