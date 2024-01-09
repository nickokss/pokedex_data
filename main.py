import flet as ft
 
import requests

import base64
from urllib.request import urlopen
from PIL import Image
from io import BytesIO

def main(page):
    page.scroll = True
    buffer = BytesIO()
    
    logo_pokedex = ft.Image(
        src=f'logo.png',
        width=270,
        height=140
    )
    nombre = ft.TextField(label="Nombre", autofocus=True)
    submit = ft.ElevatedButton("Consultar")

    pokemon_imagen = ft.Image(
        src="background.png",
        width=270,
        height=270
    )
    pokemon_imagen_shiny = ft.Image(
        src="background.png",
        width=270,
        height=270
    )
    shiny = ft.Text("Imagen Shiny: ", size=28)
    pokemon_nombre = ft.Text(size=20)
    pokemon_numero = ft.Text(size=14)
    pokemon_tipos = ft.Text(size=18)
    pokemon_estado = ft.Text(value="", size=20, visible=False)

    def btn_click(e):
        api_url_pokemon=f'https://pokeapi.co/api/v2/pokemon/{nombre.value}'
        result = requests.get(api_url_pokemon)
        if result.status_code == 200:
            nonlocal buffer  # Referencia al buffer definido fuera de la función
        api_url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{nombre.value}'
        result = requests.get(api_url_pokemon)
        if result.status_code == 200:
            pokemon_data = result.json()
            try:
                # Imagen normal
                buffer.seek(0)  # Reinicia el buffer
                with urlopen(pokemon_data['sprites']['other']['official-artwork']['front_default']) as response:
                    buffer.write(response.read())
                buffer.seek(0)
                im = Image.open(buffer)
                pokemon_imagen.src_base64 = base64.b64encode(buffer.getvalue()).decode()

                # Imagen Shiny
                buffer.seek(0)  # Reinicia el buffer
                with urlopen(pokemon_data['sprites']['other']['official-artwork']['front_shiny']) as response:
                    buffer.write(response.read())
                buffer.seek(0)
                im = Image.open(buffer)
                pokemon_imagen_shiny.src_base64 = base64.b64encode(buffer.getvalue()).decode()

                # Procesa el numero de pokedex
                pokemon_numero.value = f'Nº: ' + str(pokemon_data['id'])
                pokemon_numero.update()
                # Procesa el nombre del Pokemon
                pokemon_nombre.value = f'Nombre: ' + pokemon_data['name'].capitalize()
                pokemon_nombre.update()
                # Procesa los tipos del Pokemon

                tipos_urls = [tipo['type']['url'] for tipo in pokemon_data['types']]
            
                tipos_en_español = []
                
                # Para cada URL de tipo, obtén el nombre en español
                for url in tipos_urls:
                    result_tipo = requests.get(url)
                    if result_tipo.status_code == 200:
                        tipo_data = result_tipo.json()
                        # Busca el nombre en español en los nombres localizados
                        for nom in tipo_data['names']:
                            if nom['language']['name'] == 'es':
                                tipos_en_español.append(nom['name'].capitalize())
                                break
                
                # Actualiza el widget de los tipos con los nombres en español
                pokemon_tipos.value = f'Tipos: {", ".join(tipos_en_español)}'
                pokemon_tipos.update()

                pokemon_estado.visible = False
                pokemon_estado.update()
            except Exception as ex:
                print(f"Error al procesar la imagen: {ex}")
        else:
            pokemon_nombre.value=""
            pokemon_tipos.value = ""
            pokemon_numero.value = ""
            pokemon_imagen.src_base64 = ""
            pokemon_imagen_shiny.src_base64 = ""
            shiny.value = ""

            # Actualiza el widget de estado con el mensaje y hazlo visible
            pokemon_estado.value = "Pokémon no encontrado"
            pokemon_estado.visible = True
            pokemon_estado.update()

        page.update()

    submit.on_click = btn_click

    row_contenedor = ft.Row(
        controls=[
            pokemon_imagen,
            ft.Column(controls=[pokemon_nombre, pokemon_numero, pokemon_tipos])
        ],
        alignment="start"  # Ajusta la alineación si es necesario
    )

    row_contenedor_2 = ft.Row(
        controls=[
            shiny,
            pokemon_imagen_shiny
        ],
        alignment="start"  # Ajusta la alineación si es necesario
    )

    contenedor = ft.Column(
        controls=[logo_pokedex, nombre, submit, pokemon_estado, row_contenedor, row_contenedor_2],
        expand=1
    )

    page.add(contenedor)

ft.app(target=main)