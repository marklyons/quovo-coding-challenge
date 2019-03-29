# Quovo Coding Challenge
My solution to the Quovo Coding Challenge is a command line tool that allows a user to generate .tsv file that outlines the holdings for any fund that is required to submit a 13F-HR form. Additionally, the tool supports a 'date filed' parameter in case the user is looking for an older 13F-HR. The tool also allows the user to instantly plot a pie-chart showing the top ten holdings, but more on that later!

### Setup and Installation
You'll need to install [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), in case the machine you will be using does not already have it installed.
```
pip install bs4
```

### Running the script
To use the example that was emailed to me, to generate the .tsv for CIK: 0001166559, run the following:
```
python edgar-search.py -cik 0001166559
```

This will create a file titled 0001166559.tsv in the same directory. You can run it as many times as you want and it will always return the most recently added 13F-HR.

### Parameters
```
python edgar-search.py -cik CIK -d DATE_FILED -g
```

The -d parameter allows you to specify a date on which the 13F-HR was filed. If there was actually a filing on that date, this will generate all the data from that 13F-HR.

The -g flag does not need an argument, but when included it will display a neat graph like so:
![alt text](graph-example.png "Graph sample")

### Additional Formats