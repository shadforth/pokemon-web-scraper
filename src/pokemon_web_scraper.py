#!/usr/bin/env python
"""
This module scrapes Serebii.net for Pokémon statistics.
"""
import json
import logging
import pprint
import requests
import bs4

from colorama import Fore, Back, Style

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_FILE_NAME = 'pokemon.json'


def get_pokemon_data(min_number=1, max_number=1, save_json=False):
    """
    Scrape Serebii.net for Pokémon data and output to console.
    :param min_number: The lower bound Pokémon number to retrieve.
    :param max_number: The upper bound Pokémon number to retrieve.
    :param save_json: Save the information to a JSON file.
    """

    if save_json:
        all_pokemon = []

    for i in range(min_number, (max_number + 1)):
        # Extract data from Serebii.net
        logger.info('Extracting data from Serebii.net')
        url = 'https://serebii.net/pokedex/{}.shtml'.format(str(i).zfill(3))
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        try:
            logger.info('Extracting main Pokémon information')
            all_divs = soup.find_all('div', attrs={'align': 'center'})
            center_panel_info = all_divs[3].findAll('td', {'class': 'fooinfo'})
        except Exception as e:
            logger.error('There was an error trying to identify elements on the webpage. Error:', e)
            raise

        pokemon = {}
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

        # Print the data out nicely
        print('=' * 30)
        print_pokemon_data(pokemon)
        print('=' * 30)

        if save_json:
            all_pokemon.append(pokemon)
    
    if save_json:
        logger.info('Writing to {}'.format(OUTPUT_FILE_NAME))
        output_file = open(OUTPUT_FILE_NAME, 'w+')
        output_file.write(json.dumps(all_pokemon))
        output_file.close()


def print_pokemon_data(pokemon):
    """
    Print formatted Pokémon data.
    :param pokemon: An object containing a Pokémon's statistics.
    """
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


if __name__ == '__main__':
    get_pokemon_data(min_number=10, max_number=20, save_json=False)