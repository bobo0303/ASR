from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import os
import time
import uvicorn
import datetime
# from wjy3 import BaseResponse

from api.model import Model
from lib.data_object import LoadModelRequest

#############################################################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
model = Model()


@app.get("/docs2", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    For local js, css swagger in AUO
    :return:
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
##############################################################################


@app.get("/")
def HelloWorld():
    return {"Hello": "World"}


# load the default model at startup
@app.on_event("startup")
async def load_default_model_preheat():
    print(f"=== Start to loading default model.")
    # load model
    default_model = "large_v2"
    model.load_model(default_model)  # 直接加載默認模型
    print(f"=== Default model {default_model} has been loaded successfully.")
    # preheat
    print(f"=== Start to preheat model.")
    default_audio = "test_audio/test.wav"
    start = time.time()
    for _ in range(5):
        model.transcribe(default_audio)
    end = time.time()
    print(f"=== Preheat model has been completed in {end - start:.2f} seconds.")


# load model endpoint
@app.post("/load_model")
async def load_model(request: LoadModelRequest):
    models_name = request.models_name.lower()
    if models_name not in dir(model.models_path):
        raise HTTPException(status_code=400, default="Model not found")

    model.load_model(request.models_name)
    # return BaseResponse(message={f"=== Model '{request.models_name}' has been loaded successfully."})
    return {f"=== Model '{request.models_name}' has been loaded successfully."}

# inference endpoint
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    audio_buffer = f"audio_buffer/output_{timestamp}.wav"
    with open(audio_buffer, 'wb') as f:
        f.write(file.file.read())

    if not os.path.exists(audio_buffer):
        print("=== The audio file does not exist, please check the audio path.")
        return {"command number": (-1, -1, -1)}

    result, inference_time = model.transcribe(audio_buffer)
    print(f"=== inference has been completed in {inference_time:.2f} seconds.")
    print("=== transcription: ", result['transcription'], "\n=== hotword: ", result['hotword'], "\n=== command number: ", result['command number'])

    if os.path.exists(audio_buffer):
        os.remove(audio_buffer)

    return result['command number']

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5176))
    uvicorn.config.LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.config.LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run(app, log_level='info', host='0.0.0.0', port=port)
