###
#WebScraper
#OOP designed software to scrape data off given website and collect publicly available data of the webite.
#Gurpreet singh
#21131818
###

from requests_html import HTMLSession
from time import sleep
import parser
import datetime 
import json
import os
#import all required modules

class Webscraper():


    def  __init__(self, url) -> None:
        #initial constructor creation
        self.session = HTMLSession()
        self.base_url = "https://www.bbc.co.uk/"
        self.url = url
        
    def load_html (self):
        #load the html for the webpage
        self.reader = self.session.get(self.url)
        self.reader.html.render(sleep=1, scrolldown=0)
        
    def close(self):
        #used to complete session and free all resources
        self.session.close()    

    def fetch_aldata(self, div_finder):
        #this selects the link and title from the div by finding correct data in the html div
        divs = self.reader.html.find(div_finder)
        data = []
        for div in divs:
            # Goes through specific objects to fetch data
            link_element = div.find("a", first=True)
            if link_element:
                link = link_element.attrs.get('href', '')
                title = link_element.text
                data.append({'title':title, 'link': link})
        return data
    
    def fetch_adata(self):

        article_data = []
        msg = "No"
        article = ''
        title = (self.reader.html.find('title', first=True) or self.reader.html.find('h1', first=True) or msg).text.strip()

        try:
            paragraphs = self.reader.html.find('article')
            if paragraphs:
                for p in paragraphs:
                    article += p.text.strip() 
            else:
                article = msg
        except Exception as e:
            print(f"An error occurred: {e} article")
        
        date = None
        try:
            time_elements = self.reader.html.find('time')
            if time_elements:
                
                date_published = time_elements[0].text.strip() or time_elements[0].datetime.strip()
                try:
                    date_published = parser.parse(date_published, default=datetime(datetime.now().year, 1, 1))
                    date_published = date_published.strftime('%d-%m-%Y')
                except:
                    date_published = msg


            else:
                date_published = msg
        except Exception as e:
            print(f"An error occurred: {e} time")

        

        try:
            author = self.reader.html.find('.ssrcss-68pt20-Text-TextContributorName', first=True) or self.reader.html.find('meta-reporter', first=True)
            author = author.text

            if not author:
                author = 'BBC News'
        except Exception as e:
            print(f"An error occurred: {e} author")
        
        article_data.append({'title': title, 'article': article, 'Publishdate': date_published, 'author':author, 'link': self.url})
        
        return article_data

    def pagination(self):
        #get links for all successive pages of the results
        self.reader = self.session.get(self.url)
        npg_links = []
        for link in self.reader.html:
            if link.search("page="):
                link = str(link)
                link = link.split("'")[1]
                npg_links.append(link)

            else:
                break 
        return npg_links  
    
    def link_format(self):
        #check url is correct format
        search_ext = self.url
        if search_ext and not search_ext.startswith("https://"):
                self.url = self.base_url + search_ext
        else:
            self.url = search_ext
            return self.url
        

    def file_checker(self, found, filename):

        path = os.path.dirname(os.path.realpath(__file__))
        destination = ""
        if found == False:

            for root, dirs, files in os.walk(path):
                for file in files: 
                    if file.endswith('.json') and file.startswith(filename):
                        destination =  (root+'/'+str(file))
                        found = True

        return found, destination 

    def datatype_conversion(self, found, data, destination):

        if found  == False:
            
            json_obj = json.dumps(data, indent=4)
            with open(destination, "w") as crfile:
                crfile.write(json_obj)
                found = True
            return found, 'File created and data stored successfully'
        
        elif found == True:
            with open(destination, 'r+')  as file:
                json_obj = json.load(file)
            for item in data:
                json_obj.append(item)

            with open(destination, 'w') as file:
                json.dump(json_obj, file, 
                            indent=4,  
                            separators=(',',': '))
                
            return found, 'data stored successfully'
       
    def fetch_adata_links(self,filename):
        with open(filename, 'r+') as file:
            link_data = json.load(file)
            return link_data
         
    def div_select(self):
        #div selector for specific data needed from html
        if self.url  and not self.url.endswith("NEWS_PS") or self.url.find("page="):
            div_finder = ".ssrcss-tq7xfh-PromoContent > *"
        
        else:
            div_finder= "h1.ssrcss-1j5vay3-Heading.e1hq9lx0"
            #should be for individual article page - find specific div that correllates with the data needed 
            #might need more thn one check page
        
        return div_finder

def get_article_link_data ():
    #runs all the function and evokes the object
    has_run = False
    div_finder = ".ssrcss-tq7xfh-PromoContent > *"
    found  = False
    filename = 'article_links'
    


    while has_run  == False:
        url = "search?q=s%26p+500&seqId=e1005640-2774-11ef-b757-6398eaf17df6&d=NEWS_PS"
        scraper = Webscraper(url)
        scraper.link_format()
        npg_links = scraper.pagination()
        has_run = True
        found, destination = scraper.file_checker(found, filename)
        if found  == False:
            destination = 'article_links.json'
        scraper.close()

    
    try:

        for link in npg_links:
            url = link
            scraper = Webscraper(url)
            div_finder = scraper.div_select()
            scraper.load_html()
            data = scraper.fetch_aldata(div_finder)
            found, message = scraper.datatype_conversion(found, data, destination)
            print (message)
            for item in data:
                print(item)
            sleep(1)
            scraper.close()
            print(found)

    except Exception as e:
        print(f"An error occurred: {e}")


def get_article_data():
    url = "search?q=s%26p+500&seqId=e1005640-2774-11ef-b757-6398eaf17df6&d=NEWS_PS"
    scraper = Webscraper(url)
    al_file = 'article_links.json'
    a_file = 'article_data.json'
    url = scraper.fetch_adata_links(al_file)
    found = False
    found, filename = scraper.file_checker(found, al_file)
    link_data = scraper.fetch_adata_links(filename)
    found = False
    found, destination = scraper.file_checker(found, a_file)
    if found == False:
        destination = a_file
        print(destination)


    try:

        for link in link_data:
            url = (link['link'])
            scraper = Webscraper(url)
            scraper.load_html()
            data = scraper.fetch_adata()
            found, message = scraper.datatype_conversion(found, data, destination)
            print(message)

            scraper.close()
      

    except Exception as e:
        print(f"An error occurred: {e}")

         

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    get_article_data ()




if __name__ == "__main__":
    main()

