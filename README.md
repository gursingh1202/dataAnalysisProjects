# Data Analysis & Data Mining

This repository contains various data analysis and data mining projects, each explained in its respective section.

## Web Scraper (Newsdata BBC)
**Location:** `Webscraper_newsdata` folder

### Files:
- **Webscraper.py:** Contains code to extract data from the BBC news site, customized for this purpose only.
- **filtering_data.py:** Filters data articles for relevancy.
- **article_Data.json** and **article_links.json:** Recovered data files storage.

### Scope
The web scraper is built to extract and filter BBC news article headlines and links for further projects.

### Language 
Python

### Modules
`requests_html`, `time`, `parser`, `datetime`, `json`, `os`

### Usage
To use:
1. Run the `webscraper.py` file. If it runs correctly, it will create a JSON file.
2. Run the `filtering_data.py` file to produce the current list of results.

## Stock Data Manipulation
**Location:** `stock_data` folder

### Scope
To investigate existing data and create machine learning models as part of a larger project.

### Language 
Python

### Modules
`seaborn`, `matplotlib`, `pandas`, `os`, `scikit-learn`

### Usage
To use:
1. Upload datasets to Google Drive.
2. Run the files in Google Colab by executing each line to see the results.


## Web Scraper (Robot.txt checker)
**Location:** `robot_checker` folder

### Files:
- **robot_checker.py:** Contains code to extract robot.txt text from the url site indicated.
- **links.csv:** URL links sto be extracted.
- **results.json** and **article_links.json:** Recovered data files storage.

### Scope
The web scraper is to extract robot.txt file if one is present and store in json file for later use.

### Language 
`Python`

### Modules
`requests_html`, `time`, `parser`, `datetime`, `json`, `os`

### Usage
To use:

1. Change the `links.csv` file to wanted site URLs.
2. Run the `robot_checker.py` file. If it runs correctly, it will append a JSON file.

