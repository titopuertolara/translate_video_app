import requests
import json

video_name='/home/andres/whisper/ucompensar.mp4'

data = {
    "srclang": "es",
    "dstlang": "it",
    "filename":video_name
}

print(data)


resp=requests.post('http://localhost:5000/translate',json=data)

print(resp.json())
