import time
import firebase_admin
import speech_recognition as sr
from gtts import gTTS
from audioplayer import AudioPlayer
from firebase_admin import credentials
from firebase_admin import db 
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import numpy as np


#config firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartcar-009-default-rtdb.firebaseio.com/'
    })


#PERINTAH LANGSUNG

# 1.Lampu dekat
lampudekat_turnon = ['dekat', 'lampu', 'nyala'], ['dekat', 'lampu', 'nyala', 'ya'], ['dekat', 'lampu', 'nyalain'], ['dekat', 'lampu', 'nyalain', 'ya'], ['dekat', 'lampu', 'hidup', 'ya'], ['dekat', 'lampu', 'hidup'], ['dekat', 'lampu', 'hidupin'], ['dekat', 'lampu', 'hidupin', 'ya'], ['deket', 'lampu', 'nyala'], ['deket', 'lampu', 'nyala', 'ya'], ['deket', 'lampu', 'nyalain'], ['deket', 'lampu', 'nyalain', 'ya'], ['deket', 'lampu', 'hidup', 'ya'], ['deket', 'lampu', 'hidup'], ['deket', 'lampu', 'hidupin'], ['deket', 'lampu', 'hidupin', 'ya']
lampudekat_turnoff = ['dekat', 'lampu', 'mati'], ['dekat', 'lampu', 'mati', 'ya'], ['dekat', 'lampu', 'matiin'], ['dekat', 'lampu', 'matiin', 'ya'], ['dekat', 'lampu', 'redup', 'ya'], ['dekat', 'lampu', 'redup'], ['dekat', 'lampu', 'redupin'], ['dekat', 'lampu', 'redupin', 'ya']

# 2. Lampu jauh
lampujauh_turnon = ['jauh', 'lampu', 'nyala'], ['jauh', 'lampu', 'nyala', 'ya'], ['jauh', 'lampu', 'nyalain'], ['jauh', 'lampu', 'nyalain', 'ya'], ['hidup', 'jauh', 'lampu', 'ya'], ['hidup', 'jauh', 'lampu'], ['hidupin', 'jauh', 'lampu'], ['hidupin', 'jauh', 'lampu', 'ya']
lampujauh_turnoff = ['jauh', 'lampu', 'mati'], ['jauh', 'lampu', 'mati', 'ya'], ['jauh', 'lampu', 'matiin'], ['jauh', 'lampu', 'matiin', 'ya'], ['jauh', 'lampu', 'redup', 'ya'], ['jauh', 'lampu', 'redup'], ['jauh', 'lampu', 'redupin'], ['jauh', 'lampu', 'redupin', 'ya']

# 3. Lampu senja
lampusenja_turnon = ['lampu', 'nyala', 'senja'], ['lampu', 'nyala', 'senja', 'ya'], ['lampu', 'nyalain', 'senja'], ['lampu', 'nyalain', 'senja', 'ya'], ['hidup', 'lampu', 'senja', 'ya'], ['lampu', 'nyala', 'senja'],['lampu', 'nyalain', 'senja'], ['hidup', 'lampu', 'senja'], ['hidupin', 'lampu', 'senja'], ['hidupin', 'lampu', 'senja', 'ya'], ['nyala', 'senja'], ['nyalain', 'senja',], ['nyala', 'senja', 'ya'], ['nyalain', 'senja', 'ya']
lampusenja_turnoff = ['lampu', 'mati', 'senja'], ['lampu', 'matiin', 'senja'], ['lampu', 'mati', 'senja',], ['lampu', 'mati', 'senja', 'ya'], ['lampu', 'matiin', 'senja'], ['lampu', 'matiin', 'senja', 'ya'], ['lampu', 'redup','senja', 'ya'], ['lampu', 'redup', 'senja'], ['lampu', 'redupin', 'senja', ], ['lampu', 'redupin', 'senja', 'ya'], ['mati', 'senja'], ['matiin', 'senja'], ['mati', 'senja', 'ya'], ['matiin', 'senja', 'ya']

