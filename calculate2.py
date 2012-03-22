import re
import getpass

from login import LoggerInner
from webutils import WebUtils

from calculator2 import Calculator2

bs_username = "cYate"
bs_password = ""

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

challengepath = "/challenges/programming/calculate2"
linkPath = challengepath + "/tryout.php"
solutionPath = challengepath + "/solution.php"

if __name__ == '__main__':
    bs_password = getpass.getpass("Enter password:")
    LoggerInner(bs_username, bs_password, cookiefile)
    pageGetter = WebUtils(cookiefile, baseurl)
    problem = pageGetter.getHTML(linkPath)
    print problem
    v = re.search('\"[\[\]0-9a-zA-Z+-=]*\"', problem)
    print v.group()

    calculator = Calculator2(v.group())
    calculator.Solve()

#    print calculator.result

    solutionParams = "?solution="
    solpath = "%s%s%s" %(solutionPath, solutionParams, calculator.stringResult)
    print solpath
    print pageGetter.getHTML(solpath)
