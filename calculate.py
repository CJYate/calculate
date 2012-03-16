import sys
import re
import getpass

from login import LoggerInner
from webUtils import WebUtils

from calculator import Calculator

bs_username = "cYate"
bs_password = ""

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

challengepath = "/challenges/programming/calculate"
linkPath = challengepath + "/tryout.php"
solutionPath = challengepath + "/solution.php"

if __name__ == '__main__':
    bs_password = getpass.getpass("Enter password:")
    LoggerInner(bs_username, bs_password, cookiefile)
    pageGetter = WebUtils(cookiefile, baseurl)
    problem = pageGetter.getHTML(linkPath)
    print problem
    v = re.search('\"[0-9a-z+-=_*]*\"', problem)
    print v.group()

    calculator = Calculator(v.group())
    calculator.Solve()
    
    print calculator.result
    
    solutionParams = "?solution="
    solpath = "%s%s%s" %(solutionPath, solutionParams, "")
    print solpath
    print pageGetter.getHTML(solpath)
