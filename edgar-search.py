import urllib.request
import urllib.parse 
from bs4 import BeautifulSoup

def get_fund_html(CIK):
	""" Returns the HTML for our fund page with all the documents.
			We are passing the CIK directly, so it will be an exact match.
			@param CIK: The Central Index Key of the desired fund
	"""

	# First, encode our parameters to be safe and append
	base_url = "https://www.sec.gov/cgi-bin/browse-edgar?"
	params = urllib.parse.urlencode({"Find": "Search", "owner": "exclude", "action": "getcompany", "CIK": CIK})
	search_url = base_url + params

	# Now, make the request and return the HTML
	search_html = urllib.request.urlopen(search_url).read()
	return search_html

def get_13F_HR_html(html_fund_page):
	# Use BeautifulSoup to parse HTML
	soup = BeautifulSoup(html_fund_page)

	# Get results table, find first row with Filings=13F-HR
	table_rows = soup.find("table", {"class": "tableFile2"})
	print(table_rows)


html_fund_page = get_fund_html("0001166559")
html_13f_HR_page = get_13F_HR_html(html_fund_page)
