import requests
from bs4 import BeautifulSoup
import csv
 
  
# Get list of states
loc = "https://www.loc.gov/rr/geogmap/sanborn/"
html = requests.get(loc).text
soup = BeautifulSoup(html, "lxml")
states_html = soup.find("select", {"id": "stateID"}).find_all("option")
state_lookup= {}
for state in states_html:
  state_lookup[state['value']] =  state.text
del(state_lookup['BLANK'])  #  remove the "BLANK" option
state_lookup


state_loc = "https://www.loc.gov/rr/geogmap/sanborn/states.php?stateID={0}"
state_urls = [state_loc.format(state) for state in state_lookup]
state_urls

city_urls = []
iteration = 0
city_loc = "https://www.loc.gov/rr/geogmap/sanborn/{0}"
for state_url in state_urls:
    print(iteration)
    iteration += 1
    html = requests.get(state_url).text
    soup = BeautifulSoup(html, "lxml")
    for table in soup.find_all('table')[1:]:
        if "Fire Insurance Maps of" in table.text:
            city_table = table.table  # we want the nested table
            break
    for row in city_table.find_all('tr'):
        city = city_loc.format(row.a['href'])
        city_urls.append(city.replace(" ", "%20"))
        print(city)
        
        
# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
        
dates = []
sheets = []
geos = []
comments = []
urls = []
cities = []
states = []
iteration = 0
for loc in city_urls:
    print(iteration, ":", loc)
    iteration += 1
    html = requests.get(loc).text
    soup = BeautifulSoup(html, "lxml")
    for table in soup.find_all('table')[1:]:
        if "Fire Insurance Maps of" in table.text:
            sheet_table = table.table  # we want the nested table
            rows = sheet_table.findAll("td")
            breakdown = list(chunks(rows, 5))
            for item in breakdown:
                number = 0
                while len(item) > number:
                    if number == 0:
                        date = item[0].getText()
                        dates.append(date)

                        final_url_element = loc.split('?')[-1]
                        city = final_url_element[5:-11]
                        print('city:',city)
                        state = ''.join(final_url_element.split('=')[2:])
                        print('state:',str(state))

                        states.append(state)
                        cities.append(city)

                    if number == 1:
                        sheet = item[1].getText()
                        sheets.append(sheet)        
                    if number == 2:
                        geo = item[2].getText()
                        geos.append(geo)      
                    if number == 3:
                        comment = item[3].getText()
                        comments.append(comment)
                    if number == 4:
                        url = item[4].getText()
                        urls.append(url)

                    number = number + 1

#Writing out the results as a CSV file
print("outputing csv")
with open('loc.csv','w') as file:
    rowlists = zip(cities, states, dates, sheets, geos, comments, urls)
    writer = csv.writer(file)
    for row in rowlists:
        writer.writerows([row])        
