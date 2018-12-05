#!/usr/bin/env python
"""
This module scrapes Serebii.net for Pokémon statistics.
"""
import json
import logging
import requests
import bs4

from multiprocessing import Pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIN_POKEMON_NUMBER = 1
MAX_POKEMON_NUMBER = 10
OUTPUT_FILE_NAME = 'pokemon.json'

pokemon_list = []

def get_pokemon_data(url):
    """
    Scrape Serebii.net for Pokémon data and output to console.
    :param url: The URL to extract the data from.
    """

    logger.info('Extracting data from Serebii.net')
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    try:
        logger.info('Extracting main Pokémon information')
        all_divs = soup.find_all('div', attrs={'align': 'center'})
        center_panel_info = all_divs[3].findAll('td', {'class': 'fooinfo'})
    except Exception as e:
        logger.error('There was an error trying to identify elements on the webpage. Error:', e)
        raise

    pokemon = dict()
    pokemon['name']           = center_panel_info[1].text
    pokemon['number']         = center_panel_info[3].text
    pokemon['classification'] = center_panel_info[4].text
    pokemon['height']         = (center_panel_info[5].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
    pokemon['weight']         = (center_panel_info[6].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
    
    try:
        logger.info('Extracting Pokémon statistics from dextable'.format(OUTPUT_FILE_NAME))
        base_stats_table = soup.find('a', attrs={'name': 'stats'}).find_next('table')
        base_stats_td = base_stats_table.findAll('td')
    except Exception as e:
        logger.error('There was an error trying to identify elements on the webpage. Error:', e)
        raise

    pokemon['hit_points'] = int(base_stats_td[8].text)
    pokemon['attack']     = int(base_stats_td[9].text)
    pokemon['defense']    = int(base_stats_td[10].text)
    pokemon['special']    = int(base_stats_td[11].text)
    pokemon['speed']      = int(base_stats_td[12].text)

    print_pokemon_data(pokemon, separators=True)
    pokemon_list.append(pokemon)
    save_to_json(pokemon_list)


def save_to_json(pokemon_list):
    with open(OUTPUT_FILE_NAME, mode='a', encoding='utf-8') as file:
        logger.info('Writing to {}'.format(OUTPUT_FILE_NAME))
        json.dump(pokemon_list, file)


def print_pokemon_data(pokemon, separators=True):
    """
    Print formatted Pokémon data.
    :param pokemon: An object containing a Pokémon's statistics.
    :param separators: Add line separators on either side of the Pokémon statistics.
    """
    if separators:
        print('-' * 30)
    print('Name\t\t', pokemon['name'])
    print('Number\t\t', pokemon['number'])
    print('Classification\t', pokemon['classification'])
    print('Height\t\t', ' '.join(str(i) for i in pokemon['height']))
    print('Weight\t\t', ' '.join(str(i) for i in pokemon['weight']))
    print('HP\t\t', pokemon['hit_points'])
    print('Attack\t\t', pokemon['attack'])
    print('Defense\t\t', pokemon['defense'])
    print('Special\t\t', pokemon['special'])
    print('Speed\t\t', pokemon['speed'])
    if separators:
        print('-' * 30)


if __name__ == '__main__':
    pool = Pool()
    urls = ['https://serebii.net/pokedex/{}.shtml'.format(str(x).zfill(3)) for x in range(MIN_POKEMON_NUMBER, MAX_POKEMON_NUMBER)]
    pool.map(get_pokemon_data, urls)

    with open(OUTPUT_FILE_NAME, 'r') as file:
        file_data = file.read()
    file_data = file_data.replace('][', ',')
    with open(OUTPUT_FILE_NAME, 'w') as file:
        file.write(file_data)