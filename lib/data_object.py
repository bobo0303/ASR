from pydantic import BaseModel

# Request body model for loading a model
class LoadModelRequest(BaseModel):
    models_name: str

