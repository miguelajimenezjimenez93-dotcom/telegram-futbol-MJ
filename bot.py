
import os
import time
import requests
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

headers = {
    'x-apisports-key': API_KEY
}

# Equipos a seguir
equipos = {
    541: "Real Madrid",
    529: "Barcelona",
    543: "Betis",
    530: "Atlético Madrid"
}

avisados = set()

def enviar_mensaje(texto):
    bot.send_message(chat_id=CHAT_ID, text=texto)

def comprobar_bajas():
    for team_id, nombre in equipos.items():

        url = f"https://v3.football.api-sports.io/injuries?team={team_id}&season=2025"

        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()

        for item in data.get("response", []):

            jugador = item["player"]["name"]
            razon = item["player"]["reason"]

            clave = f"{jugador}-{razon}"

            if clave not in avisados:

                mensaje = f"""
🚨 BAJA DETECTADA

🏟 Equipo: {nombre}
❌ Jugador: {jugador}
📋 Motivo: {razon}
"""

                enviar_mensaje(mensaje)

                avisados.add(clave)

if __name__ == "__main__":

    enviar_mensaje("✅ Bot de alertas iniciado correctamente")

    while True:
        try:
            comprobar_bajas()
        except Exception as e:
            print(e)

        time.sleep(300)
