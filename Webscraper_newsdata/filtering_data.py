import json 

def get_data(file):

    with open(file) as file:
            article_links = json.load(file)

    return article_links

def news_links(lst, key, keyword ):

    filtered_data = []
    for e in lst:
        if key == 'title':
            check_title = e[key]
            if keyword in check_title:
                filtered_data.append(e)
                print(filtered_data)
        elif key== 'link':
            check_link = e[key].split('/')
            if keyword in check_link:
                filtered_data.append(e)

        
    return filtered_data

def write_file(file, data):

    json_obj = json.dumps(data, indent=4)
    with open(file, "w") as file:
        file.write(json_obj)

file  = 'article_links.json'
data =get_data(file)
news_filtration = news_links(data,'link', 'news')
stock_filtration = news_links(news_filtration ,'title', 'S&P')
write_file(file, stock_filtration)



                        