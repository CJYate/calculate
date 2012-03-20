import os
import urllib2
import cookielib


class WebUtils(object):
    """ Utils for logging in and retrieving/posting stuff to BrightShadows
    """

    def __init__(self, cookiefile, base_url):
        self.cookie_jar = cookielib.MozillaCookieJar(cookiefile)
        self.base_url = base_url

        print "baseurl = ", self.base_url
        if(os.access(cookiefile, os.F_OK)):
            self.cookie_jar.load()

        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cookie_jar)
        )

    def getPNG(self, pagePath, targetFilename):
        print "reading path " + pagePath
        response = self.opener.open(self.base_url + pagePath)
        pic = response.read()
        fout = open(targetFilename, "wb")
        fout.write(pic)
        fout.close()

        print "file written to " + targetFilename

    def getHTML(self, pagePath):
        response = self.opener.open(self.base_url + pagePath)
        return ''.join(response.readlines())
