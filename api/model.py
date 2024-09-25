# model.py
import os
import sys
import time
import torch
import logging  

from .text_postprocess import process_transcription, hotword_extract, encode_command
from .typos_postprocess import correct_sentence
from .word_split_postprocess import WordNinja
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import ModlePath, OPTIONS
import whisper

logger = logging.getLogger(__name__)  
CSV_EXPERIMENT = False


class Model:
    def __init__(self):
        """  
        Initialize the Model class with default attributes.  
        """  

        self.model = None
        self.models_path = ModlePath()
        self.wordninja_instance = WordNinja()  

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
        logger.debug(result)
        ori_pred = result['text']
        end = time.time()
        inference_time = end-start
        start = time.time()
        # 分詞
        splited_text = self.wordninja_instance.word_split(ori_pred)
        # 小寫、數轉英、分英數黏
        spoken_text = process_transcription(splited_text)
        # 相似字校正
        corrected_pred = correct_sentence(spoken_text)
        # 熱詞查找
        hotword, pred = hotword_extract(corrected_pred)
        # 編碼轉換
        command_number = encode_command(hotword)
        end = time.time()
        post_process_time = end-start
        logger.debug(f"inference time {inference_time} secomds.")
        logger.debug(f"post process time {post_process_time} secomds.")

        if CSV_EXPERIMENT:
            import csv
            csv_file_path = "noise.csv"
            # 打開 CSV 文件進行寫入
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                if result["text"] != '':
                    temperature = result['segments'][0]['temperature']
                    logprob = result['segments'][0]['avg_logprob']
                    no_speech_prob = result['segments'][0]['no_speech_prob']
                    tokens_num = len(result['segments'][0]['tokens'])
                else:
                    temperature = 0
                    logprob = 0
                    no_speech_prob = 0
                    tokens_num = 0
                csv_writer.writerow([ori_pred, temperature, logprob, no_speech_prob, tokens_num])



        return {"hotword": hotword, "transcription": pred, "command number": command_number}, inference_time
