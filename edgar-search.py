import urllib.request
import urllib.parse 

def get_13F_HR_page(CIK):
	""" Gets the HTML for our 13F_HR search result page
			We are passing the CIK directl, so it will be an exact match.
  		@param CIK: The Central Index Key of the desired fund
  """

	# First, encode our parameters to be safe and append
	base_url = "https://www.sec.gov/cgi-bin/browse-edgar?"
	params = urllib.parse.urlencode({"Find": "Search", "owner": "exclude", "action": "getcompany", "CIK": CIK})
	search_url = base_url + params

	# Now, make the request and return the HTML
	search_html = urllib.request.urlopen(search_url).read()
	return search_html

def parse_13F_HR_page(html_13F_HR):
	print("test")

html_for_13F_HR = get_13F_HR_page("0001166559")

