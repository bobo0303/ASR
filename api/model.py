# model.py
import os
import sys
import time
import torch
import logging  

from .text_postprocess import process_transcription, hotword_extract, encode_command
from .types_postprocess import correct_sentence
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import ModlePath, OPTIONS
import lib.whisper as whisper

logger = logging.getLogger(__name__)  

class Model:
    def __init__(self):
        """  
        Initialize the Model class with default attributes.  
        """  

        self.model = None
        self.models_path = ModlePath()

    def load_model(self, models_name):
        """  Load the specified model based on the model's name.  
          
        :param  
            ----------  
            models_name: str  
                The name of the model to be loaded.  
          
        :rtype  
            ----------  
            None: The function does not return any value.  
          
        :logs  
            ----------  
            Loading status and time.  
        """

        # 實現模型載入的邏輯
        start = time.time()
        if models_name == "large_v2":
            self.model = whisper.load_model(self.models_path.large_v2)
        elif models_name == "medium":
            self.model = whisper.load_model(self.models_path.medium)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)
        end = time.time()
        logger.info(f"Model '{models_name}' loaded in {end - start:.2f} secomds.")

    def transcribe(self, audio_file_path):
        """  Perform transcription on the given audio file.  
          
        :param  
            ----------  
            audio_file_path: str  
                The path to the audio file to be transcribed.  
          
        :rtype  
            ----------  
            tuple:   
                A tuple containing a dictionary with hotwords, transcription, command number, and the inference time.  
          
        :logs  
            ----------  
            Inference status and time.  
        """  

        # 實現推論的邏輯
        start = time.time()
        result = self.model.transcribe(audio_file_path, **OPTIONS)
        print(result)
        ori_pred = result['text']
        end = time.time()
        inference_time = end-start
        start = time.time()
        spoken_text = process_transcription(ori_pred)
        corrected_pred = correct_sentence(spoken_text)
        hotword, pred = hotword_extract(corrected_pred)
        command_number = encode_command(hotword)
        end = time.time()
        post_process_time = end-start
        logger.debug(f"inference time {inference_time} secomds.")
        logger.debug(f"post process time {post_process_time} secomds.")

        return {"hotword": hotword, "transcription": pred, "command number": command_number}, inference_time
