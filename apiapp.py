from flask import Flask, jsonify, request
import os
from tools import video_processor
import whisper



app = Flask(__name__)
model=whisper.load_model("small")

@app.route('/translate',methods=['POST'])
def translate():
    if request.method=='POST':
        videofile=request.files['video']
        print(videofile.filename)
        #videoname=request.json['name']
        videofile.save(videofile.filename)
        #print(videoname)
        video_tool=video_processor(videofile.filename,model)
        video_tool.extract_audio()
        video_tool.transcribe_audio()
        video_tool.translate_text()
        video_tool.create_srt()
        video_tool.merge_subtitles()

        



    return jsonify({'text':'ok'})

if __name__=='__main__':
    app.run()