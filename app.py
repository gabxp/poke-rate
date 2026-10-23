"""
Streamlit application to check the USD exchange rate and map it to a PokéAPI Pokémon.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
import streamlit as st

TIMEOUT_SECONDS = 10


def carregar_css(caminho_css: str = "style.css") -> None:
    """Reads the local CSS file and injects custom styles into the app."""
    path = Path(caminho_css)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@dataclass
class PokemonInfo:
    id: int
    name: str
    image_url: str


@dataclass
class CurrencyExchange:
    pair: str
    rate: float

    @property
    def formatted_rate(self) -> str:
        return f"{self.rate:.2f}".replace(".", ",")

    @property
    def pokemon_id(self) -> int:
        return int(f"{self.rate:.2f}".replace(".", ""))


class CurrencyService:
    BASE_URL = "https://economia.awesomeapi.com.br/json/last"

    @staticmethod
    @st.cache_data(ttl=60)
    def get_exchange_rate(pair: str = "USD-BRL") -> Optional[CurrencyExchange]:
        url = f"{CurrencyService.BASE_URL}/{pair}"
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()

            key = pair.replace("-", "")
            rate_str = data[key]["ask"]
            return CurrencyExchange(pair=pair, rate=float(rate_str))
        except (requests.RequestException, KeyError, ValueError) as err:
            st.error(f"Error fetching USD exchange rate: {err}")
            return None


class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_pokemon_by_id(pokemon_id: int) -> Optional[PokemonInfo]:
        url = f"{PokemonService.BASE_URL}/{pokemon_id}/"
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()

            name = data.get("name", "").capitalize()
            image_url = data["sprites"]["other"]["official-artwork"]["front_default"]

            if not image_url:
                st.warning(f"Pokémon #{pokemon_id} does not have an official artwork.")
                return None

            return PokemonInfo(id=pokemon_id, name=name, image_url=image_url)
        except (requests.RequestException, KeyError) as err:
            st.error(f"Error fetching PokéAPI for ID #{pokemon_id}: {err}")
            return None


def main():
    # Page configuration
    st.set_page_config(
        page_title="PokeReal",
        page_icon="⚡",
        layout="centered"
    )

    # Load custom styles from style.css
    carregar_css("style.css")

    st.title("PokeDólar -> PokeReal")
    st.markdown(
        "This app tracks the real-time US Dollar (USD-BRL) exchange rate "
        "and finds the Pokémon matching its current value!"
    )

    st.divider()

    # Spinner while loading API requests
    with st.spinner("Fetching current exchange rate and matching Pokémon..."):
        exchange = CurrencyService.get_exchange_rate("USD-BRL")

        if exchange:
            pokemon = PokemonService.get_pokemon_by_id(exchange.pokemon_id)

            # Display metric cards using custom HTML/CSS
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <span class="metric-label">USD Exchange Rate (USD/BRL)</span>
                        <div class="metric-value">R$ {exchange.formatted_rate}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                if pokemon:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <span class="metric-label">Pokémon ID</span>
                            <div class="metric-value">#{pokemon.id}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.divider()

            # Display Pokémon artwork
            if pokemon:
                st.subheader(f"Pokémon of the day: {pokemon.name}")
                st.image(
                    pokemon.image_url,
                    caption=f"Official Artwork - {pokemon.name} (#{pokemon.id})",
                    width="stretch"
                )
                # Adds invisible spacing after image to force container boundary closure
                st.markdown("<div class='bottom-spacer'></div>", unsafe_allow_html=True)

    st.divider()

    # Button to refresh data manually
    if st.button("🔄 Refresh Rate", width="stretch"):
        st.cache_data.clear()
        st.toast("Cache cleared! Fetching updated data...", icon="🔄")


if __name__ == "__main__":
    main()