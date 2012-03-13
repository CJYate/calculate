import os
import urllib
import urllib2
import cookielib
import png
import getpass
from itertools import groupby

from login import LoggerInner
from webUtils import WebUtils

bs_username = "CYate"
bs_password = ""

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

charmap = [
		# 0
		[(0,1,1,1,0), 
			(1,0,0,0,1),
			(1,0,0,0,1),
			(1,0,0,0,1),
			(0,1,1,1,0)], 
		# 1
		[(0,0,1,0,0),
			(0,1,1,0,0),
			(1,0,1,0,0),
			(0,0,1,0,0),
			(1,1,1,1,1)],
		# 2
		[(0,1,1,1,0),
			(1,0,0,0,1),
			(0,0,1,1,0),
			(0,1,0,0,0),
			(1,1,1,1,1)],
		# 3
		[(0,1,1,1,0),
			(1,0,0,0,1),
			(0,0,1,1,1),
			(1,0,0,0,1),
			(0,1,1,1,0)],
		# 4
		[(0,0,1,0,0),
			(0,1,0,0,0),
			(1,0,0,1,0),
			(1,1,1,1,1),
			(0,0,0,1,0)],			
		# 5
		[(1,1,1,1,1),
			(1,0,0,0,0),
			(1,1,1,1,1),
			(0,0,0,0,1),
			(1,1,1,1,1)],
		# 6
		[(1,1,1,1,1),
			(1,0,0,0,0),
			(1,1,1,1,1),
			(1,0,0,0,1),
			(1,1,1,1,1)],
		# 7
		[(1,1,1,1,0),
			(0,0,0,1,0),
			(0,0,1,1,1),
			(0,0,0,1,0),
			(0,0,0,1,0)],
		# 8
		[(0,1,1,1,0),
			(1,0,0,0,1),
			(0,1,1,1,0),
			(1,0,0,0,1),
			(0,1,1,1,0)],
		# 9
		[(0,1,1,1,0),
			(1,0,0,0,1),
			(0,1,1,1,1),
			(0,0,0,0,1),
			(0,1,1,1,0)]
		]

class AnalysePng(object):
	def __init__(self, filePath):
		print "analysePng created"
		
		self.reader = png.Reader(filePath)
	
		self.numbers = list()

		self.characters = list()

		self.getData()		

	def analyse(self):

		for c in self.characters:			
			
			found = False

			for i in range(0, len(charmap)):
					
				for rot in range(0,4):

					if c == charmap[i]:
						self.numbers.append(i)
						found = True
						break

					c = zip(*c[::-1])

				if found: break

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
		
		self.removeZeroRows()
		self.transpose()
		
		vp = self.countPixelSize()
		print "vertical pixel size = ",vp

		self.removeZeroRows()
		self.transpose()
		
		self.pixelise(hp, vp)
		self.printSize()
		
		self.decompose()
	
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

	def decompose(self):		

		charsize = 5

		self.transpose()
		for i in xrange(0, len(self.rows), charsize):			
			temp = self.rows[i:i+charsize]
			temp2 = []
			for line in temp:
				temp2.append(reversed(line))
			self.characters.append(temp2)
		self.transpose()

		print "found ", len(self.characters), " characters"

	def countPixelSize(self):

		groups = []
		for row in self.rows:
			t = [len(list(group)) for char, group in groupby(row, lambda x: x == 1)]
			groups.append(min(t))

		return min(groups)
	
	def convertToBW(self, outputFile, outputExtension):


		picout = png.Writer(len(self.rows[0]), len(self.rows), None,
				False, False, 1, [(0,0,0),(255,255,255)], None, None, None, None,
				False, None, 1) 
		
		outputPath = "%s_%dx%d.%s" % (outputFile,len(self.rows[0]),len(self.rows),outputExtension)		
		
		pix = self.rows 

		fout = open(outputPath, "wb")
		picout.write(fout, pix)
		print "B/W image written to ",outputPath

        
bs_password = getpass.getpass("Enter password:")
LoggerInner(bs_username, bs_password, cookiefile)
pageGetter = WebUtils(cookiefile, baseurl)

pngFilename = "numbersTest.png"

linkPath = "/challenges/programming/numbers/tryout.php"
pageGetter.getPNG(linkPath, pngFilename)

analyser = AnalysePng(pngFilename)
analyser.analyse()

print analyser.numbers

solutionPath = "/challenges/programming/numbers/solution.php"
numbers = (''.join(map(str, analyser.numbers)))
print "numbers joined = ", numbers
solutionParams = "?solution="
solpath = "%s%s%s" %(solutionPath, solutionParams, numbers)
print solpath
print pageGetter.getHTML(solpath)
