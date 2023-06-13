import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

# Define the URLs of the websites you want to scrape
urls = [
    "https://www.repubblica.it/sport/",
    "https://www.corrieredellosport.it/",
    "https://www.gazzetta.it/",
]

app = Flask(__name__)

@app.route('/')
def headlines():
    all_headlines = []
    all_links=[]
    for url in urls:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if 'repubblica.it' in url:
                headlines = soup.find_all('h2', class_='entry__title')
                for titolo in headlines:
                    titoli = titolo.find_all('a')
                    all_headlines.extend(titolo.get_text(strip=True) for titolo in headlines)

                
                h2_tags = soup.find_all('h2',class_='entry__title')
                for h2 in h2_tags:
                    # Find links within h2 tag
                    links = h2.find_all('a')
                    for link in links:
                        href = link.get('href')
                        all_links.append(href)


                all_headlines.extend(headline.get_text(strip=True) for headline in headlines)
                
                
            elif 'corrieredellosport.it' in url:
                headlines = soup.find_all('h2', class_='ArticleTitle_title__iTnVk silka-n8-teaser')
                all_headlines.extend(headline.get_text(strip=True) for headline in headlines)
                
            elif 'gazzetta.it' in url:
                headlines = soup.find_all('h4', class_='title is--medium')
                all_headlines.extend(headline.get_text(strip=True) for headline in headlines)
        
            
        else:
            return f"Failed to retrieve data from {url}"
    #print(all_links)
    return render_template('index.html', headlines=all_headlines, links=all_links)



if __name__ == '__main__':
    app.run()

