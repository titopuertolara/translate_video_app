from dash import Dash,dcc,html,Input,Output,callback,State,ctx
import os
import base64
from googletrans import constants
import time
import requests
import base64
from io import BytesIO

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server=app.server
languages=constants.LANGUAGES
app.layout=html.Div([

    dcc.Upload(id='uploader',children=['Drag and drop'],style={'width':'50%','borderStyle':'dashed'}),
    html.Div(id='output-div'),
    html.Div([
        html.Div(id='lang_origin',
            children=[dcc.Dropdown(id='langsrc',options=[{'label':languages[i],'value':i} for i in languages],placeholder='Original language')],
            style={'width':'20%','display':'inline-block'}
        ),
        html.Div(id='lang_destiny',
            children=[dcc.Dropdown(id='langdst',options=[{'label':languages[i],'value':i} for i in languages],placeholder='Subtitles language')],
            style={'width':'20%','display':'inline-block'}

        )

    ]),
  
    html.Table([  # Create an HTML table
        # Header row
        html.Tr([
            html.Th("Original", style={'border': '1px solid gray', 'text-align': 'center'}),  # Header cell 1
            html.Th("Translated", style={'border': '1px solid gray', 'text-align': 'center'})   # Header cell 2
        ]),

        # Data row
        html.Tr([
            html.Td(
                dcc.Loading(id='video-1',children=[html.Div(id='video-container')],type='circle'), 
                style={'border': '1px solid gray'}
            ),  
            html.Td(
               dcc.Loading(id='video-2',children=[ html.Div(id='video-translated')],type='circle'), 
               style={'border': '1px solid gray'}
            )   # Data cell 2
        ])
    ]),

    html.Div(id='translate-container-btn',children=[html.Button('translate',id='translate-button',n_clicks=0)]),
   
    
    
    dcc.Store(id='filename-temp'),
   
    
   

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
            
            
            video_embedded=html.Video(id='video-player',src=video_path,controls=True,height='480',width='640')
            
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
              State('filename-temp','data'),
             State('langsrc','value'),
             State('langdst','value')])
def translate_video(n_clicks,filename_dict,langsrc,langdst):
    print(ctx.triggered_id)
    if ctx.triggered_id=='translate-button':
        video_name=filename_dict['video_path']
        data = {
            "srclang": langsrc,
            "dstlang": langdst,
            "filename":video_name
        }
        print(data)

        resp=requests.post('http://localhost:5000/translate',json=data)
        #print(resp.json()['response'])
        translated_video_path=resp.json()['response'] #another option but deppending of api return
        #print(translated_video_path)
        
        #video_data=base64.b64encode(resp.content).decode('utf-8')
        
        #translated_video_path=f"data:video/mp4;base64,{video_data}"
        video_translated=html.Video(id='video-translated',src=translated_video_path,controls=True,height='480',width='640')
        return video_translated
    

        






if __name__=='__main__':
    app.run(debug=True,dev_tools_hot_reload=False)