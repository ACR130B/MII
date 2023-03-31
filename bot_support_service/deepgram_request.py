from deepgram import Deepgram
import asyncio
import json

DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'
FILE = 'YOUR_FILE_LOCATION'
MIMETYPE = 'audio/wav'


async def main(audio_name):
    global FILE

    FILE = audio_name

    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(FILE, 'rb') as audio:
    # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
    print(json.dumps(response, indent=4))

    return response["results"]["channels"][0]["alternatives"][0]["transcript"]