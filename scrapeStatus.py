import requests
import time as t
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd


def scrapEidos(url):
    # This will scrape the website make a list and add the name of the eido to
    # the end of the url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dom = etree.HTML(str(soup))
    eido = dom.xpath("//div[@class='item-icon']//..//span//a/@href")
    urlSaver = []
    for i in eido:
        urlSaver.append("https://www.aurakingdom-db.com"+i)
    return urlSaver


def scrapStats(urlEidos):
    # This will scrape the stat from the eido (which is a table that's why
    # pandas), and return it as json
    for url in urlEidos:
        # This gets the urls from scrapEidos and paste them finding
        # the table we want
        response = requests.get(url)

        # This just find the table we whant :)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('th', string='Wish').parent.parent.parent
        # The sleep is there just so we don't spam the website
        t.sleep(2)

        # Using pandas so it reads the html and fixes it in table to convert to json
        df = pd.read_html(str(table))[0]
        # This converts the table to csv
        # df.to_csv(f"eido_stats_{url.split('/')[-1]}.csv", index=False)

        # This converts the table to json
        json_data = df.to_json(orient='records')

        with open(f"eido_stats_{url.split('/')[-1]}.json", 'w') as f:
            f.write(json_data)
        print(f"Stats for {url.split('/')[-1]} extracted!")


if __name__ == '__main__':
    url = 'https://www.aurakingdom-db.com/eidolons'
    urlEidos = scrapEidos(url)
    # This scrapes the stats for each eido
    scrapStats(urlEidos)
