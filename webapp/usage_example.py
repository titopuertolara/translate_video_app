import requests
import json

video_name='/home/andres/Videos/Databricks Fundamentals/Supported Workloads and the Data INtelligence Engine/Orchestration-2024-05-23_11.02.06.mkv'

data = {
    "srclang": "en",
    "dstlang": "es",
    "filename":video_name
}

print(data)


resp=requests.post('http://localhost:5000/translate',json=data)

print(resp.json())
