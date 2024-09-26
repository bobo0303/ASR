# Whisper  
  
[Whisper](https://github.com/openai/whisper/tree/main) 是 OpenAI 提供的一個語音辨識模型。以下是可用模型的下載連結。  
  
## 模型下载  
  
| 模型名稱      | 下載位置                                                                                                                             | 模型名稱      | 下載位置                                                                                                                             |  
|---------------|--------------------------------------------------------------------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------|  
| `tiny.en`     | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt)     | `small.en`    | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872/small.en.pt)    |  
| `tiny`        | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt)        | `small`       | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt)       |  
| `base.en`     | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt)     | `medium.en`   | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt)   |  
| `base`        | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt)        | `medium`      | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt)      |  
| `large-v1`    | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt)    | `large-v2`    | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt)    |  
| `large-v3`    | [下載位置](https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c    |  
  
## 建 Images 
  
```python 3.8.10
git clone https://github.com/bobo0303/ASR.git
cd ./ASR_main
docker build -t whisper_api:lastest .
```

## 起 container 
  
```excample on teller VM  
docker run -d -it --gpus all --shm-size 32G --runtime nvidia --device=/dev/nvidia-uvm --device=/dev/nvidia-uvm-tools --device=/dev/nvidiactl --device=/dev/nvidia0 --name whisper_api --network host -v /data/bobo/whisper_API:/mnt whisper_api:lastest bash
```

## 目錄結構  

```
├── Dockerfile
├── init.py
├── api
│   ├── init.py
│   ├── model.py
│   ├── word_split_postprocess.py
│   ├── typos_postprocess.py
│   └── text_postprocess.py
├── app.yml
├── audio
│   └── test.wav
├── lib
│   ├── init.py
│   ├── base_object.py
│   ├── constant.py
│   ├── data_object.py
│   └── whisper
├── logging.conf
├── logs
│   └── sys.log
├── main.py
├── models
│   ├── large-v2.pt
│   └── medium.en.pt
├── requirements.txt
└── whl
    └── wjy3-1.7.1-py3-none-any.whl
```