# 4. Lampu kabin
lampukabin_turnon = ['kabin', 'lampu', 'nyala'], ['kabin', 'lampu', 'nyala', 'ya'], ['kabin', 'lampu', 'nyalain'], ['kabin', 'lampu', 'nyalain', 'ya'], ['hidup', 'kabin', 'lampu', 'ya'], ['hidup', 'kabin', 'lampu'], ['hidupin', 'kabin', 'lampu'], ['hidupin', 'kabin', 'lampu', 'ya'], ['kabin', 'nyala'], ['kabin', 'nyalain'], ['kabin', 'nyala', 'ya'], ['kabin', 'nyalain', 'ya']
lampukabin_turnoff = ['kabin', 'lampu', 'mati'], ['kabin', 'lampu', 'mati', 'ya'], ['kabin', 'lampu', 'matiin'], ['kabin', 'lampu', 'matiin', 'ya'], ['kabin', 'lampu', 'redup', 'ya'], ['kabin', 'lampu', 'redup'], ['kabin', 'lampu', 'redupin'], ['kabin', 'lampu', 'redupin', 'ya'], ['kabin', 'mati'], ['kabin', 'matiin'], ['kabin', 'mati', 'ya'], ['kabin', 'matiin', 'ya']
# 5. Lampu hazard
lampuhazard_turnon = ['hazard', 'lampu', 'nyala'], ['hazard', 'lampu', 'nyala', 'ya'], ['hazard', 'lampu', 'nyalain'], ['hazard', 'lampu', 'nyalain', 'ya'], ['hazard', 'lampu', 'hidup', 'ya'], ['hazard', 'lampu', 'hidup'], ['hazard', 'lampu', 'hidupin'], ['hazard', 'lampu', 'hidupin', 'ya'], ['hazard', 'nyala'], ['hazard', 'nyalain'], ['hazard', 'nyala', 'ya'], ['hazard', 'nyalain', 'ya'], ['hazar', 'lampu', 'nyala'], ['hazar', 'lampu', 'nyala', 'ya'], ['hazar', 'lampu', 'nyalain'], ['hazar', 'lampu', 'nyalain', 'ya'], ['hazar', 'hidup', 'lampu', 'ya'], ['hazar','hidup', 'lampu'], ['hazar', 'hidupin', 'lampu'], ['hazar', 'hidupin', 'lampu', 'ya'], ['hazar', 'nyala'], ['hazar', 'nyalain'], ['hazar', 'nyala', 'ya'], ['hazar', 'nyalain', 'ya']
lampuhazard_turnoff = ['hazard', 'lampu', 'mati'], ['hazard', 'lampu', 'mati', 'ya'], ['hazard', 'lampu', 'matiin'], ['hazard', 'lampu', 'matiin', 'ya'], ['hazard', 'lampu', 'redup', 'ya'], ['hazard', 'lampu', 'redup'], ['hazard', 'lampu', 'redupin'], ['hazard', 'lampu', 'redupin', 'ya'], ['hazard', 'mati'], ['hazard', 'matiin'], ['hazard', 'mati', 'ya'], ['hazard', 'matiin', 'ya'], ['hazar', 'lampu', 'mati'], ['hazar', 'lampu', 'mati', 'ya'], ['hazar', 'lampu', 'matiin'], ['hazar', 'lampu', 'matiin', 'ya'], ['hazar', 'lampu', 'redup', 'ya'], ['hazar', 'lampu', 'redup'], ['hazar', 'lampu', 'redupin'], ['hazar', 'lampu', 'redupin', 'ya'], ['hazar', 'mati'], ['hazar', 'matiin'], ['hazar', 'mati', 'ya'], ['hazar', 'matiin', 'ya']
# 6. Sein kiri
seinkiri_turnon = ['kiri', 'lampu', 'nyala', 'sein'], ['kiri', 'lampu', 'nyalain', 'sein'], ['kiri', 'lampu', 'nyala', 'sein', 'ya'], ['kiri', 'lampu', 'nyalain', 'sein', 'ya'], ['hidup', 'kiri', 'lampu', 'sein'], ['hidupin', 'kiri', 'lampu', 'sein'], ['hidup', 'kiri', 'lampu', 'sein', 'ya'], ['hidupin', 'kiri', 'lampu', 'sein', 'ya'], ['kiri', 'lampu', 'nyala', 'sen'], ['kiri', 'lampu', 'nyalain', 'sen'], ['kiri', 'lampu', 'nyala', 'sen', 'ya'], ['kiri', 'lampu', 'nyalain', 'sen', 'ya'], ['hidup', 'kiri', 'lampu', 'sen'], ['hidupin', 'kiri', 'lampu', 'sen'], ['hidup', 'kiri', 'lampu', 'sen', 'ya'], ['hidupin', 'kiri', 'lampu', 'sen', 'ya'], ['kiri','nyala','sein'], ['kiri','nyala','sein', 'ya'], ['kiri','nyalain','sein'], ['kiri','nyalain','sein', 'ya'], ['kiri','nyala','sen'], ['kiri','nyala','sen', 'ya'], ['kiri','nyalain','sen'], ['kiri','nyalain','sen', 'ya'], ['hidup', 'kiri', 'sein'], ['hidupin', 'kiri', 'sein'], ['hidup', 'kiri', 'sein', 'ya'], ['hidupin', 'kiri', 'sein', 'ya'], ['kiri', 'nyala', 'sen'], ['nyala', 'sendiri'], ['kiri', 'nyala', 'send'], ['kiri', 'nyala', 'sent'], ['kiri', 'nyala', 'senter'], ['kiri', 'nyalain', 'senter']
seinkiri_turnoff = ['kiri', 'lampu', 'mati', 'sein'], ['kiri', 'lampu', 'matiin', 'sein'], ['kiri', 'lampu', 'mati', 'sein', 'ya'], ['kiri', 'lampu', 'matiin', 'sein', 'ya'], ['kiri', 'mati', 'sein', 'ya'], ['kiri', 'mati', 'sein'], ['kiri', 'lampu', 'mati', 'sen'], ['kiri', 'lampu', 'matiin', 'sen'], ['kiri', 'lampu', 'mati', 'sen', 'ya'], ['kiri', 'lampu', 'matiin', 'sen', 'ya'], ['kiri', 'mati', 'sen', 'ya'], ['kiri', 'mati', 'sen'], ['kiri', 'mati', 'senter']
# 7. Sein kanan
seinkanan_turnon = ['kanan', 'nyala', 'sen'], ['kanan', 'lampu', 'nyala', 'sein'], ['kanan', 'lampu', 'nyalain', 'sein'], ['kanan', 'lampu', 'nyala', 'sein', 'ya'], ['kanan', 'lampu', 'nyalain', 'sein', 'ya'], ['hidup', 'kanan', 'lampu', 'sein'], ['hidupin', 'kanan', 'lampu', 'sein'], ['hidup', 'kanan', 'lampu', 'sein', 'ya'], ['hidupin', 'kanan', 'lampu', 'sein', 'ya'], ['kanan', 'lampu', 'nyala', 'sen'], ['kanan', 'lampu', 'nyalain', 'sen'], ['kanan', 'lampu', 'nyala', 'sen', 'ya'], ['kanan', 'lampu', 'nyalain', 'sen', 'ya'], ['hidup', 'kanan', 'lampu', 'sen'], ['hidupin', 'kanan', 'lampu', 'sen'], ['hidup', 'kanan', 'lampu', 'sen', 'ya'], ['hidupin', 'kanan', 'lampu', 'sen', 'ya'], ['kanan','nyala','sein'], ['kanan','nyala','sein', 'ya'], ['kanan','nyalain','sein'], ['kanan','nyalain','sein', 'ya'], ['kanan','nyala','sen'], ['kanan','nyala','sen', 'ya'], ['kanan','nyalain','sen'], ['kanan','nyalain','sen', 'ya'], ['hidup', 'kanan', 'sein'], ['hidupin', 'kanan', 'sein'], ['hidup', 'kanan', 'sein', 'ya'], ['hidupin', 'kanan', 'sein', 'ya'], ['kanan', 'nyala', 'senter'] , ['kanan', 'nyala', 'sen'], ['nyala', 'sentanan'], ['nyala', 'lampu', 'sentanan']
seinkanan_turnoff = ['kanan', 'lampu', 'mati', 'sein'], ['kanan', 'lampu', 'matiin', 'sein'], ['kanan', 'lampu', 'mati', 'sein', 'ya'], ['kanan', 'lampu', 'matiin', 'sein', 'ya'], ['kanan', 'mati', 'sein', 'ya'], ['kanan', 'mati', 'sein'], ['kanan', 'lampu', 'mati', 'sen'], ['kanan', 'lampu', 'matiin', 'sen'], ['kanan', 'lampu', 'mati', 'sen', 'ya'], ['kanan', 'lampu', 'matiin', 'sen', 'ya'], ['kanan', 'mati', 'sen', 'ya'], ['kanan', 'mati', 'sen'], ['kanan', 'mati', 'senter'], ['mati', 'sentanan'], ['mati', 'lampu', 'sentanan']

