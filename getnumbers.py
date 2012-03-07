import os
import urllib
import urllib2
import cookielib
import png
from login import LoggerInner
from pageGetter import PageGetter

bs_username = "CYate"
bs_password = "shadowmaster"

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"


class AnalysePng(object):
	def __init__(self, filePath):
		print "analysePng created"
		
		self.reader = png.Reader(filePath)
	
		self.getData()

	def getData(self):
		image = self.reader.read()
		self.width = image[0]
		self.height = image[1]
		self.pixels = image[2]
		self.metadata = image[3]
	
		self.getRows()
		self.removeEveryNthRow(5)

	def getRows(self):
		self.rows = [x for x in self.pixels if 1 in x]
		print "GetRows got %d rows" % len(self.rows)
	
	def removeEveryNthRow(self, n):
		print "splitting" 
		self.rows = self.rows[0::n]

	def convertToBW(self, outputFile, outputExtension):


		picout = png.Writer(self.width, self.nonZeroRowCount, None,
				False, False, 1, [(0,0,0),(255,255,255)], None, None, None, None,
				False, None, 1) 
		
		outputPath = "%s_%dx%d.%s" % (outputFile,self.width,self.nonZeroRowCount,outputExtension)		
		
		pix = self.nonZeroRows 

		fout = open(outputPath, "wb")
		picout.write(fout, pix)
		print "B/W image written to ",outputPath


LoggerInner(bs_username, bs_password, cookiefile)
pageGetter = PageGetter(cookiefile)

pngFilename = "numbersTest.png"

pageGetter.getPNG("/challenges/programming/numbers/tryout.php", pngFilename)

analyser = AnalysePng(pngFilename)
analyser.convertToBW("bwFile","png")

