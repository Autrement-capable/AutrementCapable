import subprocess
import os

# Get the absolute path to yt-dlp in the virtual environment
script_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(script_dir, "venv", "bin", "yt-dlp")

# Liste de liens YouTube
youtube_links = [
    "https://www.youtube.com/watch?v=mAmKJMyja34&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=26PKwm1HhgY&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=3XP1XtVGvCs&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=5JquaV9IeX8&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=sQMlEIukhpU&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=IqZOa5twOJM&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=agbIb8eNtrI&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=So33sgmemU4&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=39YqeU_w7FE&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=2haY75ERpQA&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=ZU3PlV3SDgI&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=7QiR2IIQKnY&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=UkI3RaaPSBQ&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=73Sff8gkwmQ&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=FO9KGe563co&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=w0pru_jN17w&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=5O_51G7cbLY&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=WwXiRklkOpM&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=9NVsr_cvzaA&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=duokHoIIP8o&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=5ZCqshy93hg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "http://youtube.com/watch?v=dWsyghFicjc&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=nxlkkHjSadU&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=-jgFIWy5YbM&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=TLYosjkYVMk&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=-pSt8b162cE&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=FT5P1m3vhwg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=6oEJx25_Wsg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=FZZrRHeVLL8&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=5IvO-wRVWfM&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=Vz10adN0nnY&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=7QiR2IIQKnY&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=kswwH-i68UQ&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=tHSZ_ImK1KU&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=dsRUoaFJThk&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=MTC4cQcaytA&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=WmBpkA1NYOg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=ijkqsn-gUiM&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=TgJnZsiekgE&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=0R5_gpfJQNs&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=vD-_h1vLTFg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=JAWeyHo7Atg&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=TO5IVKM8694&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=SIRxYtXa4tI&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=PnAzFPdwRH8&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=MDhtm9lRwJQ&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=Ckrl-fJjDOo&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=Xe1kwXBKdVE&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=Z74Uss_lfS0&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=zwKQl3Oqhag&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=sv8OojAbIrc&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=YgefU82hdjQ&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=OBMh3s8hHTk&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=UztnXQJpzJI&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=iUz-nOuwEWc&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=53fjm0yA60g&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=AdGfuIYFr4I&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=XNRGtANZzrE&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=XNPgpY4yW58&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=NN5owm-WES8&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=KBGDEM3RSZ0&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=QmSUSOATwV0&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw",
    "https://www.youtube.com/watch?v=PQEyZ7lAOhA&list=PLRDA9dHD2F-4jEZs29HcTw3PshdyPj8nw"
]

# Téléchargement des vidéos une par une
for link in youtube_links:
    subprocess.run([
        yt_dlp_path,  # Use the absolute path
        "-f", "best[ext=mp4]/best",  # meilleure qualité disponible en mp4
        "-o", "%(title)s.%(ext)s",   # nom du fichier : titre de la vidéo
        "--no-playlist",  # Skip playlist, just download the video
        link
    ])