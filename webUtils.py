import os
import urllib
import urllib2
import cookielib

class WebUtils(object):
	def __init__(self, cookiefile, baseUrl):
		self.cj = cookielib.MozillaCookieJar(cookiefile)
		self.baseUrl = baseUrl

		print "baseurl = ",self.baseUrl
		if(os.access(cookiefile, os.F_OK)):
			self.cj.load()

		self.opener = urllib2.build_opener(
			urllib2.HTTPRedirectHandler(),
			urllib2.HTTPHandler(debuglevel=0),
			urllib2.HTTPSHandler(debuglevel=0),
			urllib2.HTTPCookieProcessor(self.cj)
		)


	def getPNG(self, pagePath, targetFilename):
		print "reading path " + pagePath
		response = self.opener.open(self.baseUrl + pagePath)		
		pic = response.read()
		fout = open(targetFilename, "wb")
		fout.write(pic)
		fout.close()

		print "file written to " + targetFilename

	def getHTML(self, pagePath):
		response = self.opener.open(self.baseUrl + pagePath)		
		return ''.join(response.readlines())
