#-*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import httplib
import urllib2
import re
import math
import os
import platform
import time
import hashlib

class eSpider(object):

	def __init__(self, topicNumMax, proxy = "", port = ""):

		self.mainPage = "http://g.e-hentai.org"
		self.searchStr = ""
		self.searchOpt = ""

		self.topicNumMax = topicNumMax
		self.topicNumPerPage = 0 
		self.topicNumOnThisPage = 0
		self.pageNumMax = 0

		if(proxy != ""):
			proxyServer = "http://" + proxy + ":" + port
			opener = urllib2.build_opener( urllib2.ProxyHandler({'http':proxyServer}) )
			urllib2.install_opener(opener)

		return


	def openUrl(self, url, repeat = 5):
		print ""
		print "Opening Url: ", url

		for i in range(repeat):

			try:
				page = urllib2.urlopen(url).read()

			except (IOError, httplib.HTTPException):
				print "Failed ", i+1 , " times!"
				page =  None
				time.sleep(0.5)

			finally:
				if page != None:
					break

		return page


	def openMainPage(self, searchStr, searchOpt):

		self.searchStr = searchStr;
		self.searchOpt = searchOpt;

		# Open main page
		url = self.mainPage + "/?" + searchOpt + "&f_search=" + searchStr + "&f_apply=Apply+Filter"
		return self.openUrl(url) 


	def processMainPage(self, main_page):

		soup = BeautifulSoup(main_page, "html5lib")

		# Get page number
		pages = soup.find_all("td", onclick=re.compile("sp"));

		if pages == None or pages == []:
			print("eSpider::processMainPage(): No page number information found!")
			return None

		pageNum = pages[-2].string

		#print "eSpider::processMainPage(): pageNum = ", pageNum

		# Get topic number per page
		topicOnPage = soup.find("table", class_="itg").find_all("tr", class_=True)
		self.topicNumPerPage = len(topicOnPage)

		#print "eSpider::processMainPage(): self.topicNumPerPage = ", self.topicNumPerPage

		# Get topic number
		topicNum = re.search( r'of (.*$)', unicode(soup.find("p", class_="ip").string)).group(1)

		print "eSpider::processMainPage(): topicNum = ", topicNum

		# Decided how many pages to go

		if self.topicNumMax > topicNum :
			print "self.topicNumMax is too big!"
			return None

		if self.topicNumMax % self.topicNumPerPage == 0 :
			pageNumMax = self.topicNumMax / self.topicNumPerPage
		else :
			pageNumMax = self.topicNumMax / self.topicNumPerPage + 1

		self.pageNumMax = pageNumMax

		return pageNumMax


	def openSearchPage(self, pageIndex):

		url = self.mainPage + "/?page=" + str(pageIndex) + "&" + self.searchOpt + "&f_search=" + self.searchStr + "&f_apply=Apply+Filter"

		if pageIndex == self.pageNumMax - 1 :
			self.topicNumOnThisPage = self.topicNumMax % self.topicNumPerPage
		else:
			self.topicNumOnThisPage = self.topicNumPerPage

		return self.openUrl(url)


	def processSearchPage(self, page):

		soup = BeautifulSoup(page, "html5lib")

		return soup.find("table", class_="itg").find_all("div", class_="it5", limit=self.topicNumOnThisPage)


	def openTopicPage(self, topic):

		topicName = self.GetTopicName(topic)

		if(os.path.exists("./output/" + topicName)):
			print "Already have " + topicName
			return True

		return self.openUrl(unicode(topic.find("a")['href']))


	def processTopicPage(self, page, topic):
		
		images = []

		soup = BeautifulSoup(page, "html5lib")

		# Get page number
		pages = soup.find_all("td", onclick=re.compile("sp"));

		if pages != [] :
			pageNum = int(unicode(pages[-2].string))
		else:
			pageNum = 1
		

		print "eSpider::processTopicPage(): There are ", pageNum, " pages"

		# Get image number, if we failed here, then the topic may be too offensive, we skip this topic.

		tmp = soup.find("p", class_="ip")

		if(tmp == None):
			print "Too offensive! Skip!"
			return images

		imageNum = re.search( r'of (.*) images', unicode(tmp.string)).group(1)

		print "eSpider::processTopicPage(): There are ", imageNum, " images"

		# Loop on different page to get image links

		for i in range(pageNum):
		
			page = self.openImagePage(topic, i)	
			if page == None:
				print "eSpider::processMainPage(): failed in open page ", i
				continue

			images += self.processImagePage(page)

		return images 


	def openImagePage(self, topic, pageIndex):

		# Get topic url
		topicUrl = unicode(topic.find("a")['href'])
		url = topicUrl + "?p=" + str(pageIndex)

		return self.openUrl(url)


	def processImagePage(self, page):
		
		soup = BeautifulSoup(page, "html5lib")

		return soup.find_all("div", class_="gdtm")


	def getImageLink(self, image):

		url = unicode(image.find("a")['href'])
		page = self.openUrl(url)

		if page == None :
			print "eSpider::GetImageLinks(): error in open ", url
			return False

		soup = BeautifulSoup(page, "html5lib")

		print soup.find("img", id="img")['src']

		return unicode(soup.find("img", id="img")['src'])


	def downLoadImage(self, image, path, using_phantomjs, proxyServer = "", proxyPort = ""):
		
		url = unicode(image.find("a")['href'])
		
		if(using_phantomjs == True):

			if( proxyServer != ""):
				os.system("phantomjs --proxy="+proxyServer+":"+proxyPort+ " downLoadImage.js " + url + " " + path)
			else:
				os.system("phantomjs downLoadImage.js " + url + " " + path)


		else:
			imageLink = getImageLink(image);

			if imageLink != False:
				os.system("curl " + imageLinks + " > " + path )

		return


	def GetTopicName(self, topic):

		# Get topic name and process it
		topicName = re.sub("[^A-Za-z0-9]", "", unicode(topic.find("a").string))

		if topicName == "":
			topicName = hashlib.md5(topicName).hexdigest()

		return topicName

