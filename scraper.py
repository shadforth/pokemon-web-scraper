#!/usr/bin/python3
"""
Scrapes Serebii.net for Pokémon statistics.
"""
import argparse
import bs4
import json
import logging
import re
import requests

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

OUTPUT_FILE = 'pokemon.json'


def setup_arg_parser():
    """
    Set up command-line argument parser.
    :return: An ArgumentParser object.
    """
    arg_parser = argparse.ArgumentParser(description='A Pokémon web scraper')
    arg_parser.add_argument('-s', '--save', action='store_true', help='save the output to JSON')
    arg_parser.add_argument('-f', '--first', default=1, type=int, help='the ID of the first Pokémon to retrieve')
    arg_parser.add_argument('-n', '--name', default='charmander', type=str, help='name of the first Pokémon to retrieve')
    arg_parser.add_argument('-l', '--last', default=1, type=int, help='the ID of the last Pokémon to retrieve')
    arg_parser.add_argument('-v', '--verbose', action='store_true', help='print the Pokémon\'s statistics to console')
    return arg_parser.parse_args()


def scrape_pokemon(first_id: int, last_id: int, args):
    """
    Orchestrates scraping data based on a given Pokémon ID range.
    """
    data_list = []

    for poke_id in range(first_id, last_id + 1):
        data = extract_statistics(poke_id)
        data_list.append(data)

        if args.verbose or not args.save:
            display_formatted(data)
        else:
            logging.info('Scraped %s %s', data['number'], data['name'])

    if args.save:
        logging.info('Saving to %s', OUTPUT_FILE)
        save_to_json(data_list)
    else:
        logging.info('All Pokémon retrieved! To save to JSON, use the --save flag')


def extract_statistics(poke_id: int) -> object:
    """
    Scrapes the Serebii.net with a given Pokémon ID.
    """

    if args.name:
        url = 'https://serebii.net/pokedex-sv/{}'.format(args.name.lower())
        print(url)
    else:
        url = 'https://serebii.net/pokedex-sv/{}.shtml'.format(str(poke_id).zfill(3))

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')

    try:
        all_divs = soup.find_all('div', attrs={'align': 'center'})
        center_panel_info = all_divs[1].findAll('td', {'class': 'fooinfo'})

        height = center_panel_info[6].text.split('\r\n\t\t\t')
        weight = center_panel_info[7].text.split('\r\n\t\t\t')

        if center_panel_info[6].find('td', string='Standard'):
            height = center_panel_info[6].find('td', string='Standard').findNext('td').text.replace('"', '" ').split(" ")
            weight = center_panel_info[7].find('td', string='Standard').findNext('td').text.replace('lbs', 'lbs ').split(" ")

        base_stats_td = all_divs[1].find('td', string=re.compile("Base Stats - Total.*")).find_next_siblings('td')
        # Find the 'Effort Values Earned' data
        effort_values = None
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            for i, cell in enumerate(cells):
                if cell.get_text(strip=True).lower() == 'effort values earned':
                    # The effort values are in the next row, same column
                    effort_values_row = rows[rows.index(row) + 1]
                    effort_values = effort_values_row.find_all('td')[i].get_text(strip=True)
                    break
            if effort_values:
                break
    except Exception:
        logging.error('There was an error trying to identify HTML elements on the webpage. URL: %s', url)
        raise

    extracted_pokemon = {
        "name": center_panel_info[1].text,
        "number": '#{}'.format(str(poke_id).zfill(3)),
        "classification": center_panel_info[5].text,
        "height": height,
        "weight": weight,
        "hit_points": int(base_stats_td[0].text),
        "attack": int(base_stats_td[1].text),
        "defense": int(base_stats_td[2].text),
        "sp_att": int(base_stats_td[3].text),
        "sp_def": int(base_stats_td[4].text),
        "speed": int(base_stats_td[5].text),
        "effort_values": effort_values
    }

    return extracted_pokemon


def display_formatted(poke_object):
    """
    Prints a given Pokémon object.
    """
    print('Name\t\t', poke_object['name'])
    print('Number\t\t', poke_object['number'])
    print('Classification\t', poke_object['classification'])
    print('Height\t\t', ' '.join(poke_object['height']))
    print('Weight\t\t', ' '.join(poke_object['weight']))
    print('HP\t\t', poke_object['hit_points'])
    print('Attack\t\t', poke_object['attack'])
    print('Defense\t\t', poke_object['defense'])
    print('Sp.Att\t\t', poke_object['sp_att'])
    print('Sp.Def\t\t', poke_object['sp_def'])
    print('Speed\t\t', poke_object['speed'])
    print('Effort Values\t', poke_object['effort_values'])
    print('-' * 20)


def save_to_json(data: list):
    """
    Save data to file.
    """
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4)


def validate_input(first_id_input: int, last_id_input: int):
    """
    Check if the user-supplied input is valid.
    """
    if first_id_input >= 906 or last_id_input >= 906:
        logging.error('Error: This Pokémon is not yet supported!')
        exit()
    if last_id_input < first_id_input:
        last_id_input = first_id_input
    return first_id_input, last_id_input


if __name__ == '__main__':
    try:
        args = setup_arg_parser()
        logging.info('Extracting data from Serebii.net')
        first_id, last_id = validate_input(args.first, args.last)
        scrape_pokemon(first_id, last_id, args)
    except Exception as ex:
        logging.error(ex)
        raise
