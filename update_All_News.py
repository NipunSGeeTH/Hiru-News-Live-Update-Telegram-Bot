import requests
from bs4 import BeautifulSoup
import time 
import json


    
def scrape_hirunews_page(url):
    """Scrapes news articles from a single page of Hiru News."""

    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'lxml')

    articles = []
    article_elements = soup.find_all('div', class_='row', style='margin-bottom:10px') 

    for article_element in article_elements:
        try:
            title_element = article_element.find('div', class_='all-section-tittle').find('a')
            title = title_element.text.strip() if title_element else "N/A"
            link = title_element['href'] if title_element else "N/A"
            news_id = link.split("/")[-2] if link else "N/A"

            date_time_element = article_element.find('div', class_='middle-tittle-time')
            date_time = date_time_element.text.strip() if date_time_element else "N/A"

            # Extract image link
            image_element = article_element.find('div', class_='sc-image').find('img')
            image_link = image_element['src'] if image_element else "N/A" 

            articles.append({
                'news_id': news_id,
                'title': title,
                'link': link, 
                'date_time': date_time,
                'image_link': image_link
               

            })
        except Exception as e:
            print(f"Error scraping article: {e}")

    return articles

def run_scraper():
    base_url = 'https://www.hirunews.lk/local-news.php?pageID='
    num_pages = 1  # Scrape the first 2 pages (adjust as needed)

    all_articles = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        print(f"Scraping page: {url}")
        all_articles.extend(scrape_hirunews_page(url))
        time.sleep(1)  


    with open("hirunews_articles.json", "w", encoding='utf-8') as json_file:
        json.dump(all_articles, json_file, ensure_ascii=False, indent=4)

    # Output or further process the scraped data


# This will only run if you execute scraper.py directly
if __name__ == '__main__': 
    run_scraper() 