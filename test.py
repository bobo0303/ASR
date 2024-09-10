import requests

# 設定 API 端點 URL
url = "http://0.0.0.0:5176/transcribe"  # 這裡修改成你的 FastAPI 服務的 URL

# 讀取要傳輸的音頻檔案（二進制格式）
with open("whisper_API/test_audio/test.wav", "rb") as f:
    audio_binary_file = f.read()

    files = {"file": ("test.wav", audio_binary_file)}

    # 發送 POST 請求到 API 端點
    response = requests.post(url, files=files)

    # 解析回應
    if response.status_code == 200:
        command_number = response.text
        print(f"Command number: {command_number}")
    else:
        print(f"Error: {response.text}")
