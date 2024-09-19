import difflib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import COMMAND_DICTIONARY, CASE1, CASE2, CONVERSION_CASE

def choose_case(pre_word, word):
    """    
    Choose the appropriate conversion case. Determine the form of the current word based on the previous word.  
      
    :param  
    ----------  
    pre_word: str  
        The previous word  
    word: str  
        The current word  
      
    :rtype  
    ----------  
    word: str  
        The converted word  
    """ 

    index = CONVERSION_CASE.index(word)  
    if pre_word in CASE1 and index%2 == 0:
        word = CONVERSION_CASE[index+1]
    if pre_word in CASE2 and index%2 == 1:
        word = CONVERSION_CASE[index-1]

    return word
    
def check_specal_case(sentence):
    """    
    Handle special cases in the sentence. Choose the appropriate word form based on the context.  
      
    :param  
    ----------  
    sentence: list  
        The sentence to be processed, split by words  
      
    :rtype  
    ----------  
    corrected_sentence: list  
        The processed sentence, split by words  
    """  

    corrected_sentence = []
    for index, word in enumerate(sentence):
        if word in CONVERSION_CASE and index-1 >= 0:
            word = choose_case(sentence[index-1], word)
        corrected_sentence.append(word)

    return corrected_sentence

def correct_sentence(sentence):
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

    corrected_sentence = []
    for word in sentence.split():
        if word in COMMAND_DICTIONARY:
            corrected_sentence.append(word)
        else:
            closest_word = difflib.get_close_matches(word, COMMAND_DICTIONARY, n=1, cutoff=0.6)
            if closest_word:
                corrected_sentence.append(closest_word[0])
            else:
                corrected_sentence.append(word)

    corrected_sentence = check_specal_case(corrected_sentence)

    return " ".join(corrected_sentence)

if __name__ == "__main__":
    import time

    # 測試
    sentence = "Tiger"
    start = time.time()
    corrected = correct_sentence(sentence)
    end = time.time()
    print("Original text: ", sentence)
    print("Corrected text: ", corrected)
    print("spent time:", end - start)
    
