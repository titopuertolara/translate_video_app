from dash import Dash,dcc,html,Input,Output,callback,State,ctx
import os
import base64

import time
import requests
#import base64
#from io import BytesIO

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server=app.server

app.layout=html.Div([
    dcc.Input(id='video-route',type='text'),    
    html.Button('go',id='buttoncito',n_clicks=0),
    html.Video(id='video',controls=True,)


])
@app.callback(Output('video','src'),
              [Input('buttoncito','n_clicks'),
               State('video-route','value')])
def test_fn(n_clicks,route):
    if ctx.triggered_id=='buttoncito':
        print(route)
        return route
    else:
        return ''
if __name__=='__main__':
    app.run(debug=True,dev_tools_hot_reload=False,port=8051)

