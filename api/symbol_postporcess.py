import re
import os
import time
import sys
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import SYMBOL_TO_WORD


def symbol_transfor(sentence):
    """    
    Correct the words in the sentence. Perform correction based on the command dictionary and closest matches.  
      
    :param  
    ----------  
    sentence: str  
        The sentence to be corrected  
      
    :rtype  
    ----------  
    corrected_sentence: str  
        The corrected sentence  
    """  

    transfored_sentence = []
    translate_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  
    sentence = sentence.translate(translate_table)  
    sentence = sentence.lower()
    for word in sentence.split():
        if word in SYMBOL_TO_WORD:
            transfored_sentence.append(str(SYMBOL_TO_WORD[word]))
        else:
            transfored_sentence.append(word)

    return " ".join(transfored_sentence)
    

if __name__ == "__main__":
    import time

    # 測試
    sentence = "Tiger I Angel I-V"
    start = time.time()
    corrected = symbol_transfor(sentence)
    end = time.time()
    print("Original text: ", sentence)
    print("Corrected text: ", corrected)
    print("spent time:", end - start)
    