# ////////// AC \\\\\\\\\\\\\

# 8. AC
ac_adjectives_on = ['acnya', 'nyala'], ['acnya', 'nyalain'],['acnya', 'hidup'], ['acnya', 'hidupin'], ['ac', 'nyala'], ['ac', 'nyalain'], ['ac', 'hidup'], ['ac', 'hidupin'], ['acnya', 'nyala', 'ya'], ['acnya', 'nyalain', 'ya'], ['acnya', 'hidup', 'ya'], ['acnya', 'hidupin', 'ya'], ['ac', 'nyala', 'ya'], ['ac', 'nyalain', 'ya'], ['ac', 'hidup', 'ya'], ['ac', 'hidupin', 'ya']
ac_adjectives_off = ['ac', 'mati'], ['ac', 'matiin'], ['ac', 'mati', 'ya'], ['ac', 'matiin', 'ya'], ['acnya', 'mati'], ['acnya', 'matiin'], ['acnya', 'mati', 'ya'], ['acnya', 'matiin', 'ya']

# ////////// Radio \\\\\\\\\\\\\

# 9. Radio 
radio_adjectives_on = ['nyala', 'radio'], ['hidup', 'radio'], ['nyalain', 'radio'], ['hidupin', 'radio'], ['nyala', 'radio', 'ya'], ['nyalain', 'radio', 'ya'], ['hidup', 'radio'], ['hidupin', 'radio'], ['hidupin', 'radio', 'ya'], ['hidup', 'radio', 'ya']
radio_adjectives_off = ['mati', 'radio'], ['matiin', 'radio'], ['mati', 'radio', 'ya'], ['matiin', 'radio', 'ya']

# ///////// Wiper \\\\\\\\\\

# 10. Wiper depan
wiperdepan_turnon = ['depan', 'nyala', 'wiper'], ['depan', 'nyalain', 'wiper'], ['depan', 'nyala', 'wiper', 'ya'], ['depan', 'nyalain', 'wiper', 'ya'], ['depan', 'hidup', 'wiper'], ['depan', 'hidupin', 'wiper'], ['depan', 'hidup', 'wiper', 'ya'], ['depan', 'hidupin', 'wiper', 'ya'], ['depan', 'nyala']
wiperdepan_turnoff = ['depan', 'mati', 'wiper'], ['depan', 'matiin', 'wiper'], ['depan', 'mati', 'wiper', 'ya'], ['depan', 'matiin', 'wiper', 'ya']

# 11. Wiper belakang
wiperbelakang_turnon = ['belakang', 'nyala', 'wiper'], ['belakang', 'nyalain', 'wiper'], ['belakang', 'nyala', 'wiper', 'ya'], ['belakang', 'nyalain', 'wiper', 'ya'], ['belakang', 'hidup', 'wiper'], ['belakang', 'hidupin', 'wiper'], ['belakang', 'hidup', 'wiper', 'ya'], ['belakang', 'hidupin', 'wiper', 'ya'], ['belakang', 'nyala']
wiperbelakang_turnoff = ['belakang', 'mati', 'wiper'], ['belakang', 'matiin', 'wiper'], ['belakang', 'mati', 'wiper', 'ya'], ['belakang', 'matiin', 'wiper', 'ya'], ['belakang', 'mati', 'wifi']


# ///////// Jendela \\\\\\\\\\
# 12. Jendela mobil
jendela_turnon = ['buka', 'jendela'], ['bukain', 'jendela'], ['jendela', 'turun'], ['jendela', 'turunin'], ['buka', 'jendela', 'ya'], ['bukain', 'jendela', 'ya'], ['jendela','turun', 'ya'], ['jendela', 'turunin', 'ya']
jendela_turnoff = ['jendela', 'tutup'], ['jendela', 'tutupin'], ['jendela', 'naik'], ['jendela', 'naikin'], ['jendela', 'tutup',  'ya'], ['jendela','naik', 'ya'], ['jendela', 'tutupin', 'ya'], ['jendela','naikin', 'ya']


#PERINTAH MENGGUNAKAN SYARAT
dingin_trigger =['dingin'], ['angin'], ['tiris'], ['dingin', 'ya']
lampu_trigger = ['gelap'], ['tidak', 'lihat'], ["kabut"], ['gelap', 'ya']
panas_trigger = ['panas'], ['gerah'], ['harudang'], ['panas', 'ya'], ['gerah', 'ya']
radio_trigger = ["bosan"], ['jenuh'], ['gabut'], ['kesepian'], ['bosen'], ['sepi'], ['bosan', 'ya'], ['bosen', 'ya'], ['jenuh', 'ya']
hujan_trigger = ["hujan"], ['kaca', 'kotor'], ['hujan', 'ya']
darurat_trigger = ["darurat"], ['buru', 'buru'], ['celaka'], ['buru']
halo = ['halo','siti'] ,['siti'], ['hai', 'siti'], ['alo'], ['halow'], ['helo'], ['hi', 'siti'], ['halo','city'], ['halo'], ['city']
reset = ['mulai', 'ulang'], ['ulang'], ['reset'], ['reset', 'sistem'], ['mati', 'semua']
  
#JAWABAN PERSETUJUAN 
setuju = ['iya'], ['boleh'], ['silah'], ['ya'], ['oke'], ['ok'], ['siap'], ['okeh']
tidak_setuju = ['tidak'], ['ga'], ['engga'], ['ga', 'usah'], ['ga', 'perlu'], ['tidak', 'perlu'], ['tidak', 'usah'], ['gausah']
batal = ['batal'], ['cancel'], ['batalin']
shutdown = ['mati', 'siti'], ['mati', 'mesin'], ['berhenti'], ['berenti'], ['stop']



