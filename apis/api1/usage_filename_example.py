import requests
import json

video_name='/home/andres/whisper/ucompensar.mp4'

data = {
    'srclang': 'es',
    'dstlang': 'de'
}

# Define the file(s) to upload
files={'video':open(video_name,'rb')}



# Combine the JSON data and files in a single dictionary
payload = {'json_data': (None,json.dumps(data), 'application/json')}
payload.update(files)

resp=requests.post('http://localhost:5000/translate',files=payload)
with open('translated_video.mp4','wb') as videofile:
    videofile.write(resp.content)

