import re
import os
import time
import sys
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import (  
    ACTION_HOTWORDS,  
    AI_MACHINE_HOTWORDS,  
    AI_MACHINE_NUMBER_HOTWORDS,  
    NUMBER_HOTWORDS,  
    AI_MACHINES,  
    ACTIONS,  
    DIGIT_TO_WORD,  
    WORD_TO_DIGIT,
    SPOKEN_PATTERNS,
    NUMBER_PATTERNS  
)  

# 去除標點符號並將文本轉換為小寫
def remove_punctuation_and_lowercase(transcription):
    """  Remove punctuation and convert text to lowercase  

    :param  
        ----------  
        transcription: str  
            The input text to be cleaned  
    :rtype  
        ----------  
        str: The cleaned text  
    """

    text = transcription.translate(str.maketrans("", "", string.punctuation))
    text = text.lower()
    return text

# 比對熱詞並返回匹配的關鍵詞
def find_matched_hotwords(text, hotwords):
    """  Find matched hotwords in the text  

    :param  
        ----------  
        text: str  
            The input text to be searched  
        hotwords: list  
            The list of hotwords to match  
    :rtype  
        ----------  
        tuple: The index and matched hotword, or (None, -1) if no match found  
    """ 
 
    text = f" {text} "
    for index, word in enumerate(hotwords):
        if f" {word.lower()} " in text:
            matched_words = word.lower()
            matched_index = text.split().index(matched_words.split()[-1])
            return matched_index, matched_words
    return None, -1

# 比對熱詞並返回匹配的關鍵詞
def find_all_matched_hotwords(text, hotwords):
    """  Find matched hotwords in the text  

    :param  
        ----------  
        text: str  
            The input text to be searched  
        hotwords: list  
            The list of hotwords to match  
    :rtype  
        ----------  
        tuple: The index and matched hotword, or (None, -1) if no match found  
    """ 
    matched_words = []
    matched_index = []
    text = f" {text} "
    for index, word in enumerate(hotwords):
        if f" {word.lower()} " in text:
            matched_words.append(word.lower())
            matched_index.append(text.split().index(word.lower().split()[-1]))
    if matched_words and matched_index:
        min_index = min(enumerate(matched_index), key=lambda x: x[1])[0]  
        word = matched_words[min_index]
        index = matched_index[min_index]
        return word, index
    return None, -1

# 比對熱詞只保留數字並返回關鍵數字
def check_numbers_hotwords(text, hotwords):
    """  Check for number hotwords in the text  

    :param  
        ----------  
        text: list  
            The input text split into words  
        hotwords: list  
            The list of number hotwords to match  
    :rtype  
        ----------  
        list or int: The list of matched number hotwords, or -1 if no match found  
    """ 

    matched_words = []
    for word in text:
        if word in hotwords:
            matched_words.append(word)
    return matched_words if matched_words else -1

# 將數字字符串轉換為口語形式
def mixed_to_spoken(input_string):
    """  Convert mixed alphanumeric string to spoken form  

    :param  
        ----------  
        input_string: str  
            The input alphanumeric string  
    :rtype  
        ----------  
        str: The spoken form of the input string  
    """ 
 
    def number_to_spoken(number_string):
        """  Convert number string to spoken form  

        :param  
            ----------  
            number_string: str  
                The input number string  
        :rtype  
            ----------  
            str: The spoken form of the number string  
        """ 

        for pattern, word in NUMBER_PATTERNS.items():
            if number_string.endswith(pattern):
                num_len = len(number_string)
                if num_len > len(pattern):
                    prefix = number_string[:-len(pattern)]
                    prefix_spoken = ' '.join(DIGIT_TO_WORD[digit] for digit in prefix)
                    return f"{prefix_spoken} {word}"
                else:
                    return word
        return ' '.join(DIGIT_TO_WORD[digit] for digit in number_string)

    def process_alphanumeric_segment(segment):
        """  Process alphanumeric segment  
        
        :param  
            ----------  
            segment: str  
                The input segment  
        :rtype  
            ----------  
            str: The processed segment  
        """


        if segment.isdigit():
            return number_to_spoken(segment)
        else:
            return segment

    parts = re.split(r'(\d+)', input_string)
    spoken_parts = [process_alphanumeric_segment(part) for part in parts if part]
    
    # 用空格分隔部件並去除多餘的空格
    spoken_form = ' '.join(spoken_parts).strip()
    return re.sub(r'\s+', ' ', spoken_form)

# 將字母和數字分開
def separate_alphanumeric(text):
    """  This function separates letters and numbers in the given text.  
      
    :param  
        ----------  
        text: str  
            The input string containing alphanumeric characters.  
      
    :rtype  
        ----------  
        str:   
            The modified string with letters and numbers separated by spaces.  
    """ 
 
    pattern = re.compile(r'([a-zA-Z]+)(\d+)|(\d+)([a-zA-Z]+)')
    separated_text = pattern.sub(r'\1 \2\3 \4', text)
    return separated_text