#SpeechRecogniton 
r = sr.Recognizer()
class SpeechRecogniton:
#Initializes r for Recognizer()
    def recording():
        with sr.Microphone() as source:
            
            print("You can speak now")
            AudioPlayer("beep.wav").play(block=True)
            datatext=r.record(source, duration=5)
            data=''
        try:
            data = r.recognize_google(datatext, language= "id-ID")
            print(data)
        except:
            print('error')
        return data

#text to Speech
class GoogleTextToSpeech:
    def Speech(text):
        tts = gTTS(text, lang="id")
        tts.save("Speech.mp3")
        AudioPlayer("Speech.mp3").play(block=True)

class StateMachine: 
     
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise Exception("must call .set_start() before .run()")
        if not self.endStates:
            raise  Exception("at least one state must be an end_state")
    
        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("state :", newState)
                break 
            else:
                handler = self.handlers[newState.upper()]  
gts = GoogleTextToSpeech
class Transitions:

    def start_transitions(txt):
        start_time = time.time()
        word = command
        ref = db.reference('Car/')
        users_ref = ref.child('Siti')
        snapshot = ref.child('Siti').get()
        # print(snapshot)
        if word in halo:      
            if snapshot == 1:
                gts.Speech("Ada yang bisa saya bantu?")
                txt = textProcess.nlp()
                newState = "idle"
            elif snapshot == 0:
                users_ref.set(1)
                gts.Speech("Halo, apa yang ingin anda lakukan?")
                txt = textProcess.nlp()
                newState = "idle"
        else:
            gts.Speech("Katakan Halo Siti untuk memberikan perintah")
            newState = "error_state"
        return (newState, txt)

    def idle_state_transitions(txt):
        word = txt

        #////// 1. AC //////////
        if word in ac_adjectives_on:
            newState = "ac_state"
        
        elif word in ac_adjectives_off:
            newState = "ac_state"
        
        elif word in halo:
            ref = db.reference('Car/')
            users_ref = ref.child('Siti')
            snapshot = ref.child('Siti').get()
            if snapshot == 1:
                users_ref.set(0)
                newState = "Start"

        #////// 2. LAMPU DEKAT//////////
        elif word in lampudekat_turnon:
            newState = "lampudekat_state"
        elif word in lampudekat_turnoff:
            newState = "lampudekat_state"    

        #////// 3. LAMPU JAUH//////////
        elif word in lampujauh_turnon:
            newState = "lampujauh_state"
        elif word in lampujauh_turnoff:
            newState = "lampujauh_state"

        #////// 4. LAMPU KABIN//////////
        elif word in lampukabin_turnon:
            newState = "kabin_state"
        elif word in lampukabin_turnoff:
            newState = "kabin_state"

        #////// 5. LAMPU SENJA//////////
        elif word in lampusenja_turnon:
            newState = "senja_state"
        elif word in lampusenja_turnoff:
            newState = "senja_state"
        
        #////// 6. LAMPU HAZARD//////////
        elif word in lampuhazard_turnon:
            newState = "hazard_state"
        elif word in lampuhazard_turnoff:
            newState = "hazard_state"
            
        #////// 7. LAMPU SEIN KIRI//////////
        elif word in seinkiri_turnon:
            newState = "seinkiri_state"
        elif word in seinkiri_turnoff:
            newState = "seinkiri_state"
            
        #////// 8. LAMPU SEIN KANAN/////////
        elif word in seinkanan_turnon:
            newState = "seinkanan_state"
        elif word in seinkanan_turnoff:
            newState = "seinkanan_state"

        #////// 9. RADIO//////////
        elif word in radio_adjectives_on:
            newState = "radio_state"
        elif word in radio_adjectives_off:
            newState = "radio_state"

        #////// 10. WIPER DEPAN//////////
        elif word in wiperdepan_turnon:
            newState = "wiperdepan_state"
        elif word in wiperdepan_turnoff:
            newState = "wiperdepan_state"
            
        #////// 11. WIPER BELAKANG//////////
        elif word in wiperbelakang_turnon:
            newState = "wiperbelakang_state"
        elif word in wiperbelakang_turnoff:
            newState = "wiperbelakang_state"
            
        #////// 12. JENDELA//////////
        elif word in jendela_turnon:
            newState = "jendela_state"
        elif word in jendela_turnoff:
            newState = "jendela_state"
        

            
        #PERINTAH TRIGGER
        elif word in shutdown:
            start_time = time.time()
            ref = db.reference('Car/')
            users_ref = ref.child('Siti')
            snapshot = ref.child('Siti').get()
            users_ref.set(0)
            newState = "off_state"
            exit()

        elif word in dingin_trigger:
            newState = "dingin_state"

        elif word in panas_trigger:
            newState = "panas_state"
        
        elif word in radio_trigger:
            newState = "bosan_state"

        elif word in lampu_trigger:
            newState = "gelap_state"

        elif word in hujan_trigger:
            newState = "hujan_state"

        elif word in darurat_trigger:
            newState = "darurat_state"

        elif word in reset:
            start_time = time.time()
            ref = db.reference('Car/')
            drop_lampudekat = ref.child('Lampu Dekat')
            drop_lampujauh = ref.child('Lampu Jauh')
            drop_lampukabin = ref.child('Lampu Kabin')
            drop_lampuhazard = ref.child('Lampu Hazard')
            drop_lampusenja = ref.child('Lampu Senja')
            drop_seinkiri = ref.child('Sein Kiri')
            drop_seinkanan = ref.child('Sein Kanan')
            drop_wdepan = ref.child('Wiper Depan')
            drop_wbelakang = ref.child('Wiper Belakang')
            drop_radio = ref.child('Radio')
            drop_ac = ref.child('AC')
            drop_jendela = ref.child('Jendela')

            drop_lampudekat.set(0)
            drop_lampujauh.set(0)
            drop_lampukabin.set(0)
            drop_lampuhazard.set(0)
            drop_lampusenja.set(0)
            drop_seinkiri.set(0)
            drop_seinkanan.set(0)
            drop_wdepan.set(0)
            drop_wbelakang.set(0)
            drop_radio.set(0)
            drop_ac.set(0)
            drop_jendela.set(0)
            print("berhasil mereset database")
            newState = "end_state"
            
        elif word in batal:
            print('batalkan perintah')
            newState = "Start"
        else:
            gts.Speech("Perintah tidak diketahui")
            newState = "end_state"
        
        return (newState, txt)

    # LAMPU DEKAT TRANISITION
    def lampudekat_state_transitions(txt):
        start_time = time.time()
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Lampu Dekat')
        snapshot = ref.child('Lampu Dekat').get()
        if word in lampudekat_turnon: 
            if snapshot == 1:
                gts.Speech("lampu dekat sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu dekat")
                users_ref.set(1)
                newState = "end_state"
        elif word in lampudekat_turnoff:
            if snapshot == 0:
                gts.Speech("lampu dekat sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu dekat")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
   
        return (newState, txt)

    # LAMPU JAUH TRASNITION
    def lampujauh_state_transitions(txt):
        start_time = time.time()
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Lampu Jauh')
        snapshot = ref.child('Lampu Jauh').get()
        if word in lampujauh_turnon: 
            if snapshot == 1:
                gts.Speech("lampu jauh sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu jauh")
                users_ref.set(1)
                newState = "end_state"
        elif word in lampujauh_turnoff:
            if snapshot == 0:
                gts.Speech("lampu jauh sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu jauh")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
        
        return (newState, txt)

    # LAMPU KABIN TRANSITION
    def lampukabin_state_transitions(txt):
        
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Lampu Kabin')
        snapshot = ref.child('Lampu Kabin').get()
        if word in lampukabin_turnon: 
            if snapshot == 1:
                gts.Speech("lampu kabin sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu kabin")
                users_ref.set(1)
                newState = "end_state"
        elif word in lampukabin_turnoff:
            if snapshot == 0:
                gts.Speech("lampu kabin sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu kabin")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
        
        return (newState, txt)

    # LAMPU SENJA TRANSITION
    def lampusenja_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Lampu Senja')
        snapshot = ref.child('Lampu Senja').get()
        if word in lampusenja_turnon: 
            if snapshot == 1:
                gts.Speech("lampu senja sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu senja")
                users_ref.set(1)
                newState = "end_state"
        elif word in lampusenja_turnoff:
            if snapshot == 0:
                gts.Speech("lampu senja sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu senja")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
        
        return (newState, txt)

    # LAMPU HAZARD TRANSITION
    def lampuhazard_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Lampu Hazard')
        snapshot = ref.child('Lampu Hazard').get()
        if word in lampuhazard_turnon: 
            if snapshot == 1:
                gts.Speech("lampu hazard sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu hazard")
                users_ref.set(1)
                newState = "end_state"
        elif word in lampuhazard_turnoff:
            if snapshot == 0:
                gts.Speech("lampu hazard sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu hazard")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
        
        return (newState, txt)

    # LAMPU SEIN KIRI TRANSITION
    def seinkiri_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Sein Kiri')
        snapshot = ref.child('Sein Kiri').get()
        if word in seinkiri_turnon: 
            if snapshot == 1:
                gts.Speech("lampu sein kiri sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu sein kiri")
                users_ref.set(1)
                newState = "end_state"
        elif word in seinkiri_turnoff:
            if snapshot == 0:
                gts.Speech("lampu sein kiri sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu sein kiri")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
  
        return (newState, txt)

    # LAMPU SEIN KANAN TRANSITION
    def seinkanan_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Sein Kanan')
        snapshot = ref.child('Sein Kanan').get()
        if word in seinkanan_turnon: 
            if snapshot == 1:
                gts.Speech("lampu sein kanan sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan lampu sein kanan")
                users_ref.set(1)
                newState = "end_state"
        elif word in seinkanan_turnoff:
            if snapshot == 0:
                gts.Speech("lampu sein kanan sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan lampu sein kanan")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
       
        return (newState, txt)

    # RADIO TRANSITION
    def radio_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Radio')
        snapshot = ref.child('Radio').get()
        if word in radio_adjectives_on: 
            if snapshot == 1:
                gts.Speech("Radio sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan Radio")
                users_ref.set(1)
                newState = "end_state"
        elif word in radio_adjectives_off:
            if snapshot == 0:
                gts.Speech("Radio sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan Radio")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
  
        return (newState, txt)

    # WIPER DEPAN TRANSITION
    def wiperdepan_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Wiper Depan')
        snapshot = ref.child('Wiper Depan').get()
        if word in wiperdepan_turnon: 
            if snapshot == 1:
                gts.Speech("Wiper depan sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan wiper depan")
                users_ref.set(1)
                newState = "end_state"
        elif word in wiperdepan_turnoff:
            if snapshot == 0:
                gts.Speech("wiper depan sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan wiperdepan")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
       
        return (newState, txt)

    # WIPER DEPAN TRANSITION
    def wiperbelakang_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Wiper Belakang')
        snapshot = ref.child('Wiper Belakang').get()
        if word in wiperbelakang_turnon: 
            if snapshot == 1:
                gts.Speech("Wiper belakang sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan wiper belakang")
                users_ref.set(1)
                newState = "end_state"
        elif word in wiperbelakang_turnoff:
            if snapshot == 0:
                gts.Speech("wiper belakang sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan wiper belakang")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
     
        return (newState, txt)


    # AC TRANSITION
    def ac_state_transitions(txt):
        ac = ['ac', 'nyala'], ['ac'], ['nyalain', 'ac'], ['ac', 'nyala', 'ya']
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('AC')
        snapshot = ref.child('AC').get()
        if word in ac_adjectives_on: 
            if snapshot == 1:
                gts.Speech("AC sudah dalam keadaan menyala")
                newState = "end_state"
            else:
                gts.Speech("baik menyalakan AC")
                users_ref.set(1)
                newState = "end_state"
        elif word in ac_adjectives_off:
            if snapshot == 0:
                gts.Speech("AC sudah dalam keadaan mati")
                newState = "end_state"
            else:
                gts.Speech("baik mematikan AC")
                users_ref.set(0)
                newState = "end_state"
        elif word in ac:
            ref = db.reference('Car/')
            users_ref = ref.child('AC')
            snapshot = ref.child('AC').get()
            if snapshot == 1:
                newState = "end_state"
                gts.Speech("ac sudah dalam keadaan menyala")
            else:
                newState = "end_state"
                gts.Speech("baik menyalakan ac")
                users_ref.set(1)
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
      
        return (newState, txt)

    # JENDELA TRANSITION
    def jendela_state_transitions(txt):
        word = txt
        ref = db.reference('Car/')
        users_ref = ref.child('Jendela')
        snapshot = ref.child('Jendela').get()
        if word in jendela_turnon: 
            if snapshot == 1:
                gts.Speech("Jendela sudah dalam keadaan membuka")
                newState = "end_state"
            else:
                gts.Speech("Baik membuka jendela")
                users_ref.set(1)
                newState = "end_state"
        elif word in jendela_turnoff:
            if snapshot == 0:
                gts.Speech("Jendela sudah dalam keadaan tertutup")
                newState = "end_state"
            else:
                gts.Speech("Baik menutup jendela")
                users_ref.set(0)
                newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "end_state"
       
        return (newState, txt)


    def bosan_state_transitions(txt):
        setuju_radio = ['setuju'], ['boleh'], ['silahkan'], ['ya'], ['oke'], ['ok'], ['siap'], ['okeh'], ['boleh', 'nyala', 'radio'], ['boleh','hidup', 'radio'], ['boleh', 'nyalain', 'radio'] , ['boleh','hidupin', 'radio'], ['hidup', 'oke', 'radio'], ['nyalain', 'oke', 'radio'], ['hidupin', 'oke', 'radio'], ['nyala', 'radio', 'ya'],  ['iya'], ['yah'], ['hidup', 'radio', 'ya'], ['boleh','nyala', 'radio', 'ya'], ['boleh','hidup', 'radio', 'ya'], ['boleh', 'nyalain', 'radio', 'ya'] , ['boleh','hidupin', 'radio', 'ya'], ['hidup', 'oke', 'radio', 'ya'], ['nyalain', 'oke', 'radio', 'ya'], ['nyala', 'oke', 'radio', 'ya']
        tidak_setuju_radio = ['tidak'], ['ga'], ['engga'], ['ga', 'usah'], ['ga', 'perlu'], ['tidak', 'perlu'], ['tidak', 'usah'], ['gausah'], ['gamau'], ['jangan'], ['gausah', 'nyala', 'radio'], ['gausah', 'nyalain', 'radio']
        word = txt
        gts.Speech("apakah ingin menyalakan radio?")
        word= textProcess.nlp()
        if word in setuju_radio:
            gts.Speech("baik menyalakan Radio")
            ref = db.reference('Car/')
            users_ref = ref.child('Radio')
            users_ref.set(1)
            newState = "radio_state_end"
        elif word in tidak_setuju_radio:
            gts.Speech("oke radio tetap mati")
            ref = db.reference('Car/')
            users_ref = ref.child('Radio')
            users_ref.set(0)
            newState = "radio_state_end"
        elif word in batal:
            gts.Speech("Ok, panggil saya kembali untuk memeberikan perintah")  
            newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "bosan_state"
  
        return (newState, txt)

    def panas_state_transitions(txt):
        ac = ['ac', 'nyala'], ['ac'], ['nyalain', 'ac'], ['ac', 'nyala', 'ya']
        jendela = ['buka', 'jendela'], ['jendela'], ['bukain', 'jendela'], ['jendela', 'naikin']
        word = txt
        gts.Speech("apakah ingin menyalakan ac atau membuka jendela?")
        word= textProcess.nlp()
        if word in ac:
            ref = db.reference('Car/')
            users_ref = ref.child('AC')
            snapshot = ref.child('AC').get()
            if snapshot == 1:
                newState = "ac_state_end"
                gts.Speech("ac sudah dalam keadaan menyala")
            else:
                newState = "ac_state_end"
                gts.Speech("baik menyalakan ac")
                users_ref.set(1)
        elif word in jendela:
            ref = db.reference('Car/')
            users_ref = ref.child('Jendela')
            snapshot = ref.child('Jendela').get()
            if snapshot == 1:
                gts.Speech("jendela sudah dalam keadaan terbuka")
                newState = "jendela_state_end"
            else:
                gts.Speech("baik membuka jendela")
                users_ref.set(1)
                newState = "jendela_state_end"
        else:
            gts.Speech("Perintah tidak diketahui")
            newState = "panas_state"
      
        return (newState, txt)

    def gelap_state_transitions(txt):
        start_time = time.time()
        choose_kabin = ['kabin', 'lampu'], ['kabin', 'lampu', 'nyala'], ['kabin', 'lampu', 'nyala'], ['kabin', 'lampu', 'nyala', 'ya'], ['kabin', 'lampu', 'nyalain'], ['kabin', 'lampu', 'nyalain', 'ya'], ['hidup', 'kabin', 'lampu', 'ya'], ['hidup', 'kabin', 'lampu'], ['hidupin', 'kabin', 'lampu'], ['hidupin', 'kabin', 'lampu', 'ya'], ['kabin', 'nyala'], ['kabin', 'nyalain'], ['kabin', 'nyala', 'ya'], ['kabin', 'nyalain', 'ya']
        choose_senja = ['lampu', 'senja'], ['lampu', 'nyala', 'senja'], ['senja'], ['kabut'], ['kabut', 'lampu'], ['lampu', 'nyala', 'senja'], ['lampu', 'nyala', 'senja', 'ya'], ['lampu', 'nyalain', 'senja'], ['lampu', 'nyalain', 'senja', 'ya'], ['hidup', 'lampu', 'senja', 'ya'], ['lampu', 'nyala', 'senja'],['lampu', 'nyalain', 'senja'], ['hidup', 'lampu', 'senja'], ['hidupin', 'lampu', 'senja'], ['hidupin', 'lampu', 'senja', 'ya'], ['nyala', 'senja'], ['nyalain', 'senja',], ['nyala', 'senja', 'ya'], ['nyalain', 'senja', 'ya']
        choose_jauh = ['jauh', 'lampu'], ['jauh', 'lampu', 'nyala'], ['jauh'], ['jauh', 'lampu', 'ya'], ['jauh', 'lampu', 'nyala', 'ya'], ['jauh', 'ya'], ['jauh', 'lampu', 'nyala'], ['jauh', 'lampu', 'nyala', 'ya'], ['jauh', 'lampu', 'nyalain'], ['jauh', 'lampu', 'nyalain', 'ya'], ['hidup', 'jauh', 'lampu', 'ya'], ['hidup', 'jauh', 'lampu'], ['hidupin', 'jauh', 'lampu'], ['hidupin', 'jauh', 'lampu', 'ya']
        choose_dekat = ['deket', 'lampu', 'ya'], ['dekat', 'lampu', 'ya'], ['dekat', 'lampu'], ['dekat', 'lampu', 'nyala'], ['deket'], [ 'deket', 'lampu'], ['deket'], ['dekat', 'lampu', 'nyala'], ['dekat', 'lampu', 'nyala', 'ya'], ['dekat', 'lampu', 'nyalain'], ['dekat', 'lampu', 'nyalain', 'ya'], ['dekat', 'lampu', 'hidup', 'ya'], ['dekat', 'lampu', 'hidup'], ['dekat', 'lampu', 'hidupin'], ['dekat', 'lampu', 'hidupin', 'ya'], ['deket', 'lampu', 'nyala'], ['deket', 'lampu', 'nyala', 'ya'], ['deket', 'lampu', 'nyalain'], ['deket', 'lampu', 'nyalain', 'ya'], ['deket', 'lampu', 'hidup', 'ya'], ['deket', 'lampu', 'hidup'], ['deket', 'lampu', 'hidupin'], ['deket', 'lampu', 'hidupin', 'ya']
        word = txt
        gts.Speech("sebutkan komponen lampu mana yang ingin dinyalakan?")
        word = textProcess.nlp()
        if word in choose_kabin:
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Kabin')
            snapshot_kabin = ref.child('Lampu Kabin').get()
            if snapshot_kabin == 1:
                gts.Speech("lampu kabin sudah dalam keadaan menyala")
                newState = "lampukabin_state_end"
            else:
                gts.Speech("baik menyalakan lampu kabin")
                users_ref.set(1)
                newState = "lampukabin_state_end"
        elif word in choose_senja:
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Senja')
            snapshot_senja = ref.child('Lampu Senja').get()
            if snapshot_senja == 1:
                gts.Speech("lampu senja sudah dalam keadaan menyala")
                newState = "lampusenja_state_end"
            else:
                gts.Speech("baik menyalakan lampu senja")
                users_ref.set(1)
                newState = "lampusenja_state_end"
        elif word in choose_jauh:
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Jauh')
            snapshot_jauh = ref.child('Lampu Jauh').get()
            if snapshot_jauh == 1:
                gts.Speech("lampu jauh sudah dalam keadaan menyala")
                newState = "lampujauh_state_end"
            else:
                gts.Speech("baik menyalakan lampu jauh")
                users_ref.set(1)
                newState = "lampujauh_state_end"
        elif word in choose_dekat:
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Dekat')
            snapshot_dekat = ref.child('Lampu Dekat').get()
            if snapshot_dekat == 1:
                gts.Speech("lampu dekat sudah dalam keadaan menyala")
                newState = "lampudekat_state_end"
            else:
                gts.Speech("baik menyalakan lampu dekat")
                users_ref.set(1)
                newState = "lampudekat_state_end"
        elif word in batal:
            gts.Speech("Ok, panggil saya kembali untuk memeberikan perintah")  
            newState = "end_state"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "gelap_state"
      
        return (newState, txt)

    def dingin_state_transitions(txt):
        word = txt
        gts.Speech("apakah anda ingin mematikan AC atau menutup jendela?")
        word= textProcess.nlp()
        ac = ['ac'],['ac', 'mati'], ['ac', 'matiin'], ['ac','ya'], ['ac', 'boleh', 'mati'], ['acnya']
        jendela = ['jendela'], ['jendela', 'tutup'], ['jendela', 'tutup', 'ya'], ['jendela', 'ya'], ['jendela', 'tutupin', 'ya']
        if word in ac:
            ref = db.reference('Car/')
            users_ref = ref.child('AC')
            snapshot = ref.child('AC').get()
            if snapshot == 0:
                gts.Speech("ac sudah dalam keadaan mati")
                newState = "ac_state_end"
            else:
                gts.Speech("baik mematikan ac")
                users_ref.set(0)
                newState = "ac_state_end"
        elif word in jendela:
            ref = db.reference('Car/')
            users_ref = ref.child('Jendela')
            snapshot = ref.child('Jendela').get()
            if snapshot == 0:
                gts.Speech("jendela sudah dalam keadaan tertutup")
                newState = "jendela_state_end"
            else:
                gts.Speech("baik menutup jendela")
                users_ref.set(0)
                newState = "jendela_state_end"
        elif word in batal:
            gts.Speech("Ok, panggil saya kembali untuk menjalankan perintah")  
            newState = "end_state"
        else:
            gts.Speech("Perintah tidak diketahui")
            gts.Speech("beri jawaban mematikan ac atau menutup jendela")
            newState = "dingin_state"
    
        return (newState, txt)

    def hujan_state_transitions(txt):
        pilih_depan = ['depan', 'wiper'], ['depan', 'oke'], ['depan'], ['depan', 'nyala', 'wiper'], ['depan', 'nyalain', 'wiper'], ['depan','ya'], ['boleh', 'depan', 'nyala', 'wiper'], ['boleh', 'depan', 'hidup', 'wiper'], ['boleh', 'depan', 'nyalain', 'wiper'] , ['boleh', 'depan', 'hidupin', 'wiper'], ['depan', 'hidup', 'oke', 'wiper'], ['depan','nyalain', 'oke', 'wiper'] , ['depan','hidupin', 'oke', 'wiper']
        belakang = ['belakang', 'wiper'], ['belakang', 'oke'], ['belakang'], ['belakang', 'nyala', 'wiper'], ['belakang', 'nyalain', 'wiper'], ['belakang','ya'], ['belakang', 'boleh', 'nyala', 'wiper'], ['belakang', 'boleh', 'hidup', 'wiper'], ['belakang', 'boleh','nyalain', 'wiper'] , ['belakang', 'boleh', 'hidupin', 'wiper', ], ['belakang', 'hidup', 'oke', 'wiper'], ['belakang', 'nyalain', 'oke', 'wiper'], ['belakang', 'hidupin', 'oke', 'wiper']
        word = txt
        gts.Speech("Ingin menyalakan wiper depan atau belakang?")
        word = textProcess.nlp()
        if word in pilih_depan:
            ref = db.reference('Car/')
            users_ref = ref.child('Wiper Depan')
            snapshot = ref.child('Wiper Depan').get()
            if snapshot == 1:
                gts.Speech("wiper depan sudah dalam keadaan menyala")
                newState = "wiperdepan_state_end"
            else:
                gts.Speech("Baik, menyalakan wiper depan")
                newState = "wiperdepan_state_end"
                users_ref.set(1)
        elif word in belakang: 
            ref = db.reference('Car/')
            users_ref = ref.child('Wiper Belakang')
            snapshot = ref.child('Wiper Belakang').get()
            if snapshot == 1:
                gts.Speech("wiper belakang sudah dalam keadaan menyala")
                newState = "wiperbelakang_state_end"
            else:
                gts.Speech("Baik, menyalakan wiper belakang")
                users_ref.set(1)
                newState = "wiperbelakang_state_end"
        elif word in batal:
            gts.Speech("Ok, panggil saya kembali untuk memberikan perintah")  
            newState = "end_state" 
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "hujan_state"

        return (newState, txt)

    def darurat_state_transitions(txt):
        setuju_darurat = ['iya'], ['boleh'], ['silahkan'], ['ya'], ['oke'], ['ok'], ['siap'], ['okeh'], ['hazard', 'lampu', 'nyala', 'ya'], ['boleh','hazard', 'lampu', 'nyala'], ['boleh','hazard', 'lampu', 'nyalain'], ['boleh', 'hazard', 'lampu', 'nyala', 'ya'], ['boleh', 'hazard', 'lampu', 'nyalain', 'ya'], ['hazard', 'iya', 'lampu', 'nyala'], ['hazard', 'iya', 'nyala'], ['hazard', 'lampu', 'nyala'], ['hazard', 'lampu', 'nyalain']
        tidak_setuju_darurat = ['tidak'], ['ga'], ['engga'], ['ga', 'usah'], ['ga', 'perlu'], ['tidak', 'perlu'], ['tidak', 'usah'], ['gausah'], ['ngga'], ['enggak']
        word = txt
        gts.Speech("Apakah ingin menyalakan lampu hazard?")
        word = textProcess.nlp()
        if word in setuju_darurat:
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Hazard')
            snapshot = ref.child('Lampu Hazard').get()
            if snapshot == 1:
                gts.Speech("lampu hazard sudah dalam keadaan menyala")
                newState = "hazard_state_end"
            else:
                gts.Speech("Baik, menyalakan lampu hazard")
                users_ref.set(1)
                newState = "hazard_state_end"
        elif word in tidak_setuju_darurat:
            newState = "hazard_state_end"
            ref = db.reference('Car/')
            users_ref = ref.child('Lampu Hazard')
            snapshot = ref.child('Lampu Hazard').get()
            if snapshot == 0:
                gts.Speech("lampu hazard sudah dalam keadaan mati")
                newState = "hazard_state_end"
            else:
                gts.Speech("Baik, mematikan lampu hazard")
                users_ref.set(0)
                newState = "hazard_state_end"
        elif word in batal:
            gts.Speech("Ok, panggil saya kembali untuk memberikan perintah")  
            newState = "hazard_state_end"
        else:
            gts.Speech("perintah tidak diketahui")
            newState = "darurat_state"
        return (newState, txt)

