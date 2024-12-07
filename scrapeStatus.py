import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import json
import re


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


def separate_stats(stats_string):
    # This will separate the stats from each other and lower casering casering
    # the stats names
    stats_dict = {}
    stats = re.findall(r"(\w+) \+(\d+)", stats_string.lower())
    for stat, value in stats:
        stats_dict[stat] = int(value)
    return stats_dict

    separated_stats = separate_stats(stats_dict)
    print(separated_stats)


def scrapStats(urlEidos):
    # This will scrape the stat from the eido (which is a table that's why
    # pandas), and return it as json
    all_eidos_data = []
    for url in urlEidos:
        # This gets the urls from scrapEidos and paste them finding
        # the table we want
        response = requests.get(url)

        # This just find the table we whant :)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('th', string='Wish').parent.parent.parent

        # Using pandas so it reads the html and fixes it in table to convert to json
        df = pd.read_html(str(table))[0]
        df = df.drop(columns=['Materials'])
        # Using this to save eido name extracted from the URL
        eido_name = soup.find('h1').text.strip()
        # Add eido name, Wish and Level to dataframe for easier manipulation
        df['Eido Name'] = eido_name
        df['wish'] = df['Wish']

        new_df = pd.DataFrame(columns=['eido_name', 'wish'])
        new_df['eido_name'] = eido_name
        new_df['wish'] = df[['Level', 'Wish']].to_dict('records')

        # This set the new structure of the json
        grouped_df = df.groupby('Eido Name')
        for name, group in grouped_df:
            eido_data = {
                "eido_name": name,
                "wishes": []
            }
            for index, row in group.iterrows():
                wish_data = {
                    "wish_number": row['Wish'],
                    "level": row['Level'],
                    "stats": separate_stats(row['Stats'])
                }
                eido_data['wishes'].append(wish_data)
            # Append all eidos to one json
            all_eidos_data.append(eido_data)

        # Save all eidos into one json
        with open('all_eidos_stats.json', 'w') as f:
            json.dump(all_eidos_data, f, indent=4)
        # Prints te result when all eidos stats were extracted
        print("All eido stats extracted and combined!")


if __name__ == '__main__':
    url = 'https://www.aurakingdom-db.com/eidolons'
    urlEidos = scrapEidos(url)
    # This scrapes the stats for each eido
    scrapStats(urlEidos)
