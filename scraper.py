import urllib
from bs4 import BeautifulSoup

page = "http://www.governing.com/gov-data/gentrification-in-cities-governing-report.html"

# query the website and return the html to the variable ‘page’
page = urllib.request.urlopen(page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

# get table with data
table = soup.find("table", attrs={"id": "inputdata"})

data = []
# get the index price
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    count = 0
    city = ""
    index = 0
    for column in columns:
    	if count == 0:
    		city = column.get_text()
    	elif count == 1:
    		index = column.get_text()
    	else:
    		break;
    	count += 1
    data.append([city, index])

data = data[2:]

################################
# get census data on each city #
################################
page = "https://en.wikipedia.org/wiki/List_of_U.S._states_by_educational_attainment"

# query the website and return the html to the variable ‘page’
page = urllib.request.urlopen(page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

# get table with data
table = soup.find("table", attrs={"class": "wikitable sortable"})

edu = {}
# get the educational attainment
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    count = 0
    city = ""
    index = 0
    for column in columns:
    	if count == 0:
    		city = column.get_text()
    	elif count == 3:
    		index = column.get_text()
    	elif count > 3:
    		break;
    	count += 1
    	edu[city] = index

# abbreviations to states
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# iterate through data and get educatiuonal attainment 
for node in data:
	city = node[0]
	state = states[city[-2:]]
	node.append(edu[state])


########################
# get household income #
########################
page = "https://en.wikipedia.org/wiki/List_of_U.S._states_by_income"

# query the website and return the html to the variable ‘page’
page = urllib.request.urlopen(page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

# get table with data
table = soup.find("table", attrs={"class": "wikitable sortable"})

income = {}
# get the income
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    count = 0
    city = ""
    index = 0
    for column in columns:
    	if count == 1:
    		city = column.get_text()
    	elif count == 2:
    		index = column.get_text()
    	elif count > 2:
    		break;
    	count += 1
    	income[city] = index
income["District of Columbia"] = "$75,628"

# iterate through data and get income
for node in data:
	city = node[0]
	state = states[city[-2:]]
	node.append(income[state])

print(data)



