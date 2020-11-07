import asyncio
import aiohttp
from random import randint

from estruturas.pokemon import Pokemon
from estruturas.lista import ListaEncadeada


url_base: str = "https://pokeapi.co/api/v2/pokemon/"


async def captura_pokemon(id: int, lista: ListaEncadeada) -> None:
    async with aiohttp.ClientSession() as sessao:
        async with sessao.get(f'{url_base}{id}') as resposta:
            pokemon_dict: dict = await resposta.json()

            nome: str = pokemon_dict["name"]
            altura: float = pokemon_dict["height"]
            peso: float = pokemon_dict["weight"]
            tipo: str = pokemon_dict["types"][0]["type"]["name"]

            pokemon = Pokemon(id, nome, altura, peso, tipo)
            lista.inserir(lista.tamanho+1, pokemon)


def captura_pokemons(quantidade: int = 1, aleatorio: bool = False) -> list:
    """ Busca na api a quantidade de Pokemons passada como parametro e
    retorna uma lista
    """
    pokemons: ListaEncadeada = ListaEncadeada()
    loop: object = asyncio.get_event_loop()
    quantidade_liq: int = quantidade if quantidade <= 890 else 890

    print("\nBuscando pokemons, aguarde...")

    loop.run_until_complete(
        asyncio.gather(
            *(captura_pokemon(randint(1, 890) if aleatorio else i+1, pokemons) for i in range(quantidade_liq))
        )
    )

    if aleatorio and quantidade > 890:
        for _ in range(quantidade - 890):
            pokemons.inserir(pokemons.tamanho+1,
                             pokemons.elemento(randint(0, 889)))
    elif quantidade > 890 and not aleatorio:
        raise Exception("Só existem 890 pokemons.")

    return pokemons
