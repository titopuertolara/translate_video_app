from flask import Flask, jsonify, request,send_file
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
        videofile=request.files['video']
        video_lang=json.loads(request.form['json_data'])
        
        
        videofile.save(videofile.filename)
        time.sleep(0.5)        
        video_tool=video_processor(videofile.filename,model)
        video_tool.extract_audio()
        video_tool.transcribe_audio()
        video_tool.translate_text(src_lang=video_lang['srclang'],dst_lang=video_lang['dstlang'])
        video_tool.create_srt()
        video_tool.merge_subtitles()
        name=video_tool.name+'_with_subtitles.mp4'

        



    return send_file(name)

if __name__=='__main__':
    app.run()