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
			url_13F_HR = "https://www.sec.gov" + format_col.find("a")['href']
			html_13F_HR = urllib.request.urlopen(url_13F_HR).read()
			return html_13F_HR
			# Because we're only looking for first match:
			break

	# Occurs if first 40 documents don't contain a 13F-HR
	return None 

html_fund_page = get_fund_html("0001166559")
html_13F_HR_page = get_13F_HR_html(html_fund_page)
print(html_13F_HR_page)

