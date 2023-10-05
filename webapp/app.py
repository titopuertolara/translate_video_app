from dash import Dash,dcc,html,Input,Output,callback,State,ctx
import os
import base64
from googletrans import constants
import time
import requests


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server=app.server
languages=constants.LANGUAGES
language_pickers=  html.Div([
                        html.Div(id='lang_origin',
                            children=[dcc.Dropdown(id='langsrc',options=[{'label':languages[i],'value':i} for i in languages],placeholder='Video language')],
                            style={'width':'50%'}
                        ),
                        html.Div(id='lang_destiny',
                            children=[dcc.Dropdown(id='langdst',options=[{'label':languages[i],'value':i} for i in languages],placeholder='Subtitles language')],
                            style={'width':'50%'}

                        )

                    ])

app.layout=html.Div([
    html.Div([
        html.Img(id='main-img',src='assets/images/fuffy1.png',width=100,height=100,style={'margin-left':'32%','position':'absolute','margin-top':'0.2%'}),
        html.H3('Add subtitles to video',style={'margin-top':'3%','position':'absolute'})
    
    ],style={'margin':'auto','width':'80%','text-align':'center'}),
    dcc.Upload(id='uploader'
        ,children=[html.P('Drag and drop your video here or click .',style={'text-align':'center'})]
        ,style={'width':'80%','height':'100px','borderStyle':'dashed','margin':'auto'}
   
    ),
    
  
  
    html.Table([  # Create an HTML table
        # Header row
        html.Tr([
            html.Th("Original", style={'border': '1px solid gray', 'text-align': 'center'}),  # Header cell 1
            html.Th("Translated", style={'border': '1px solid gray', 'text-align': 'center'})   # Header cell 2
        ]),

        # Data row
        html.Tr([
            html.Td(
                dcc.Loading(id='video-1',
                    children=[  
                        html.Div(id='name-div'),
                        language_pickers,
                        html.Div(id='video-container'),
                        html.Div(id='translate-container-btn',children=[html.Button('translate',id='translate-button',n_clicks=0)])
                    ],
                    type='circle'
                    ), 
                style={'border': '1px solid gray'}
            ),  
            html.Td(
               dcc.Loading(id='video-2',children=[ html.Div(id='video-translated')],type='circle'), 
               style={'border': '1px solid gray'}
            )   # Data cell 2
        ])
    ],style={'margin-left':'auto','margin-right':'auto','width':'80%'}),

   
   
    
   
    dcc.Store(id='filename-temp'),
    
   
    
   

])

@app.callback(Output('name-div','children'),
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
            return f'Filename :  {filename}',video_embedded,{'video_path':video_path}
        except Exception as e:
            print(e)
            pass
    else:
        return 'Not video uploaded.','',''

@app.callback(Output('video-translated','children'),
              
              
             [Input('translate-button','n_clicks'),
              State('filename-temp','data'),
             State('langsrc','value'),
             State('langdst','value')])
def translate_video(n_clicks,filename_dict,langsrc,langdst):
    
    if ctx.triggered_id=='translate-button':
        if langsrc is None:
            return 'Please select origin language.'
        if langdst is None:
            return 'Please select subtitles language.'
        if filename_dict=='':
            return 'Please upload a video.'
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
        #video_translated=html.Video(id='video-translated',src=translated_video_path,controls=True,height='480',width='640')
        #video_translated=html.Div(children=[html.Button('Download video',id='download-video'),dcc.Download(id='downloader')])
        video_translated=html.A(translated_video_path.split('/')[-1],download='video.mp4',href=translated_video_path,target="_blank")
        return video_translated
    else:
        return ''
    
    






if __name__=='__main__':
    app.run(debug=True,dev_tools_hot_reload=False)