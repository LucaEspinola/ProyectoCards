# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user


def getAllImages():
   
    raw_images = transport.getAllImages()
    cards = []
    
    for raw_image in raw_images:
        card = translator.fromRequestIntoCard(raw_image)
        

        if card:
            cards.append(card)
    
    return cards



# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    tarjetas_filtradas = []

    for tarjeta in getAllImages():
        # Verifica si el nombre buscado está contenido en el nombre de la tarjeta
        if name.lower() in tarjeta.name.lower():
            tarjetas_filtradas.append(tarjeta)

    return tarjetas_filtradas

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # Verificar si el tipo del Pokémon coincide con el tipo recibido por parámetro
        if hasattr(card, 'types') and type_filter in card.types:
            # Si coincide, añadirlo al listado de filtered_cards
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)