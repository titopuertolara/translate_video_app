import requests
import json

video_name='/home/andres/whisper/wetransfer_uma-memoria-do-futuro-20240228_171104-meeting-recording-mp4_2024-04-24_2146/Uma memória do futuro-20240320_175705-Meeting Recording.mp4'

data = {
    "srclang": "pt",
    "dstlang": "es",
    "filename":video_name
}

print(data)


resp=requests.post('http://localhost:5000/translate',json=data)

print(resp.json())
