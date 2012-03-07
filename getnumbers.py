import os
import urllib
import urllib2
import cookielib
import png
from itertools import groupby

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
	
		self.numbers = list()

		self.characters = list()

		self.getData()		

	def getData(self):
		image = self.reader.read()
		self.width = image[0]
		self.height = image[1]
		self.pixels = image[2]
		self.metadata = image[3]

		print "Original size %d rows x %d columns " % (self.height, self.width)
		self.rows = list()

		self.getPixels()

		hp = self.countPixelSize()
		print "horizontal pixel size = ", hp
		
		# reduce to single pixel per row
		self.removeZeroRows()

		self.printSize()
		self.transpose()
		
		vp = self.countPixelSize()
		print "vertical pixel size = ",vp

		self.removeZeroRows()
		self.transpose()

		self.pixelise(hp, vp)

		self.printSize()

	def getPixels(self):
		for x in self.pixels:
			self.rows.append(x)
	
	def removeZeroRows(self):
		self.rows = [x for x in self.rows if 1 in x]
		print "removeZeroRows -- now got %d rows" % len(self.rows)
	
	def transpose(self):
		self.rows = zip(*self.rows)

	def printSize(self):
		print "%d rows %d cols" % (len(self.rows), len(self.rows[0]))

	def pixelise(self, horizPixelSize, vertPixelSize):
		print "pixelising"
		temp = []
		for row in self.rows[0::vertPixelSize]:
			temp.append(row[0::horizPixelSize])
		
		self.rows = temp

	def countPixelSize(self):

		groups = []
		for row in self.rows:
			t = [len(list(group)) for char, group in groupby(row, lambda x: x == 1)]
#			print t
#			print min(t)
			groups.append(min(t))

#		print groups
#		print min(groups)
		return min(groups)
#		return min(len(list(v) for g,v in itertools.groupby(self.rows, lambda x: x == 1) if g))
			
	
	def convertToBW(self, outputFile, outputExtension):


		picout = png.Writer(len(self.rows[0]), len(self.rows), None,
				False, False, 1, [(0,0,0),(255,255,255)], None, None, None, None,
				False, None, 1) 
		
		outputPath = "%s_%dx%d.%s" % (outputFile,len(self.rows[0]),len(self.rows),outputExtension)		
		
		pix = self.rows 

		fout = open(outputPath, "wb")
		picout.write(fout, pix)
		print "B/W image written to ",outputPath


LoggerInner(bs_username, bs_password, cookiefile)
pageGetter = PageGetter(cookiefile)

pngFilename = "numbersTest.png"
pageGetter.getPNG("/challenges/programming/numbers/tryout.php", pngFilename)

analyser = AnalysePng(pngFilename)
analyser.convertToBW("bwFile","png")

