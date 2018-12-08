#!/usr/bin/env python
"""
This module scrapes Serebii.net for Pokémon statistics.
"""
import argparse
import bs4
import json
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_FILE = 'pokemon.json'

parser = argparse.ArgumentParser(description='A Pokémon web scraper')
parser.add_argument('-s', '--save', action='store_true', help='save the output to JSON')
parser.add_argument('-m', '--min', default=1, type=int, help='the number of the minimum Pokémon to retrieve')
parser.add_argument('-mm', '--max', default=1, type=int, help='the number of the maximum Pokémon to retrieve')
parser.add_argument('-v', '--verbose', action='store_true', help='print the Pokémon\'s statistics to console')
args = parser.parse_args()


def get_pokemon_data(urls):
    """
    Scrape Serebii.net for Pokémon data and output to console.
    :param urls: The URLs to extract the data from.
    """
    pokemon_list = []

    for url in urls:
        logger.info('Extracting data from Serebii.net')
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        try:
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

        if not args.save or args.verbose:
            print_pokemon_data(pokemon)
        logger.info('Appending {} {} to Pokémon array'.format(pokemon['number'], pokemon['name']))
        pokemon_list.append(pokemon)

    if args.save:
        logger.info('Saving to {}'.format(OUTPUT_FILE))
        save_to_json(pokemon_list)
    else:
        logger.info('All Pokémon retrieved! To save to JSON, use the --save flag')


def save_to_json(pokemon_list):
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as file:
        json.dump(pokemon_list, file, indent=4)


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
    try:
        urls = ['https://serebii.net/pokedex/{}.shtml'.format(str(x).zfill(3)) for x in range(args.min, args.max + 1)]
        get_pokemon_data(urls)
    except Exception as e:
        logger.error(e)
        raise