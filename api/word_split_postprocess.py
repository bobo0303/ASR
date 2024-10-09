import wordninja  
import os  
import sys  
  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from lib.constant import COMMANDS_GZ  
  
class WordNinja(object):  
    def __init__(self) -> None:  
        self.lm = wordninja.LanguageModel(COMMANDS_GZ)  
  
    def word_split(self, text):  
        """  
        Splits concatenated words into individual words using the  
        param  
        ----------  
        text: str  
            The text to be split into words.  
  
        :rtype  
        ----------  
        str: The text with words separated by spaces.  
        """  
        if text is not None:  
            text = self.lm.split(text)  
            text = ' '.join(word for word in text)  
        return text  
  
if __name__ == "__main__":  
    # 示例使用  
    wordninja_instance = WordNinja()  
    import time  
    text = "scrumble"  
    start = time.time()  
    splited_text = wordninja_instance.word_split(text)  
    end = time.time()  
    print("Splited text:", splited_text)  
    print("end time:", end - start) 