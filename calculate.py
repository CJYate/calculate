import os
import urllib
import urllib2
import cookielib
from itertools import groupby

from login import LoggerInner
from webUtils import WebUtils

bs_username = "cYate"
bs_password = "shadowmaster"

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

challengepath = "/challenges/programming/calculate"
linkPath = challengepath + "/tryout.php"
solutionPath = challengepath + "/solution.php"

class Calculator(object):
	def __init__(self, inputLine):
		self.Parse(inputLine)

	def Parse(self, inputLine):
		equation = inputLine[inputLine.find('\"') + 1: inputLine.rfind('\"')]
		print equation

LoggerInner(bs_username, bs_password, cookiefile)
pageGetter = WebUtils(cookiefile, baseurl)
problem = pageGetter.getHTML(linkPath)
print problem

calculator = Calculator(problem)

solutionParams = "?solution="
solpath = "%s%s%s" %(solutionPath, solutionParams, "")
print solpath
print pageGetter.getHTML(solpath)
