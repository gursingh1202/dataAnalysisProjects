
################################
#Webscraper to check for robot.txt file of any website
#Author: Gurpreet Singh
#Date: 07/03/2025
################################


import requests
from bs4 import BeautifulSoup
import csv
import json
#modules needed to run file

def checker(url):
    #checks for robot.txt file of any website and gets the content of the file
    try:
        url = url
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
            
        elif response.status_code == 400:
            print('Error: Bad request')
        elif response.status_code == 403:
            print('Error: Forbidden')
        elif response.status_code == 500:
            print('Error: Internal server')
        elif response.status_code == 404:
            print('Error: Page not found')
        elif response.status_code == 503:
            print('Service unavailable')
        else:
            print('Error: Unknown error')
    except Exception as e:
        print(f"Error: {e}")


def get_links(file):
    #gets links from the input url file and returns a list of links
    file = file
    links = []
    if file.endswith(".csv"):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for link in reader:
                links.append(link)
    elif file.endswith(".json"):
        with open(file, 'r') as f:
            data = json.load(f)
            for link in data:
                links.append(link)
    elif file.endswith(".txt"):
        with open(file, 'r') as f:
            for link in f:
                links.append(link)
    return links


def write_json(url, soup):
     #writes the result of the robot.txt file to a json file along with url
    try:
        with open('results.json', 'r') as file:
            data = json.load(file)  
    except FileNotFoundError:
        data = {}
    data[url] = str(soup)
    with open('results.json', 'w') as file:
        json.dump(data, file, indent=4)

def main(file):
    #main function that calls other functions
    links = get_links(file)
    try:

        for url in links:
            soup = checker(url[0])
            write_json(url[0], soup)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    file = 'links.csv'
    main(file)

        
    