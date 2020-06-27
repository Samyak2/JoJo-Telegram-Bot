import os.path
import shutil

import whoosh.index as index
import whoosh.fields as fields
import whoosh.qparser as qparser

schema = fields.Schema(keywords=fields.TEXT(stored=False),
                       audio_url=fields.STORED(),
                       title=fields.STORED(),
                       id=fields.STORED()
                       )

if os.path.exists("index"):
    shutil.rmtree("index")
os.mkdir("index")
ix = index.create_in("index", schema)

writer = ix.writer()
writer.add_document(
    keywords="kono dio da",
    audio_url="https://www.myinstants.com/media/sounds/kono-dio-da99.mp3",
    title="Kono Dio Da!",
    id="kono-dio-da99")
writer.add_document(
    keywords="za warudo the world",
    audio_url="https://www.myinstants.com/media/sounds/za-warudo-stop-time-sound.mp3",
    title="Za Warudo!",
    id="za-warudo-stop-time-sound")
writer.add_document(
    keywords="wryyy wry wryy wryyyy",
    audio_url="https://www.myinstants.com/media/sounds/dio-wryyy.mp3",
    title="Wryyyyy",
    id="dio-wryyy")
writer.add_document(
    keywords="roundabout to be continued",
    audio_url="https://www.myinstants.com/media/sounds/untitled_1071.mp3",
    title="Roundabout",
    id="untitled_1071")
writer.add_document(
    keywords="oh no",
    audio_url="https://www.myinstants.com/media/sounds/oh-no_7.mp3",
    title="Ohh noo",
    id="oh-no_7")
writer.add_document(
    keywords="yes yes yes yes!",
    audio_url="https://www.myinstants.com/media/sounds/yes-yes-yes-yes-yes.mp3",
    title="YES YES YES YES!",
    id="yes-yes-yes-yes-yes")
writer.add_document(
    keywords="no no no no no",
    audio_url="https://www.myinstants.com/media/sounds/jotaro-no.mp3",
    title="NO NO NO NO NO!",
    id="jotaro-no")
writer.add_document(
    keywords="dero lelo rero lero",
    audio_url="https://www.myinstants.com/media/sounds/rero-rero-rero.mp3",
    title="dero dero dero",
    id="rero-rero-rero")
writer.add_document(
    keywords="ay ay ay awaken my masters",
    audio_url="https://www.myinstants.com/media/sounds/jojos-bizarre-adventure-ay-ay-ay-ay-_-sound-effect.mp3",
    title="AWAKEN",
    id="jojos-bizarre-adventure-ay-ay-ay-ay-_-sound-effect")
writer.add_document(
    keywords="nice",
    audio_url="https://www.myinstants.com/media/sounds/joseph-joestar-nice.mp3",
    title="nice",
    id="joseph-joestar-nice")
writer.add_document(
    keywords="nigerundayo run away",
    audio_url="https://www.myinstants.com/media/sounds/joestar-run.mp3",
    title="NIGERUNDAYO",
    id="joestar-run")
writer.add_document(
    keywords="yes i am tsk tsk",
    audio_url="https://www.myinstants.com/media/sounds/yes-i-am.mp3",
    title="Yes I am!",
    id="yes-i-am")
writer.add_document(
    keywords="kira yoshikage theme",
    audio_url="https://www.myinstants.com/media/sounds/yoshikage-kira-theme-ringtone.mp3",
    title="Kira Yoshikage Theme",
    id="yoshikage-kira-theme-ringtone")
writer.add_document(
    keywords="you utter fool stroheim german",
    audio_url="https://www.myinstants.com/media/sounds/img_7808.mp3",
    title="You Utttter fool",
    id="You Utttter fool")
writer.add_document(
    keywords="doppio phone ring turururu",
    audio_url="https://www.myinstants.com/media/sounds/doppio-ringing.mp3",
    title="Tu rururururu",
    id="doppio-ringing")
writer.add_document(
    keywords="oi josuke okuyasu yo",
    audio_url="https://www.myinstants.com/media/sounds/img_4189.mp3",
    title="Tu rururururu",
    id="doppio-ringing")
writer.add_document(
    keywords="arrivederci bruno bucciarati",
    audio_url="https://www.myinstants.com/media/sounds/arrivederci.mp3",
    title="Arrivederci",
    id="arrivederci")
writer.add_document(
    keywords="muda muda muda",
    audio_url="https://www.myinstants.com/media/sounds/mudamudamudamudamudamudamudamudamudamuda_1.mp3",
    title="muda muda muda",
    id="mudamudamudamudamudamudamudamudamudamuda")
writer.add_document(
    keywords="HINJAKU HINJAKU",
    audio_url="https://www.myinstants.com/media/sounds/tumblr_n5dxckfvob1sh11j9o1.mp3",
    title="HINJAKU HINJAKU",
    id="HINJAKU HINJAKU")
writer.add_document(
    keywords="yare yare daze",
    audio_url="https://www.myinstants.com/media/sounds/yare-yare-daze_zAnWvX6.mp3",
    title="Yare Yare Daze",
    id="Yare Yare Daze")
writer.add_document(
    keywords="oh my god joseph joestar",
    audio_url="https://www.myinstants.com/media/sounds/oh-my-god-jojo.mp3",
    title="Oh My God",
    id="Oh My God")
writer.add_document(
    keywords="holy shit joseph joestar",
    audio_url="https://www.myinstants.com/media/sounds/holy-shit-jojo.mp3",
    title="Holy Shit",
    id="Holy Shit")
writer.add_document(
    keywords="giorno theme giorno giovanna piano",
    audio_url="https://www.myinstants.com/media/sounds/giornos-theme-but-only-the-best-part-is-in_vwd15lya_lyb0-online-audio-converter.mp3",
    title="Giorno's Theme",
    id="Giono's Theme")
writer.add_document(
    keywords="i giorno giovanna have a dream kono giorno giovanna niwa yume ga aru",
    audio_url="https://www.myinstants.com/media/sounds/test_TUQkBD1.mp3",
    title="I Giorno Giovanna have a dream",
    id="I Giorno Giovanna have a dream")
writer.commit()

parser = qparser.QueryParser("keywords", ix.schema)

if __name__ == "__main__":
    searcher = ix.searcher()
    myquery = parser.parse("kono")
    results = searcher.search(myquery)
    print(results)
