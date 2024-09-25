from pydantic import BaseModel
import torch

#############################################################################

class ModlePath(BaseModel):
    large_v2: str = "models/large-v2.pt"
    medium: str = "models/medium.en.pt"

#############################################################################
""" options for Whisper inference """
OPTIONS = {
    "fp16": torch.cuda.is_available(),
    "language": "en",
    "task": "transcribe",
    "initial_prompt": """
                      tree, niner, two, tiger, viper, scramble, holding hands, engage, mission complete, initial five, wedge, go cover, in, off, cleared to land, angel, heading, cleared for takeoff, go around
                      """,
    "logprob_threshold": -1.0,
    "no_speech_threshold": 0.2,
}

#############################################################################
""" 示例 ATC 熱詞列表 """
ACTION_HOTWORDS = [
    "Scramble", "Holding Hands", "Engage", "Engaged", "Mission Complete", "Initial Five",
    "Go Cover", "Cleared for Takeoff", "Cleared for Take off", "Cleared to Land", "Go Around", "IN", "OFF",
    "Angel", "Heading",
]

AI_MACHINE_HOTWORDS = ['Viber', 'Viper', 'Tiger']

AI_MACHINE_NUMBER_HOTWORDS = ['one', 'two', 'tree', 'three', 'four']

NUMBER_HOTWORDS = ['zero', 'one', 'two', 'tree', 'three', 'four', 'five',
                   'six', 'seven', 'eight', 'nine', 'niner', 'thousand']

#############################################################################
""" 定義 AI 機器與動作的編碼 """
AI_MACHINES = {
    "tiger one": 1, "tiger two": 2, "tiger tree": 3, "tiger three": 3, "tiger four": 4,
    "viper one": 5, "viper two": 6, "viper tree": 7, "viper three": 7, "viper four": 8,
    "viber one": 5, "viber two": 6, "viber tree": 7, "viber three": 7, "viber four": 8
}

ACTIONS = {
    "scramble": 1, "holding hands": 2, "engage": 3, "engaged": 3, "mission complete": 4,
    "initial five": 5, "go cover": 6, "in": 7, "off": 8, "cleared for takeoff": 9, "cleared for take off": 9,
    "cleared to land": 10, "go around": 11, "heading": 12, "angel": 13, "angle": 13
}

#############################################################################
""" 數字文字轉換 """
DIGIT_TO_WORD = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
}

WORD_TO_DIGIT = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'tree': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'niner': '9'
}

SPOKEN_PATTERNS = {
    'thousand': '000',
    }

NUMBER_PATTERNS = {
    '000': 'thousand',
}

#############################################################################

HALLUCINATION_THRESHOLD = 60

#############################################################################
""" command  """
COMMAND_DICTIONARY = [
    "scramble", "holding", "hands", "engage", "mission", "complete", "initial", "wedge", \
    "tiger", "viper", \
    "go", "cover", "in", "off", "cleared", "to", "land", "for", "takeoff", "take", "around", \
    "angel", "heading", \
    "two", "four", "nine", "niner", "thousand",
    # "zero", "one", "two", "three", "tree", "four", "five", "six", "seven", "eight", "nine", "niner",
]

""" special case """
# to > two, for > four
CASE1 = ["tiger", "viper"]
# two > to, four > for
CASE2 = ["cleared"]
# the case we need to convert
CONVERSION_CASE = ["to", "two", "for", "four"]

#############################################################################