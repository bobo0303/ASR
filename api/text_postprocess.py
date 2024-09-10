import string
import re
import time

# 示例 ATC 熱詞列表
# action_hotwords = [
#     "Scramble", "Holding Hands", "Flow Four", "Engaged",
#     "Mission Complete", "Initial Five", "Gear Check, Full Stop",
#     "Go Cover", "IN", "OFF", "Cleared to Land",
#     "Angle", "Heading",
# ]
action_hotwords = [
    "Scramble", "Holding Hands", "Engage", "Engaged", "Mission Complete", "Initial Five",
    "Go Cover", "Cleared for Takeoff", "Cleared for Take off", "Cleared to Land", "Go Around", "IN", "OFF",
    "Angel", "Heading",
]

# ai_machine_hotwords = ['Alpha', 'Bravo', 'Delta', 'Gamma']
ai_machine_hotwords = ['Viber', 'Viper', 'Tiger']

ai_machine_number_hotwords = ['one', 'two', 'tree', 'three', 'four']

number_hotwords = ['zero', 'one', 'two', 'tree', 'three', 'four', 'five',
                   'six', 'seven', 'eight', 'nine', 'niner', 'thousand']


# 定義 AI 機器與動作的編碼
ai_machines = {
    "tiger one": 1, "tiger two": 2, "tiger tree": 3, "tiger three": 3, "tiger four": 4,
    "viper one": 5, "viper two": 6, "viper tree": 7, "viper four": 8,
    "viber one": 5, "viber two": 6, "viber tree": 7, "viber four": 8
}

actions = {
    "scramble": 1, "holding hands": 2, "engage": 3, "mission complete": 4,
    "initial five": 5, "go cover": 6, "in": 7, "off": 8, "cleared for takeoff": 9, "cleared for take off": 9,
    "cleared to land": 10, "go around": 11, "heading": 12, "angel": 13, "angle": 13
}

# 去除標點符號並將文本轉換為小寫
def remove_punctuation_and_lowercase(transcription):
    text = transcription.translate(str.maketrans("", "", string.punctuation))
    text = text.lower()
    return text

# 比對熱詞並返回匹配的關鍵詞
def find_matched_hotwords(text, hotwords):
    text = f" {text} "
    for index, word in enumerate(hotwords):
        if f" {word.lower()} " in text:
            matched_words = word.lower()
            matched_index = text.split().index(matched_words.split()[-1])
            return matched_index, matched_words
    return None, -1

def check_numbers_hotwords(text, hotwords):
    matched_words = []
    for word in text:
        if word in hotwords:
            matched_words.append(word)
    return matched_words if matched_words else -1

# 將數字字符串轉換為口語形式
def mixed_to_spoken(input_string):
    digit_to_word = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }

    def number_to_spoken(number_string):
        number_patterns = {
            '000': 'thousand',
        }
        for pattern, word in number_patterns.items():
            if number_string.endswith(pattern):
                num_len = len(number_string)
                if num_len > len(pattern):
                    prefix = number_string[:-len(pattern)]
                    prefix_spoken = ' '.join(digit_to_word[digit] for digit in prefix)
                    return f"{prefix_spoken} {word}"
                else:
                    return word
        return ' '.join(digit_to_word[digit] for digit in number_string)

    def process_alphanumeric_segment(segment):
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
    pattern = re.compile(r'([a-zA-Z]+)(\d+)|(\d+)([a-zA-Z]+)')
    separated_text = pattern.sub(r'\1 \2\3 \4', text)
    return separated_text

# 處理轉錄文本，找到熱詞並轉換數字為口語形式
def process_transcription(transcription):
    cleaned_text = remove_punctuation_and_lowercase(transcription)
    separated_text = separate_alphanumeric(cleaned_text)
    spoken_text = mixed_to_spoken(separated_text)

    # find AI machine type
    matched_machine_index, matched_machine_hotwords = find_matched_hotwords(spoken_text, ai_machine_hotwords)

    # find AI machine number
    if matched_machine_index is not None and spoken_text:
        ai_machine_number = check_numbers_hotwords([spoken_text.split()[matched_machine_index+1]], ai_machine_number_hotwords)
        matched_machine_hotwords=f"{matched_machine_hotwords} {' '.join(ai_machine_number)}" if ai_machine_number != -1 else -1

    # find action type
    matched_action_index, matched_action_hotwords = find_matched_hotwords(spoken_text, action_hotwords)

    # number to word

    # checking the last number
    if matched_action_hotwords in ["angel", "heading"] and spoken_text:
        last_data = spoken_text.split()[spoken_text.split().index(matched_action_hotwords)+1:]
        numbers = check_numbers_hotwords(last_data, number_hotwords)
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
    word_to_digit = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'tree': '3', 'four': '4',
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'niner': '9'
    }
    spoken_patterns = {
        'thousand': '000',
    }

    def spoken_to_number(spoken_string):

        words = spoken_string.split()
        result = []

        for word in words:
            if word in word_to_digit:
                result.append(word_to_digit[word])
            elif word in spoken_patterns:
                result.append(spoken_patterns[word])
            else:
                result.append(word)

        return ''.join(result)

    def process_segment(segment):
        if all(word in word_to_digit or word in spoken_patterns for word in segment.split()):
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
    ids = {
        "ai_code": -1,
        "action_code": -1,
        "numbers": -1
    }

    ids['ai_code'] = ai_machines.get(hotwords['ai_code'], -1)
    ids['action_code'] = actions.get(hotwords['action_code'], -1)
    if hotwords['numbers'] != -1:
        ids['numbers'] = int(spoken_to_mixed(hotwords['numbers']))
    return ids

if __name__ == "__main__":
    # 示例使用

    transcription = "tiger1 angel, three000."
    start = time.time()
    matched_hotwords, spoken_text = process_transcription(transcription)
    command_number = encode_command(matched_hotwords)
    end = time.time()
    print("Matched hotwords:", matched_hotwords)
    print("command number:", (command_number['ai code'], command_number['action code'], command_number['numbers']))
    print("Spoken form:", spoken_text)
    print("spent time:", end - start)

