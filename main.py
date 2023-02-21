import PyPDF2
from gtts import gTTS
from pydub import AudioSegment
import soundfile as sf
import pyrubberband as pyrb


# READING TEXT AND CONVERTING TO MP3
text = ''
name=input('PDF NAME: ')
speed = float(input('Speed: '))
pdffileobj = open('pdfs/{name}.pdf'.format(name=name), 'rb')


# create reader variable that will read the pdffileobj
pdfreader = PyPDF2.PdfReader(pdffileobj)

# This will store the number of pages of this pdf file
x = len(pdfreader.pages)

for r in range(x):
    pageobj = pdfreader.pages[r-1]
    text += pageobj.extract_text()

print('creating tts...')
tts = gTTS(text)
tts.save('sound.mp3')
print('created tts!')

# SPEEDING OR SLOWING DOWN SOUND
sound = AudioSegment.from_file("sound.mp3")
sound.export("sound.wav", format="wav")

y, sr = sf.read("sound.wav")

print('changing speed...')
# Play back at extra low speed
y_stretch = pyrb.time_stretch(y, sr, speed)
# Play back extra low tones
y_shift = pyrb.pitch_shift(y, sr, speed)
sf.write("sound.wav", y_stretch, sr, format='wav')
print('speed changed!')

print('creating MP3...')
sound = AudioSegment.from_wav("sound.wav")
sound.export("mp3s/{name}X{speed}.mp3".format(name=name,speed=str(speed)), format="mp3")
print('created MP3!')