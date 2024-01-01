# translate_video_app

Add subtitles to yput videos using AI

![Screenshot from 2023-10-06 11-22-41](https://github.com/titopuertolara/translate_video_app/assets/10605898/d4826d2b-c16c-4016-9b0f-987dbffa0c5c)


Create virtual enviroment eg ```python3.9 -m env my_enviroment```<br />

```source my_enviroment/bin/activate```<br />

```cd webapp```<br />
Install requirements <br />
```pip install requirements.txt```

Activate api file

```python webapapi.py``` ( here, api service will be able to transcribe and add subtitles, listening on 5000 port) <br />

Activate webapp 

```python app.py``` (listening on 127.0.0.1:8050, this must be on another console tab ) <br />

Results are inside ```webapp/assets/uploads``` folder

