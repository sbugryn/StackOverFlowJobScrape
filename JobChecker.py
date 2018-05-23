import requests
import re
from textwrap import TextWrapper
import time
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


def cleanHtml(raw_html, regExToRemove):
    cleanr = re.compile(regExToRemove)
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

def run(SOQuery):
    webResponse = requests.get(SOQuery)
    return webResponse.text

def testUserInput(x):
    #~120 is max number of jobs
    x = int(x)
    if x < 120:
        return x
    else:
        return False

def get_site(url):
    page = requests.get(url)
    return page

def plotPoints(listOfLatLon, map):
    for latLon in listOfLatLon:
        # print (x[1])
        x, y = map(latLon[1], latLon[0])
        map.plot(x, y, 'ro', markersize=3)
        plt.text(x-3900, y+1500, str(latLon[2]), FontSize =8)
        #plt.text(x - 3000, y + 1500, str(latLon[2]), bbox = dict(facecolor='red', alpha=0.5))


def mapSetup():
    plt.figure(figsize=(18, 8))
    map = Basemap(projection='merc', resolution='h', area_thresh=0.1,
                  llcrnrlon=-73.5100, llcrnrlat=41.3500, urcrnrlon=-69.8600, urcrnrlat=42.8900)

    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='#ede0af', lake_color='aqua')
    map.drawstates()
    map.drawmapboundary()
    return map


def listOfLatLonUpdate(listOfLatLon, lat, lon):
    for tup in listOfLatLon:
        if ((tup[0], tup[1]) == (lat, lon)):
            tup[2] = tup[2] + 1
            return listOfLatLon
    listOfLatLon.append([lat, lon, 1])
    return listOfLatLon


def cleanPageContent(input):
    listOfCleanDescriptions = []
    for desc in input:
        # remove html tags
        string = cleanHtml(str(desc), '<.*?>')
        # remove paragraph/font tags
        string = cleanHtml(string, '&.*?;')
        # remove extra spaces
        string = cleanHtml(string, ' +')
        listOfCleanDescriptions.append(string)
    return listOfCleanDescriptions


def searchDescriptionsForKeyword(descriptions, keyword):
    listOfMatchingJobs = []
    for index, desc in enumerate(descriptions):
        if re.search(keyword, desc, re.IGNORECASE):
            listOfMatchingJobs.append(index)
    #remove reduntant last entry
    del listOfMatchingJobs[-1]
    return listOfMatchingJobs


def getUserInput(numOfJobs):
    print("Found ", numOfJobs, " jobs.")
    userDefinedRange = input("How many jobs would you like to see plotted on map (please input an integer that is <= the number of jobs found)?")
    print("\n")
    while not userDefinedRange.isdigit() or int(userDefinedRange)>numOfJobs:
        print("Invalid input!")
        userDefinedRange = input("Please input an integer that is <= the number of jobs found: ")
    return int(userDefinedRange)


def getUserDefinedKeyword():
    userDefinedKeyword = input("What keyword would you like to filter the results with?")
    print("\n")
    return userDefinedKeyword


def main():

    run('https://stackoverflow.com/jobs/feed?l=Boston%2c+MA%2c+United+States&u=Miles&d=50')


if __name__ == '__main__':
    main()