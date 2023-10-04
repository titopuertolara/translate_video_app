from flask import Flask, jsonify, request
import os
from tools import video_processor
import whisper
import json
import time

app = Flask(__name__)
model=whisper.load_model("small")

@app.route('/translate',methods=['POST'])
def translate():
    if request.method=='POST':
        video_params=request.json
               
        video_file_name=video_params['filename']
                
        
        time.sleep(0.5)        
        video_tool=video_processor(video_file_name,model)
        video_tool.extract_audio()
        video_tool.transcribe_audio()
        video_tool.translate_text(src_lang=video_params['srclang'],dst_lang=video_params['dstlang'])
        video_tool.create_srt()
        video_tool.merge_subtitles()
        name=video_tool.name+'_with_subtitles.mp4'


        



    return jsonify({'response':name})

if __name__=='__main__':
    app.run()