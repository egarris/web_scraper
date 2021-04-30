from bs4 import BeautifulSoup
import os
import requests
import string


def scraper(page_num, content_type):
    """Scrapes articles from the scientific journal Nature and writes each 
    one to a separate file.

    :param page_num: int
        Number of pages to scrape.
    :param content_type: str
        Type of article to scrape.
    :return: None
    """
    for i in range(1, page_num + 1):
        n = str(i)
        url = f'https://www.nature.com/nature/articles?searchType=journal\
                Search&sort=PubDate&page={n}'

        r = requests.get(url)
        page_content = r.content

        soup = BeautifulSoup(page_content, 'html.parser')

        # Create directory for scraped page and change working directory
        dir_name = f'Page_{n}'
        os.mkdir(dir_name)
        os.chdir(dir_name)

        for article in soup.find_all('article'):
            # Find article type
            article_type = article.find('span', class_='c-meta__type').text

            if article_type == content_type:
                # Find article title
                title = article.find('a').text

                # Find article path and combine with domain
                path = article.find('a')['href']
                article_url = f'http://www.nature.com{path}'

                # Get and parse content from article body
                r = requests.get(article_url)
                soup = BeautifulSoup(r.content, 'html.parser')
                article_body = soup.find('div', class_='article-item__body')\
                                    .text.strip()

                # Remove punctuation from article titles and make filename
                translator = title.maketrans('', '', string.punctuation)
                title_no_punc = title.translate(translator)
                filename = title_no_punc.replace(' ', '_')

                # Write article body to file
                file = open(f'{filename}.txt', 'w', encoding='utf-8')
                file.write(article_body)
                file.close()

        # Reset working directory to parent folder
        os.chdir(os.path.dirname(os.getcwd()))


def main():
    pages = int(input())
    content = input()

    scraper(pages, content)


if __name__ == '__main__':
    main()
