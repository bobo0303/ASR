#
import difflib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import COMMAD_DICTIONARY

def correct_sentence(sentence):
    corrected_sentence = []
    for word in sentence.split():
        if word in COMMAD_DICTIONARY:
            corrected_sentence.append(word)
        else:
            closest_word = difflib.get_close_matches(word, COMMAD_DICTIONARY, n=1, cutoff=0.8)
            if closest_word:
                corrected_sentence.append(closest_word[0])
                similarity = difflib.SequenceMatcher(None, word, closest_word[0]).ratio()
                print(closest_word[0], similarity)
            else:
                corrected_sentence.append(word)
                
    return " ".join(corrected_sentence)


if __name__ == "__main__":
    #################################
    #基本從資料庫轉換的方法已經做好，但還要去針對 "to" "for" 去做保護以免被錯誤轉換
    #################################
    import time
    # 測試
    sentence = "The plane is cleared for landling."
    start = time.time()
    corrected = correct_sentence(sentence)
    end = time.time()
    print("Original text: ", sentence)
    print("Corrected text: ", corrected)
    print("spent time:", end - start)
    
