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

def get_13F_html(html_fund_page):
	""" Returns the HTML for the most recent 13F-HR.
			@param html_fund_page: HTML of the fund's EDGAR page.
	"""

	# Use BeautifulSoup to parse HTML
	soup = BeautifulSoup(html_fund_page, features="html.parser")

	# Get results table and then all rows.
	result_table = soup.find("table", {"class": "tableFile2"})
	rows = result_table.findAll("tr")

	# Loop and find first row with 'Filings' = '13F-HR'
	for row in rows:
		# Get the value of first column, but escape if we're in header.
		filings_val = row.find("td").contents[0] if not row.find("th") else "Header"
		
		# We only need the first 13F-HR entry.
		if(filings_val == "13F-HR"):
			format_col = row.findAll("td")[1]
			url_13F = "https://www.sec.gov" + format_col.find("a")['href']
			html_13F = urllib.request.urlopen(url_13F).read()
			return html_13F

	# Occurs if first 40 documents don't contain a 13F-HR
	return None 

def get_13F_text_url(html_13F_page):
	# Use BeautifulSoup to parse HTML
	soup = BeautifulSoup(html_13F_page, features="html.parser")
	documents_table = soup.find("table", {"class": "tableFile"})

	# It looks like it will always be last item.
	last_row = documents_table.findAll("tr")[-1]
	url_col = last_row.findAll("td")[2]
	text_url = "https://www.sec.gov" + url_col.find("a")['href']
	return text_url

html_fund_page = get_fund_html("0001166559")
html_13F_page = get_13F_html(html_fund_page)
text_url_13F = get_13F_text_url(html_13F_page)

