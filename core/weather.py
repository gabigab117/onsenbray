"""Récupération de la météo actuelle d'Ons-en-Bray via l'API OpenWeather.

L'appel se fait côté serveur (la clé API ne doit jamais être exposée au
navigateur) et le résultat est mis en cache pour éviter de solliciter l'API à
chaque visite. En cas d'erreur (réseau, clé manquante/invalide, réponse
inattendue), la fonction renvoie ``None`` afin que la page reste fonctionnelle.
"""

import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Coordonnées d'Ons-en-Bray (Oise, Hauts-de-France).
LATITUDE = 49.41649618664718
LONGITUDE = 1.9221876337153907

CACHE_KEY = "weather:ons-en-bray"
CACHE_TIMEOUT = 1800  # 30 minutes
API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather():
    """Renvoie la météo actuelle (dict simplifié) ou ``None`` en cas d'échec.

    Format renvoyé::

        {"temp": 18, "description": "Ciel dégagé", "icon": "01d", "city": "Ons-en-Bray"}
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if not api_key:
        logger.warning("OPENWEATHER_API_KEY non configurée : météo indisponible.")
        return None

    try:
        response = requests.get(
            API_URL,
            params={
                "lat": LATITUDE,
                "lon": LONGITUDE,
                "units": "metric",
                "lang": "fr",
                "appid": api_key,
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        weather = {
            "temp": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"],
            "city": "Ons-en-Bray",
        }
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        logger.warning("Échec de récupération de la météo OpenWeather : %s", exc)
        return None

    cache.set(CACHE_KEY, weather, CACHE_TIMEOUT)
    return weather
