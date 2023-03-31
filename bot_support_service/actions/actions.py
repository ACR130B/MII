from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import asyncio
from pydub import AudioSegment

import deepgram_request as dr
import speech_recognition as sr


def convert_audio(audio, sample_rate=16000):
    final_name = audio[:-4] + ".wav"

    if audio.endswith(".mp3"):
        sound = AudioSegment.from_mp3(audio)
    elif audio.endswith(".ogg"):
        sound = AudioSegment.from_ogg(audio)
    elif audio.endswith(".wav"):
        sound = AudioSegment.from_wav(audio)
    sound_w_new_fs = sound.set_frame_rate(sample_rate).set_channels(1).set_sample_width(2)
    sound_w_new_fs.export(final_name, format="wav")

    return final_name


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_convert_vm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file_name = tracker.get_slot('file_name')
        file_path = 'audio/' + file_name + '.ogg'
        new_file_path = convert_audio(file_path)
        r = sr.Recognizer()
        with sr.AudioFile(new_file_path) as source:
            audio_data = r.record(source)
            audio_text = r.recognize_google(audio_data, language='ru-RU')
        dispatcher.utter_message(text=audio_text)

        return []
