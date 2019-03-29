import csv
import sys
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
	params = urllib.parse.urlencode({"Find": "Search", "owner": "exclude", "action": "getcompany", "CIK": CIK, "type": "13F-HR", "count": "100"})
	search_url = base_url + params

	# Now, make the request and return the HTML
	search_html = urllib.request.urlopen(search_url).read()
	return search_html

def get_13F_html(html_fund_page, filing_date):
	""" Returns the HTML for the most recent 13F-HR.
			@param html_fund_page: HTML of the fund's EDGAR page.
			@param filing_date: Date in YYYY-MM-DD (optional)
	"""

	# Use BeautifulSoup to parse HTML
	soup = BeautifulSoup(html_fund_page, features="html.parser")

	# Get results table and then all rows.
	result_table = soup.find("table", {"class": "tableFile2"})
	rows = result_table.findAll("tr")

	# Loop and find first row with 'Filings' = '13F-HR'
	for row in rows:
		if not row.find("th"):
			# Get the value of first column
			filings_val = row.find("td").contents[0]

			# Also get the date value, in case the user specified
			date_val = row.findAll("td")[3].contents[0]
	
			# Extract the link
			format_col = row.findAll("td")[1]
			url_13F = "https://www.sec.gov" + format_col.find("a")['href']

			# Date parameter takes precedence
			if filing_date is not None:
				if date_val == filing_date:
					html_13F = urllib.request.urlopen(url_13F).read()
					return html_13F
			elif (filings_val == "13F-HR"):
				# Else, we only need the first 13F-HR entry.
				html_13F = urllib.request.urlopen(url_13F).read()
				return html_13F

	# Occurs if first 40 documents don't contain a 13F-HR
	return None 

def get_13F_text_url(html_13F_page):
	""" Returns the URL to the 13F-HR full text file.
			@param html_13F_page: HTML of the 13F-HR page.
	"""
	soup = BeautifulSoup(html_13F_page, features="html.parser")
	documents_table = soup.find("table", {"class": "tableFile"})

	# It looks like it will always be last item.
	last_row = documents_table.findAll("tr")[-1]
	url_col = last_row.findAll("td")[2]
	text_url = "https://www.sec.gov" + url_col.find("a")['href']
	return text_url

def parse_13F_text_file(text_url_13F, CIK):
	""" Parses 13F_HR .txt and produces a TSV file
			@param text_url_13F: String contents of the 13F-HR .txt file.
			@param CIK: The Central Index Key of the desired fund
	"""
	text_13F = urllib.request.urlopen(text_url_13F).read()

	# BeautifulSoup also works for XML!
	parsed_xml = BeautifulSoup(text_13F, "xml")
	# Holdings is contained in second XML block
	holdings_xml = parsed_xml.findAll('XML')[1]
	holdings = holdings_xml.findAll('infoTable')
	tsv_file_name = CIK + ".tsv"

	# CSV writer is easiest to use, just change delimeter.
	with open(tsv_file_name, "w+") as holdings_tsv:
		writer = csv.writer(holdings_tsv, delimiter='\t')

		#Write the header row
		writer.writerow([
			"ISSUER NAME", "CLASS TITLE", "CUSIP", "VALUE ($thousands)",
			"INVESTMENT DISCRETION", "SHRS or PRN AMOUNT", "SH or PRN",
			"VOTING AUTH SOLE", "VOTING AUTH SHARED", "VOTING AUTH NONE" 
		])

		for holding in holdings:
			name_of_issuer = holding.find("nameOfIssuer").contents[0]
			title_of_class = holding.find("titleOfClass").contents[0]
			cusip = holding.find("cusip").contents[0]
			value = holding.find("value").contents[0]
			investment_discretion = holding.find("investmentDiscretion").contents[0]
			sshprnamt = holding.find("sshPrnamt").contents[0]
			sshprnamttype = holding.find("sshPrnamtType").contents[0]
			voting_authority_sole = holding.find("Sole").contents[0]
			voting_authority_shared = holding.find("Shared").contents[0]
			voting_authority_none = holding.find("None").contents[0]

			# Automatically separates with delimeter for us.
			writer.writerow([
				name_of_issuer, title_of_class, cusip, value, 
				investment_discretion, sshprnamt, sshprnamttype, 
				voting_authority_sole, voting_authority_shared,
				voting_authority_none
			])

	holdings_tsv.close()


CIK_in = sys.argv[1]

# Allow user to specify filing date (optional)
filing_date = None
if(len(sys.argv) >= 3):
	filing_date = sys.argv[2]

html_fund_page = get_fund_html(CIK_in)
html_13F_page = get_13F_html(html_fund_page, filing_date)
text_url_13F = get_13F_text_url(html_13F_page)
parse_13F_text_file(text_url_13F, CIK_in)

