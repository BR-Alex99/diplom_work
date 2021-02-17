from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
import pymorphy2


import json
from vosk import Model, KaldiRecognizer
import sys
import os
import wave

f= open('bad_words.txt')
bad_words_vocabulary=f.read()
bad_words_vocabulary=bad_words_vocabulary.split(', ')

def text_scan(text):
    return lazy_text_scan(text)
def audio_scan(file_name):
    text=audio_to_txt(file_name)
    return text_scan(text)
	
def normalize_txt(text):
    words_in_text=word_tokenize(text, language="russian")
    stop_words=stopwords.words("russian")
    stop_words+=[']','[','.',',',';',':','!','?','','#','-','``',"''"]
    filtered_words=[]
    for token in words_in_text:
        if token not in stop_words:
            filtered_words.append(token)
            
    
    morph = pymorphy2.MorphAnalyzer()
    for i in range(len(filtered_words)):
        filtered_words[i] = morph.parse(filtered_words[i])[0].normal_form
    end_txt=''
    for word in filtered_words:
        end_txt=end_txt+' '+word
    return(end_txt)
	

def lazy_text_scan(text):
    x=text.split('\n')
    text=''
    for line in x:
        text+=line + ' '
    text = normalize_txt(text)
    array_words=text.split(' ')
    agressiv_flag = 0
    for word in array_words:
        if word in bad_words_vocabulary:
            agressiv_flag=1
            break
    
    if agressiv_flag==0:
        return 0
    else:
        return 1
    
def audio_to_txt(file_name):
    
    os.system(f'ffmpeg -i {file_name} out.wav')
    
    model = Model("model")

    # Large vocabulary free form recognition
    rec = KaldiRecognizer(model, 16000)

    wf = wave.open('out.wav', "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    rec = KaldiRecognizer(model, wf.getframerate())
    transcript=''
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            json_dict = json.loads(rec.Result())
            transcript += json_dict['text']
        else:
            rec.PartialResult()
    os.system(f'rm out.wav')
    return transcript
	

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def progress(count, total, suffix=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()