#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This module scrapes Serebii.net for Pokémon statistics.
"""
import argparse
import json
import logging
import bs4
import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

OUTPUT_FILE = 'pokemon.json'

PARSER = argparse.ArgumentParser(description='A Pokémon web scraper')
PARSER.add_argument('-s', '--save', action='store_true',
                    help='save the output to JSON')
PARSER.add_argument('-f', '--first', default=1, type=int,
                    help='the number of the first Pokémon to retrieve')
PARSER.add_argument('-l', '--last', default=1, type=int,
                    help='the number of the last Pokémon to retrieve')
PARSER.add_argument('-v', '--verbose', action='store_true',
                    help='print the Pokémon\'s statistics to console')
ARGS = PARSER.parse_args()


def get_pokemon_data(urls):
    """
    Scrape Pokémon data from Serebii.net and output to console.
    :param urls: URLs to extract the data from.
    """
    pokemon_list = []

    for url in urls:
        LOGGER.info('Extracting data from Serebii.net')
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        try:
            all_divs = soup.find_all('div', attrs={'align': 'center'})
            center_panel_info = all_divs[1].findAll('td', {'class': 'fooinfo'})
        except Exception:
            LOGGER.error('There was an error trying to identify HTML elements on the webpage.')
            raise

        pokemon = dict()
        pokemon['name'] = center_panel_info[1].text
        pokemon['number'] = center_panel_info[3].text
        pokemon['classification'] = center_panel_info[4].text
        pokemon['height'] = (center_panel_info[5].text).split('\r\n\t\t\t')
        pokemon['weight'] = (center_panel_info[6].text).split('\r\n\t\t\t')

        try:
            base_stats_table = soup.find('a', attrs={'name': 'stats'}).find_next('table')
            base_stats_td = base_stats_table.findAll('td')
        except Exception:
            LOGGER.error('There was an error trying to identify HTML elements on the webpage.')
            raise

        pokemon['hit_points'] = int(base_stats_td[8].text)
        pokemon['attack'] = int(base_stats_td[9].text)
        pokemon['defense'] = int(base_stats_td[10].text)
        pokemon['special'] = int(base_stats_td[11].text)
        pokemon['speed'] = int(base_stats_td[12].text)

        if not ARGS.save or ARGS.verbose:
            print_pokemon_data(pokemon)
        LOGGER.info('Appending %s %s to Pokémon array', pokemon['number'], pokemon['name'])
        pokemon_list.append(pokemon)

    if ARGS.save:
        LOGGER.info('Saving to %s', OUTPUT_FILE)
        save_to_json(pokemon_list)
    else:
        LOGGER.info('All Pokémon retrieved! To save to JSON, use the --save flag')


def save_to_json(pokemon_list):
    """
    Save Pokémon array to JSON file.
    :param pokemon_list: Array of Pokémon data.
    """
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as output_file:
        json.dump(pokemon_list, output_file, indent=4)


def print_pokemon_data(pokemon):
    """
    Print formatted Pokémon data.
    :param pokemon: Pokémon object containing statistics.
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
        URLS = ['https://serebii.net/pokedex/{}.shtml'.format(str(x).zfill(3))
                for x in range(ARGS.first, ARGS.last + 1)]
        get_pokemon_data(URLS)
    except Exception as ex:
        LOGGER.error(ex)
        raise
