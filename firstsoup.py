from bs4 import BeautifulSoup
import requests
# import urllib3.contrib.pyopenssl


# urllib3.contrib.pyopenssl.inject_into_urllib3()


# for i in range(1,4):
# r = requests.get("http://www.warcraftlogs.com/reports/byHGWvkqDT8d3CXV#view=rankings&fight=4", verify=True)
# data = r.text
# soup = BeautifulSoup(data, "html.parser")
# print soup
	# rows = soup.findAll('tr', attrs={'class':'odd'})
	# for row in rows:
		# print row


# https://www.warcraftlogs.com/reports/byHGWvkqDT8d3CXV#fight=3&type=healing&source=4

r = requests.get("https://www.warcraftlogs.com/reports/byHGWvkqDT8d3CXV#fight=3&type=healing&source=4", verify=True)
data = r.text
soup = BeautifulSoup(data, "html.parser")
# print soup
rows = soup.findAll('ul', attrs={'id':'filter-fight-boss-dropdown'})
for row in rows:
		print row


s = soup.findAll("table")[3]
for row in s.findAll("tr")[1:]
	print row.findAll("td")[4]["a"]


# https://www.warcraftlogs.com/rankings/report_rankings_for_fight/ + log id + fight + boss ID

# https://www.warcraftlogs.com/rankings/report_rankings_for_fight/jTKCWaMDB8cNwJzV/4/1785

# GET https://www.warcraftlogs.com/reports/graph/healin...034/11102639/source/0/0/0/0/0/0/-1/0/0/Any/Any/0
	
# 200 OK
# 		148ms	
# jquery.min.js (line 6)
	
# 200 OK
# 		557ms	
# jquery.min.js (line 6)
# GET https://www.warcraftlogs.com/rankings/report_rankings_for_fight/byHGWvkqDT8d3CXV/49/1784
	
# 200 OK
# 		996ms	
# jquery.min.js (line 6)
# GET https://www.warcraftlogs.com/rankings/report_rankings_for_fight/byHGWvkqDT8d3CXV/1/1778
	
# 200 OK
# 		620ms	
# jquery.min.js (line 6)
# GET https://www.warcraftlogs.com/rankings/report_rankings_for_fight/byHGWvkqDT8d3CXV/3/1785
	
# 200 OK
# 		923ms


# >>> import re
# >>> import mechanize
# >>> br = mechanize.Browser()
# >>> br.open("https://www.warcraftlogs.com/reports/byHGWvkqDT8d3CXV#fight=3&type=healing&source=4")
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "build/bdist.macosx-10.10-intel/egg/mechanize/_mechanize.py", line 203, in open
#   File "build/bdist.macosx-10.10-intel/egg/mechanize/_mechanize.py", line 255, in _mech_open
# mechanize._response.httperror_seek_wrapper: HTTP Error 403: request disallowed by robots.txt
# >>> br.set_handle_robots(False)
# >>> br.open("https://www.warcraftlogs.com/reports/byHGWvkqDT8d3CXV#fight=3&type=healing&source=4")
# <response_seek_wrapper at 0x102fe2ea8 whose wrapped object = <closeable_response at 0x102fe0908 whose fp = <socket._fileobject object at 0x102fb7e50>>>
# >>> soup = BeautifulSoup(br.response().read())
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'BeautifulSoup' is not defined
# >>> from bs4 import BeautifulSoup
# >>> soup = BeautifulSoup(br.response().read())
# /Users/victoriapayne/src/WCLranks/env/lib/python2.7/site-packages/bs4/__init__.py:166: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("html.parser"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

# To get rid of this warning, change this:

#  BeautifulSoup([your markup])

# to this:

#  BeautifulSoup([your markup], "html.parser")

#   markup_type=markup_type))
# >>> soup = BeautifulSoup((br.response().read()), "html.parser")
# >>> rows = soup.findAll('tr', attrs={'role':'row'})
# >>> for rows in row:
# ...     print row
# ... 
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'row' is not defined
# >>> for row in rows:
# ...     print row
# ... 
# >>> print soup