# 處理轉錄文本，找到熱詞並轉換數字為口語形式
def process_transcription(transcription):
    """   This function processes the transcribed text, identifies hotwords, and converts numbers to spoken form.  
      
    :param  
    ----------  
    transcription: str  
        The transcribed text to be processed.  
      
    :return  
    ----------  
    str:  
        The processed spoken text.  
    """ 

    cleaned_text = remove_punctuation_and_lowercase(transcription)
    separated_text = separate_alphanumeric(cleaned_text)
    spoken_text = mixed_to_spoken(separated_text)

    return spoken_text

def hotword_extract(spoken_text):
    """ This function identifies hotwords from the processed spoken text.  
      
    :param  
    ----------  
    spoken_text: str  
        The processed spoken text from which hotwords are to be identified.  
      
    :return  
    ----------  
    tuple:  
        A tuple containing a dictionary of hotwords and the spoken text.  
    """

    # find AI machine type
    matched_machine_index, matched_machine_hotwords = find_matched_hotwords(spoken_text, AI_MACHINE_HOTWORDS)

    # find AI machine number
    if matched_machine_index is not None and spoken_text:
        if len(spoken_text.split())>matched_machine_index+1:
            ai_machine_number = check_numbers_hotwords([spoken_text.split()[matched_machine_index+1]], AI_MACHINE_NUMBER_HOTWORDS)
            matched_machine_hotwords=f"{matched_machine_hotwords} {' '.join(ai_machine_number)}" if ai_machine_number != -1 else -1
    
    # reshape spoken_text 
    reshaped_spoken_text = ' '.join(spoken_text.split()[matched_machine_index + 1:]) if matched_machine_hotwords != -1 else spoken_text  

    # find action type
    matched_action_index, matched_action_hotwords = find_matched_hotwords(reshaped_spoken_text, ACTION_HOTWORDS)

    # checking the last number
    if matched_action_hotwords in ["angel", "heading"] and reshaped_spoken_text:
        last_data = reshaped_spoken_text.split()[matched_action_index+1:]
        numbers = check_numbers_hotwords(last_data, NUMBER_HOTWORDS)
        numbers = ' '.join(numbers) if numbers != -1 else -1
    else:
        numbers = -1

    hotwords = {
        "ai_code": matched_machine_hotwords,
        "action_code": matched_action_hotwords,
        "numbers": numbers
    }

    return hotwords, spoken_text

def spoken_to_mixed(input_string):
    """  This function converts spoken numbers in the input string to a mixed alphanumeric form.  
      
    :param  
        ----------  
        input_string: str  
            The input string containing spoken numbers.  
      
    :rtype  
        ----------  
        str:   
            The modified string with spoken numbers converted to their numeric forms.  
    """  
        
    def spoken_to_number(spoken_string):
        """  Helper function to convert spoken words to numbers.  
  
        :param  
            ----------  
            spoken_string: str  
                The input string containing spoken numbers.  
          
        :rtype  
            ----------  
            str:  
                The string with spoken numbers converted to numeric form.  
        """ 

        words = spoken_string.split()
        result = []

        for word in words:
            if word in WORD_TO_DIGIT:
                result.append(WORD_TO_DIGIT[word])
            elif word in SPOKEN_PATTERNS:
                result.append(SPOKEN_PATTERNS[word])
            else:
                result.append(word)

        return ''.join(result)

    def process_segment(segment):
        """  Helper function to process segments of the input string.  
  
        :param  
            ----------  
            segment: str  
                A segment of the input string to be processed.  
          
        :rtype  
            ----------  
            str:  
                The processed segment with spoken numbers converted to numeric form if applicable.  
        """     
            

        if all(word in WORD_TO_DIGIT or word in SPOKEN_PATTERNS for word in segment.split()):
            return spoken_to_number(segment)
        else:
            return segment

    parts = re.split(r'(\s+)', input_string)
    mixed_parts = [process_segment(part) for part in parts if part]

    # 合併結果並去除多餘的空格
    mixed_form = ''.join(mixed_parts).strip()
    return re.sub(r'\s+', ' ', mixed_form)

# 編碼函數
def encode_command(hotwords):
    """  This function encodes hotwords into corresponding command IDs.  
      
    :param  
        ----------  
        hotwords: dict  
            A dictionary containing identified hotwords.  
      
    :rtype  
        ----------  
        dict:   
            A dictionary with encoded command IDs.  
    """

    ids = {
        "ai_code": -1,
        "action_code": -1,
        "numbers": -1
    }

    ids['ai_code'] = str(AI_MACHINES.get(hotwords['ai_code'], -1))
    ids['action_code'] = str(ACTIONS.get(hotwords['action_code'], -1))
    ids['numbers'] = str(spoken_to_mixed(hotwords['numbers']) if hotwords['numbers'] != -1 else '-1')
        
    return ids

if __name__ == "__main__":
    # 示例使用

    transcription = "one tiger"
    start = time.time()
    spoken_text = process_transcription(transcription)
    matched_hotwords, spoken_text = hotword_extract(spoken_text)
    command_number = encode_command(matched_hotwords)
    end = time.time()
    print("Matched hotwords:", matched_hotwords)
    print("command number:", (command_number['ai_code'], command_number['action_code'], command_number['numbers']))
    print("Spoken form:", spoken_text)
    print("spent time:", end - start)

