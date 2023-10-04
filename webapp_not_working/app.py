from dash import Dash,dcc,html,Input,Output,callback,State,ctx
import os
import base64
import dash_player
import time
import requests
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server=app.server

app.layout=html.Div([

    dcc.Upload(id='uploader',children=['Drag and drop'],style={'width':'50%','borderStyle':'dashed'}),
    html.Div(id='output-div'),
        
    html.Div(id='video-container'),
    
    html.Div(id='translate-container-btn',children=[html.Button('translate',id='translate-button',n_clicks=0)]),
    
    html.Div(id='video-translated'),
    dcc.Store(id='filename-temp')
    
   

])

@app.callback(Output('output-div','children'),
              Output('video-container','children'),
              #Output('translate-container-btn','children'),
              Output('filename-temp','data'),

             [Input('uploader','contents'),
             Input('uploader','filename')],prevent_initial_call=False)
def process_video_content(contents,filename):
    if contents is not None:
        try:
            video_path=f'assets/uploads/{filename}'
            with open(video_path,'wb') as videofile:
                videofile.write(base64.b64decode(contents.split(',')[1]))
            
            #video_embedded=dash_player.DashPlayer(id='video-player',url=video_path,controls=True)
            video_embedded=html.Video(id='video-player',src=video_path,controls=True)
            
            #button=html.Button('translate',id='translate-button',n_clicks=0)
            #return f'Uploaded {filename}',button,{'video_path':video_path}
            return f'Uploaded {filename}',video_embedded,{'video_path':video_path}
        except Exception as e:
            print(e)
            pass
    else:
        return 'Upload video','',''

@app.callback(Output('video-translated','children'),
             [Input('translate-button','n_clicks'),
             State('filename-temp','data')])
def translate_video(n_clicks,filename_dict):
    print(ctx.triggered_id)
    if ctx.triggered_id=='translate-button':
        video_name=filename_dict['video_path']
        data = {
            "srclang": "es",
            "dstlang": "it",
            "filename":video_name
        }
        resp=requests.post('http://localhost:5000/translate',json=data)
        return resp['response']
    else:
        return ''


if __name__=='__main__':
    app.run(debug=True)