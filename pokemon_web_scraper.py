#!/usr/bin/env python
"""
This module scrapes Serebii.net for a given Pokémon.
"""
import json
import logging
import pprint
import requests
import bs4

from colorama import Fore, Back, Style

logging.basicConfig(level=logging.DEBUG)

OUTPUT_FILE_NAME = 'pokemon.json'

def get_pokemon_data(limit=10, output_json=False):
    """
    Scrape Serebii.net for Pokémon data and output to console.
    :param limit: The maximum pokemon number to retrieve information from.
    """

    if output_json:
        output_file = open(OUTPUT_FILE_NAME, 'w+')
        all_pokemon = []

    for i in range(1, (limit + 1)):
        # Extract data from Serebii.net
        logging.debug('Extracting data from Serebii.net')
        url = 'https://serebii.net/pokedex/{}.shtml'.format(str(i).zfill(3))
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        try: 
            all_divs = soup.find_all('div', attrs={'align': 'center'})
            center_panel_info = all_divs[3].findAll('td', {'class': 'fooinfo'})
        except Exception as e:
            logging.error('There was an error trying to identify elements on the webpage.')

        pokemon = {}
        pokemon['name']           = center_panel_info[1].text
        pokemon['number']         = center_panel_info[3].text
        pokemon['classification'] = center_panel_info[4].text
        pokemon['height']         = (center_panel_info[5].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
        pokemon['weight']         = (center_panel_info[6].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
        
        # Get data from stats table
        all_tables = soup.find_all('table', attrs={'class': 'dextable'})
        base_stats_table = all_tables[7].findAll('td')

        pokemon['hit_points'] = int(base_stats_table[8].text)
        pokemon['attack']     = int(base_stats_table[9].text)
        pokemon['defense']    = int(base_stats_table[10].text)
        pokemon['special']    = int(base_stats_table[11].text)
        pokemon['speed']      = int(base_stats_table[12].text)

        # Print the data out nicely
        print('=' * 30)
        print_pokemon_data(pokemon)
        print('=' * 30)

        if output_json:
            all_pokemon.append(pokemon)
    
    if output_json:
        logging.info('Writing to {}'.format(OUTPUT_FILE_NAME))
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
    get_pokemon_data(3, True)