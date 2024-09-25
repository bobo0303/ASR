from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import time
import logging  
import uvicorn
import datetime
import schedule  
from threading import Thread  

from api.model import Model
from lib.data_object import LoadModelRequest
from lib.base_object import BaseResponse
from lib.constant import HALLUCINATION_THRESHOLD

#############################################################################
if not os.path.exists("./audio"):  
    os.mkdir("./audio") 

# 配置日志记录  
log_format = "%(asctime)s - %(message)s"  # 输出时间戳和消息内容  
logging.basicConfig(level=logging.INFO, format=log_format)  # ['DEBUG', 'INFO']
logger = logging.getLogger(__name__)

app = FastAPI()
model = Model()

@app.get("/")
def HelloWorld():
    return {"Hello": "World"}
##############################################################################


# load the default model at startup
@app.on_event("startup")
async def load_default_model_preheat():
    """  The process of loading the default model and preheating on startup  

    :param  
        ----------  
        None: The function does not take any parameters  
    :rtype  
        ----------  
        None: The function does not return any value  
    :logs  
        ----------  
        Loading and preheating status and times  
    """ 

    logger.info("#####################################################")
    logger.info(f"Start to loading default model.")

    # load model
    default_model = "large_v2"
    model.load_model(default_model)  # 直接加載默認模型
    logger.info(f"Default model {default_model} has been loaded successfully.")

    # preheat
    logger.info(f"Start to preheat model.")
    default_audio = "audio/test.wav"
    start = time.time()
    for _ in range(5):
        model.transcribe(default_audio)
    end = time.time()

    logger.info(f"Preheat model has been completed in {end - start:.2f} seconds.")
    logger.info("#####################################################")


# load model endpoint
@app.post("/load_model")
async def load_model(request: LoadModelRequest):
    """  The process of loading a specified model  

    :param  
        ----------  
        request: LoadModelRequest  
            The request object containing the model's name to be loaded  
    :rtype  
        ----------  
        BaseResponse:  
            A response indicating the success or failure of the model loading process  
    """ 
 
    models_name = request.models_name.lower()
    if models_name not in dir(model.models_path):
        raise HTTPException(status_code=400, default="Model not found")

    model.load_model(request.models_name)
    return BaseResponse(message="Model "+request.models_name+" has been loaded successfully.")

# inference endpoint
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """  The process of transcribing an audio file  

    :param  
        ----------  
        file: UploadFile  
            The audio file to be transcribed  
    :rtype  
        ----------  
        BaseResponse:   
            A response containing the transcription results  
    """ 
    
    # Get the file name  
    file_name = file.filename  
    logger.info(f"requist ID name {file_name}.")

    start = time.time()
    default_result = {"ai_code": -1, "action_code": -1, "numbers": -1}
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    audio_buffer = f"audio/output_{timestamp}.wav"

    with open(audio_buffer, 'wb') as f:
        f.write(file.file.read())

    if not os.path.exists(audio_buffer):
        logger.info("The audio file does not exist, please check the audio path.")
        return BaseResponse(message={"inference failed!"}, data=default_result)
    end = time.time()
    save_audio = end-start

    start = time.time()
    result, inference_time = model.transcribe(audio_buffer)
    logger.info(f"inference has been completed in {inference_time:.2f} seconds.")
    logger.info(f"transcription: {result['transcription']}\n=== hotword: {result['hotword']}\n=== command number: {result['command number']}")  
    end = time.time()
    total_inference_time = end-start
    
    start = time.time()
    if os.path.exists(audio_buffer):
        os.remove(audio_buffer)
    end = time.time()
    remove_audio_time = end-start

    if len(result['transcription']) >= HALLUCINATION_THRESHOLD:
        return BaseResponse(message="out of hallucination threshold, please try again", data=default_result)

    logger.debug(f"save_audio: {save_audio} seconds, total_inference_time: {total_inference_time}, remove_audio_time: {remove_audio_time}.")

    output_message = f"transcription: {result['transcription']} | hotword: ai_code: {result['hotword']['ai_code']}, action_code: {result['hotword']['action_code']},  numbers: {result['hotword']['numbers']}"
    return BaseResponse(message=output_message, data=result['command number'])

# 清理音频文件  
def delete_old_audio_files():  
    """  The process of deleting old audio files  

    :param  
        ----------  
        None: The function does not take any parameters  
    :rtype  
        ----------  
        None: The function does not return any value  
    :logs  
        ----------  
        Deleted old files  
    """ 
 
    current_time = time.time()  
    audio_dir = "./audio" 
    for filename in os.listdir(audio_dir):  
        if filename == "test.wav":  # 跳过特定文件  
            continue    
        file_path = os.path.join(audio_dir, filename)  
        if os.path.isfile(file_path): 

            file_creation_time = os.path.getctime(file_path)  
            # 删除超过一天的文件  
            if current_time - file_creation_time > 24 * 60 * 60:  
                os.remove(file_path)  
                logger.info(f"Deleted old file: {file_path}")  
  
# 每日任务调度  
def schedule_daily_task():  
    schedule.every().day.at("00:00").do(delete_old_audio_files)  
    while True:  
        schedule.run_pending()  
        time.sleep(60)  
  
# 启动每日任务调度  
Thread(target=schedule_daily_task).start()  

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    uvicorn.config.LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.config.LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run(app, log_level='info', host='0.0.0.0', port=port)
 