import os
import urllib
import urllib2
import cookielib

baseurl = "http://www.bright-shadows.net"
loginpath = "/login.php"

class LoggerInner(object):
	def __init__(self, login, password, cookiefile):
		""" Start """
		print "setting up login action"
		self.login = login
		self.password = password

		self.cookie_jar = cookielib.MozillaCookieJar(cookiefile)

		if(os.access(cookiefile, os.F_OK)):
				self.cookie_jar.load()
		self.opener = urllib2.build_opener(
			urllib2.HTTPRedirectHandler(), 
			urllib2.HTTPHandler(debuglevel=0), 
			urllib2.HTTPSHandler(debuglevel=0), 
			urllib2.HTTPCookieProcessor(self.cookie_jar)
		)
		
		self.loginToBrightShadows()

		self.cookie_jar.save()

	def loginToBrightShadows(self):
		""" do a login """
		params = urllib.urlencode({'edit_username':self.login, 
								   'edit_password':self.password, 
								   'submitted':'1'})

		response = self.opener.open(baseurl + loginpath, params)
		print "login action complete"
		return ''.join(response.readlines())
		
