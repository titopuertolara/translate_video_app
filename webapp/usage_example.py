import requests
import json

video_name='/home/andres/whisper/videos_tin/breathe.mp4'

data = {
    "srclang": "pt",
    "dstlang": "es",
    "filename":video_name
}

print(data)


resp=requests.post('http://localhost:5000/translate',json=data)

print(resp.json())
