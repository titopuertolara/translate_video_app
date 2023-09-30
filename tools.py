import os 
#import whisper 
import time
from googletrans import Translator,constants

class video_processor:
    def __init__(self,video_file_name,model):
        self.video_file_name=video_file_name
        self.name=self.video_file_name.split('.')[0]
        self.model=model
        self.translator=Translator()
    def extract_audio(self):
        
        command=f'ffmpeg -i "{self.video_file_name}" -y "{self.name}.mp3"'
        print('1.Extracting audio..')
        os.system(command)
        print('Done.')
    def transcribe_audio(self):
        print('2.Transcribing..')
        self.result=self.model.transcribe(f'{self.name}.mp3')
        print('Done')
    def translate_text(self,src_lang='es',dest_lang='en'):
        print('3. Translating..')
        self.final_res=[{'id':r['id'],\
            'start':time.strftime("%H:%M:%S,000", time.gmtime(r['start'])),\
            'end':time.strftime("%H:%M:%S,000", time.gmtime(r['end'])),\
            'text':r['text'],\
            'translation':self.translator.translate(r['text'],src=src_lang, dest=dest_lang).text} for r in self.result['segments']]
        print('Done.')
    def create_srt(self):
        print('4.Creating srt file')
        self.srt_txt=''
        for r in self.final_res:
            self.srt_txt+=f"{str(r['id']+1)}\n{r['start']} --> {r['end']}\n{r['translation']}\n\n"
        with open(f'{self.name}.srt','w') as srtfile:
            srtfile.write(self.srt_txt)
        print('Done.')
    def merge_subtitles(self):
        print('5. Merging video subtitles')
        command=f'ffmpeg -i "{self.video_file_name}" -vf subtitles="{self.name}.srt" "{self.name}_with_subtitles.mp4"'
        os.system(command)
        print('Done.')

    







