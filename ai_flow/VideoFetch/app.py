from flask import Flask, request, jsonify
import os
import logging
import re

from yt_dlp import YoutubeDL

app = Flask(__name__)

SAVE_PATH = "./save"


def download(link, save_path, key):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_path, f'{key}.mp3'),
            'noplaylist': True,  # S'assure de ne pas traiter les playlists
            'cookiefile': '/Users/apple/Documents/pythonPro/aivideo/ai_flow/VideoFetch/cookies.txt'
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Extraire les informations sans télécharger
            info_dict = ydl.extract_info(link, download=False)
            duration = info_dict.get('duration', 0)  # Durée en secondes

            # Vérifier si la durée est supérieure à 20 minutes (1200 secondes)
            if duration > 3600:
                return None

            # Si la durée est acceptable, télécharger
            ydl.download([link])
            video_title = info_dict.get('title', None)

        print("Download is completed successfully")
        return video_title
    except Exception as e:
        logging.error("An error occurred while downloading the audio: %s", e)
        return None


def validator_url(url):
    if not url or url.isspace():
        return False

    youtube_pattern = re.compile(r'^(http|https)://(www\.)?youtube\.com/watch\?v=|^(http|https)://youtu\.be/')
    if not youtube_pattern.match(url):
        return False

    return True

if __name__ == '__main__':
    title = download("https://www.youtube.com/watch?v=3M1QBzdpu4Y&list=PLmJkIjmo8j6SetIJSQIbwWqkrCXpA7MfV", "file", "key")
