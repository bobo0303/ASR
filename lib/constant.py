from pydantic import BaseModel
import torch

class ModlePath(BaseModel):
    large_v2: str = "models/large-v2.pt"
    medium: str = "models/medium.en.pt"

# options for Whisper inference
OPTIONS = {
    "fp16": torch.cuda.is_available(),
    "language": "en",
    "task": "transcribe",
    "initial_prompt": """
                      two , off, tiger, viper, Scramble, Holding Hands, fluid four, Engaged, Mission Complete, Initial Five, wedge, Go Cover, IN, OFF, Cleared to Land, Angle and Heading, Cleared for Takeoff, Go Around.
                      """,
}