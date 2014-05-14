#-*- coding: UTF-8 -*-
import platform
import os
import time

from eSpider import eSpider

# Time gap
gap = 10

# Proxy
proxyServer = "127.0.0.1"
proxyPort = "8087"

# The number of topics to achieve, set to 0 for unlimited.
topicNumMax = 30

# The number of pictures in each topic, set to 0 for unlimited.
imageNumPerTopic = 100


# Search string and search options
searchStr = "stocking+color+chinese"
searchOpt = "f_doujinshi=1&f_manga=1&f_artistcg=1&f_gamecg=1&f_western=1&f_non-h=0&f_imageset=1&f_cosplay=1&f_asianporn=1&f_misc=1"

# Initiated a eSpider
spider = eSpider(topicNumMax, proxyServer, proxyPort)

print ""
print "*************************************************"
print "Search String:	", searchStr
print "Search Options:	", searchOpt
print "Topic Number Limit:				", topicNumMax
print "Picture Number Per Topic Limit:	", imageNumPerTopic
print "*************************************************"
print ""

step = 0

def stepInc():
	global step
	step = step + 1
	return step

stepStr = lambda str: "Step %d : %s" % ( stepInc() , str)


# Open Main Page
print ""
print "*******************************"
print stepStr("Open main page")
print "*******************************"
print ""

main_page = spider.openMainPage(searchStr, searchOpt)

if main_page == None :
	print("Open main_page failed!")
	exit()
else :
	print("Open main_page success!")


# Parse main page for search results, if return None, means no results.
print ""
print "*******************************"
print stepStr("Parse main page for search result")
print "*******************************"
print ""

pageNumMax =  spider.processMainPage(main_page)

if pageNumMax == None:
	print "No Search Result!"
	exit()
else:
	print "There is(are) ", pageNumMax, " page(s) to go."


# Loop on pages to get topics, with a gap of 5 seconds
print ""
print "*******************************"
print stepStr("Loop on search result pages to get topics")
print "*******************************"
print ""

topics = []

for i in range(0, pageNumMax) :
	print "Getting topics from page ", i+1, " ..." 

	page = spider.openSearchPage(i)
	if( page == None ):
		print "Failed to open search page ", i+1
		exit()

	topics += spider.processSearchPage(page)

	print "Sleep 5 seconds ..."
	time.sleep(10)

if topics == []:
	print "Get No topics!"
	exit()
else:
	print "Got ", len(topics), " topics! "


# Loop on every topic to get pictures
print ""
print "*******************************"
print stepStr("Loop on every topic to get pictures")
print "*******************************"
print ""

newTopicNum = 0;
newImages = 0;

for i in range(len(topics)): 
	print "Getting topic ", i, " ..."

	page = spider.openTopicPage(topics[i])
	if( page == None ):
		print " ** Warning: Failed to open topic page ", i

	if( page == True):
		continue

	images = spider.processTopicPage(page, topics[i])
	print "Get ", len(images), " imageses!"

	topicName = spider.GetTopicName(topics[i])
	storePath = "./output/" + topicName
	
	# Create a directory for this topic
	if( platform.system() == "Linux"):
		os.system(u"mkdir " + storePath)

	elif( platform.system() == "Windows"):
		os.system(u"md " + storePath)	

	# Loop on every images and download them!

	imageNum = len(images)
	if imageNum > imageNumPerTopic:
		print "Too many images, let's just download " + str(imageNumPerTopic)
		imageNum = imageNumPerTopic

	for j in range(imageNum):
		print "Downloading topic " + str(i) + " image " + str(j)
		filePath = storePath + "/" + str(j) + ".jpg"
		spider.downLoadImage( images[j], filePath, True, proxyServer, proxyPort)
		newImages = newImages + 1
		
		time.sleep(10)

	newTopicNum = newTopicNum + 1

	time.sleep(10)


print "Finished ", newTopicNum, " new topics and ", newImages ," new images!!" 


