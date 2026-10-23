# PokeDollar / PokeReal

A Streamlit app that checks the US dollar exchange rate in Brazilian reais and identifies the Pokémon corresponding to the current value.

## Features

- Fetches the live USD-BRL exchange rate
- Looks up a Pokémon in the PokéAPI using the converted value as an ID
- Displays the official artwork of the matching Pokémon
- Custom visual interface with CSS styling

## Requirements

- Python 3.10 or higher
- pip

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

On Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## Main dependencies

- streamlit
- requests

## Project structure

```text
POKECOTACAO/
├── app.py
├── style.css
├── README.md
├── requirements.txt
├── .gitignore
└── .venv/
```

## Note

The application uses the following APIs:

- AwesomeAPI for the dollar exchange rate
- PokéAPI to fetch the Pokémon data
