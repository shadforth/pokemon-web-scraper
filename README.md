# Pokémon Web Scraper

A web scraper made with Python that scrapes Serebii.net. Mostly made for my [Vue Pokedex](https://github.com/shadforth/vue-pokedex) project.

## Getting Started

### Prerequisites

- Python
- pip

To get started, make sure Python is installed on your machine. Detailed instructions on how to install Python can be found at [Real Python](https://realpython.com/installing-python/). To check that Python is successfully installed, run the following command in terminal.

```bash
python --version
```

Next, install Python's package manager, pip. Instructions on how to install pip can be found at [PyPA]. Check that pip was successfully installed by running the following command.

```bash
pip --version
```

Finally, install the required Python packages by navigating to the project directory and running the following command.

```bash
pip install -r requirements.txt
```

### Usage

In terminal, navigate to the project's `src` folder. Run the following command. By default, this will only retrieve Bulbasaur.

```bash
python scraper.py
```

To specify which Pokémon to retrieve, use the `--min` and `--max` flags.

```bash
python scraper.py --min 1 --max 10
```

To save the output to a JSON file, use the `--save` flag.

```bash
python scraper.py --min 1 --max 10 --save
```

To view the retrieved web output in console, use the `--verbose` flag.

```bash
python scraper.py --verbose
```

For help on running the script, use the `--help` flag.

```bash
python scraper.py --help
```