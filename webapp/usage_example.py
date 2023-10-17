import requests
import json

video_name='/home/andres/whisper/videos_tin/Uma memória do Futuro-20230906_180342-Meeting Recording_EDIT.mp4'

data = {
    "srclang": "pt",
    "dstlang": "es",
    "filename":video_name
}

print(data)


resp=requests.post('http://localhost:5000/translate',json=data)

print(resp.json())
