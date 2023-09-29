from flask import Flask, jsonify, request
#import whisper



app = Flask(__name__)


@app.route('/translate',methods=['POST'])
def predict():
    if request.method=='POST':
        videofile=request.files['video']
        print(videofile)



    return jsonify({'text':'ok'})

if __name__=='__main__':
    app.run()