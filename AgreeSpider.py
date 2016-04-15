#!/usr/bin/env python
#coding=utf-8

import sys
import re
import myjson
from datetime import datetime
import  time 
import random
from lxml import etree
from UrlOpener import UrlOpener

main_page = ""
target_words = []
target_channels = []

def get_channels(data):

	# [(channel_name, channel_url), ...]
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


def match_title(title, words):

	for word in words:
		if title.find(word) != -1:
			return word

	return None


def get_max_page(data):
	tree = etree.HTML(data)
	pages = tree.xpath("//div[@class='pages']/a")

	max_num = 0

	for page in pages:
		href = page.get("href")
		m = re.match(r'.*page=(.*)', href) 
		num = int(m.group(1))

		if num > max_num:
			max_num = num

	return max_num


def process_page(page_url):

	# [(title, url, matched_word), ...]
	page_result = []

	try:
		url_opener = UrlOpener(debug=True)
		data = url_opener.open_url(page_url)

		tree = etree.HTML(data)
		subjects = tree.xpath("//span[contains(@id,'thread_')]/a")

		for subject in subjects:
			try:
				url = main_page + subject.get("href")
				title = subject.text

				match_word =  match_title(title, target_words) 

				if match_word != None:
					print "%s\t%s\t%s" % (match_word, title, url)
					page_result.append((title, url, match_word))

			except Exception, ex:
				print str(ex)
				pass

	except Exception, ex:
		print str(ex)

	return page_result


def process_channel(url, page):

	# [(title, url, matched_word), ...]
	channel_result = []

	url_opener = UrlOpener(debug=True)
	data = url_opener.open_url(url)
	max_page = get_max_page(data)

	print "get max_page = %d, require page = %d" % (max_page, page)

	if max_page > page:
		max_page = page

	for i in range(max_page):
		print "processing page %d ..." % (i)
		page_url = url + "&page=%d" % (i + 1)
		page_result = process_page(page_url)
		channel_result.extend(page_result)
		time.sleep(random.random())

	return channel_result


def store_channel_result(channel_name, channel_result, result_dir):

	file_map = {}

	file_header="""
		<html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta http-equiv="Content-Language" content="zh-cn">
		<title>result</title>
		</head>
		<body>

	"""

	file_footer="""
		</body>
		</html>
	"""

	for result in channel_result:
		try:
			title = result[0]
			url = result[1]
			word = result[2]

			file_name = channel_name + "_" + word

			if file_name not in file_map:
				f = open(result_dir + "/" + file_name + ".html", "w")
				file_map[file_name] = f
				f.write(file_header + "\n")

			file_map[file_name].write("<a href=\"%s\">%s</a><br/>\n" % (url, title.encode("utf-8")) )

		except Exception, ex:
			print str(ex)

	for file_name in file_map:
		file_map[file_name].write(file_footer + "\n")
		file_map[file_name].close()

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
				print "start processing channel: %s" % (channel_name)
				channel_result = process_channel(channel_url, 100)
				store_channel_result(channel_name, channel_result, "./result")
				print "finish processing channel: %s" % (channel_name)

			except Exception, ex:
				print str(ex)

	return


main()
