# model.py
import whisper
import torch
import sys
import os
import time

from .text_postprocess import process_transcription, encode_command
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import ModlePath, OPTIONS


class Model:
    def __init__(self):
        self.model = None
        self.models_path = ModlePath()

    def load_model(self, models_name):
        # 實現模型載入的邏輯
        start = time.time()
        if models_name in ["large_v2"]:
            self.model = whisper.load_model(self.models_path.large_v2)
        elif models_name == "medium":
            self.model = whisper.load_model(self.models_path.medium)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)
        end = time.time()
        print(f"=== Model '{models_name}' loaded in {end - start:.2f} secomds.")

    def transcribe(self, audio_file_path):
        # 實現推論的邏輯
        start = time.time()
        result = self.model.transcribe(audio_file_path, **OPTIONS)
        ori_pred = result['text']
        hotword, pred = process_transcription(ori_pred)
        command_number = encode_command(hotword)
        end = time.time()
        inference_time = end-start


        return {"hotword": hotword, "transcription": pred, "command number": command_number}, inference_time
