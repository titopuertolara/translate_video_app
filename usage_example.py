import requests
import json

video_name='/home/andres/whisper/Uma memória do Futuro-20230816_180222-Meeting Recording_cut.mp4'

data = {
    'srclang': 'pt',
    'dstlang': 'es'
}

# Define the file(s) to upload
files={'video':open(video_name,'rb')}



# Combine the JSON data and files in a single dictionary
payload = {'json_data': (None,json.dumps(data), 'application/json')}
payload.update(files)

resp=requests.post('http://localhost:5000/translate',files=payload)

print(resp.json())
