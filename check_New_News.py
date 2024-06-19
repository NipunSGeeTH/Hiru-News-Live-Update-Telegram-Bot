import json
import requests
from bs4 import BeautifulSoup

# Load the last update ID
def get_and_save_latest_news():
    with open('last_News_update_ID.json', 'r') as f:
        last_update = json.load(f)
        last_id = int(last_update['ID'])

    # Load the news articles
    with open('hirunews_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Find new articles
    new_articles = [article for article in articles if int(article['news_id']) > last_id]

    # Display and save new articles
    if new_articles:
        latest_news = []
        for article in new_articles:



            url=article['link']
              

            

            response = requests.get(url)
            response.raise_for_status()  

            soup = BeautifulSoup(response.content, 'lxml')
            paragraph_div = soup.find('div', id='article-phara2')

            if paragraph_div:
                for br in paragraph_div.find_all("br\br"):
                    br.replace_with("\n")  
                paragraph_text = paragraph_div.get_text(separator="\n")
                paragraph_text = paragraph_text.strip()
                paragraph_text = paragraph_text[:900]
                print(paragraph_text)
            else:
                print("Paragraph not found") 




            news_item = {
                "ID": article['news_id'],
                "Title": article['title'],
                "Link": article['link'],
                "Date": article['date_time'],
                "Image": article['image_link'],
                "Paragraph" : paragraph_text
            }
            latest_news.append(news_item)
            

        # Save the new articles to Latest_News.json
        with open('Latest_News.json', 'w', encoding='utf-8') as f:  # 'w' mode overwrites the file
            json.dump(latest_news, f, ensure_ascii=False, indent=4)

        # Update the last news update ID with the latest news ID from the new articles
        new_last_id = max(int(article['news_id']) for article in new_articles)
        last_update['ID'] = new_last_id

        # Save the updated last news update ID
        with open('last_News_update_ID.json', 'w') as f:
            json.dump(last_update, f, indent=4)

        print(f"Updated last news update ID to {new_last_id}")
    else:
        print("No new articles found.")
        # Clear the contents of Latest_News.json
        with open('Latest_News.json', 'w', encoding='utf-8') as f:
            f.write("[]")  # Write an empty JSON array