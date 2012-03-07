import os
import urllib
import urllib2
import cookielib

baseurl = "http://www.bright-shadows.net"

class PageGetter(object):
	def __init__(self, cookiefile):
		self.cj = cookielib.MozillaCookieJar(cookiefile)
		
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
		response = self.opener.open(baseurl + pagePath)		
		pic = response.read()
		fout = open(targetFilename, "wb")
		fout.write(pic)
		fout.close()

		print "file written to " + targetFilename
	def getHTML(self, pagePath):
		response = self.opener.open(baseurl + pagePath)		
		return ''.join(response.readlines())