class Preprocessting_text:
    def nlp():
        kata = input()
        factory = StemmerFactory()
        # kata = SpeechRecogniton.recording()
        print('User:'+kata)
        split_file = kata.split(" ")
        punc = """!"#$%&'(1234567890)*+,-./:;<=>?@[\]^_`{|}~"""
        file_no_punc = ["".join(char for char in string if char not in punc) for string in split_file]
        casefolding_text = [x.lower() for x in file_no_punc]
        stopword_removal = open("stopword_tala.txt", "r")
        open_tala = stopword_removal.read()
        stopword_split = open_tala.split("\n")
        new_words = [word for word in casefolding_text if word not in stopword_split]
        stemming = factory.create_stemmer()
        word_documents = [stemming.stem(word) for word in new_words]
        print("Kata-kata yang sudah diubah, User:", word_documents, "\n")
        unique_word = np.unique(word_documents)
        final_word = [word for word in unique_word if word not in stopword_split]
        print("Kata yang telah dilakukan sorting\n", final_word, "\n")
        return final_word

while True:
    textProcess = Preprocessting_text
    trs = Transitions
    print("recording")
    command = textProcess.nlp()
   
    if (command in shutdown):
        break
    m = StateMachine()
    m.add_state("Start", trs.start_transitions)
    m.add_state("idle", trs.idle_state_transitions)
    m.add_state("panas_state", trs.panas_state_transitions)
    m.add_state("dingin_state", trs.dingin_state_transitions)
    m.add_state("bosan_state", trs.bosan_state_transitions)
    m.add_state("gelap_state", trs.gelap_state_transitions) 
    m.add_state("hujan_state", trs.hujan_state_transitions) 
    m.add_state("darurat_state", trs.darurat_state_transitions)
    m.add_state("lampudekat_state", trs.lampudekat_state_transitions) 
    m.add_state("lampujauh_state", trs.lampujauh_state_transitions)
    m.add_state("kabin_state", trs.lampukabin_state_transitions)
    m.add_state("senja_state", trs.lampusenja_state_transitions)
    m.add_state("hazard_state", trs.lampuhazard_state_transitions)
    m.add_state("seinkiri_state", trs.seinkiri_state_transitions)
    m.add_state("seinkanan_state", trs.seinkanan_state_transitions)
    m.add_state("radio_state", trs.radio_state_transitions)
    m.add_state("ac_state", trs.ac_state_transitions) 
    m.add_state("jendela_state", trs.jendela_state_transitions)
    m.add_state("bosan_state", trs.bosan_state_transitions)
    m.add_state("wiperdepan_state", trs.wiperdepan_state_transitions)
    m.add_state("wiperbelakang_state", trs.wiperbelakang_state_transitions)

    m.add_state("wiperdepan_state_end", None, end_state=1)
    m.add_state("wiperbelakang_state_end", None, end_state=1)
    m.add_state("radio_state_end", None, end_state=1)
    m.add_state("ac_state_end", None, end_state=1)
    m.add_state("jendela_state_end", None, end_state=1)
    m.add_state("hazard_state_end", None, end_state=1)
    m.add_state("lampudekat_state_end", None, end_state=1)
    m.add_state("lampujauh_state_end", None, end_state=1)
    m.add_state("kabin_state_end", None, end_state=1)
    m.add_state("senja_state_end", None, end_state=1)

    m.add_state("end_state", None, end_state=1)
    m.add_state("error_state", None, end_state=1)

    m.add_state("off_state", None, end_state=1)
    m.set_start("Start")
    m.run(str(command))