#!/usr/bin/env python
"""
This module scrapes Serebii.net for a given Pokémon.
"""
import requests
import bs4

from colorama import Fore, Back, Style


def get_pokemon_data():
    """
    Scrape Serebii.net for Pokémon data and output to console.
    """

    # Extract data from Serebii.net
    data = requests.get('https://serebii.net/pokedex/001.shtml')
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    all_divs = soup.find_all('div', attrs={'align': 'center'})
    center_panel_info = all_divs[3].findAll('td', {'class': 'fooinfo'})

    pokemon = {}
    pokemon['name']           = center_panel_info[1].text
    pokemon['number']         = center_panel_info[3].text
    pokemon['classification'] = center_panel_info[4].text
    pokemon['height']         = (center_panel_info[5].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
    pokemon['weight']        = (center_panel_info[6].text).replace('\r', '').replace('\n', '').replace('\t\t\t', ',').split(',')
    
    # Get data from stats table
    all_tables = soup.find_all('table', attrs={'class': 'dextable'})
    base_stats_table = all_tables[7].findAll('td')

    pokemon['hit_points'] = base_stats_table[8].text
    pokemon['attack']     = base_stats_table[9].text
    pokemon['defense']    = base_stats_table[10].text
    pokemon['special']    = base_stats_table[11].text
    pokemon['speed']      = base_stats_table[12].text

    # Print the data out nicely
    print_pokemon_data(pokemon)


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
    get_pokemon_data()