from lxml import html
from lxml import etree
from geopy.geocoders import Nominatim
import requests
import re
from textwrap import TextWrapper
import JobChecker
import time
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


# initialize textwrapper to wrap descriptions so they aren't on one line
tw = TextWrapper(width=80)

geolocator = Nominatim(scheme='http')

page = JobChecker.get_site('https://stackoverflow.com/jobs/feed?location=bridgewater&range=50&distanceUnits=Miles')

# had to use etree as regular tree couldn't output locations the way i wanted to, or rather i couldn't get it to work
etree = etree.fromstring(page.content)
tree = html.fromstring(page.content)

titles = etree.xpath('//title/text()')
descriptions = etree.xpath('//description/text()')
links = etree.xpath('//item/link/text()')
locationsString = tree.xpath('//location/text()')
# locationsString = etree.xpath('//location[*]/text()')

cleanedDescriptionsList = JobChecker.cleanPageContent(descriptions)
cleanedTitlesList = JobChecker.cleanPageContent(titles)

userDefinedKeyword = JobChecker.getUserDefinedKeyword()


# re.escape changes user input with special characters to be able to search for keywords such as C++
userDefinedKeywordAfterReEscape=re.escape(userDefinedKeyword)

indexListOfMatchingJobs = JobChecker.searchDescriptionsForKeyword(cleanedDescriptionsList, userDefinedKeywordAfterReEscape)

userDefinedRange = JobChecker.getUserInput(len(indexListOfMatchingJobs))

listOfLatLon = []

jobCounter = 0
#for x in range(userDefinedRange):
for x in indexListOfMatchingJobs:
    if jobCounter==userDefinedRange:
        break
    jobCounter = jobCounter + 1
    #add two to not use StackOverflow site/page titles (line up the titles with everything else)
    print("Title: " + cleanedTitlesList[x+2])
    print("Link: " + links[x])
    print("Location: " + locationsString[x])
    location = geolocator.geocode(locationsString[x], timeout=10)
    #print("Latitude, Longitude: " + str(location.latitude), str(location.longitude))
    listOfLatLon = JobChecker.listOfLatLonUpdate(listOfLatLon, location.latitude, location.longitude)

    #add one to line up descriptions with everything else
    descStr = cleanedDescriptionsList[x+1]
    print("\n".join(tw.wrap(descStr))[:800] + "...*****TO READ REST OF DESCRIPTION GO TO LINK*****")
    print("\n")
    #pause to not overload geolocator.geocode
    time.sleep(.1)

print("**********PLEASE WAIT UP TO 15 SECONDS FOR MAP TO LOAD**********")
map = JobChecker.mapSetup()
JobChecker.plotPoints(listOfLatLon, map)
plt.title("Jobs within 50 miles of Bridgewater MA with keyword '" + userDefinedKeyword + "' in description")
plt.show()
