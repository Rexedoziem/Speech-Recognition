import json
import os
import subprocess
from urllib.request import urlopen
import speech_recognition as sr
import sys
import re
import smtplib
import requests
import subprocess
from pyowm.owm import OWM
import youtube_dl
import vlc
import urllib.request
from bs4 import BeautifulSoup as soup
from time import strftime
import webbrowser
from gtts import gTTS
import playsound
import random
from wikipedia import wikipedia


def sofiaResponse(audio):
    """speaks audio passed as argument"""
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)


def myCommand():
    """listens for commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def sofiaResponse(audio_string):
    tts = gTTS(text=audio_string, lang="en")
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_file)
    os.remove(audio_file)


def assistant(command):
    """if statements for executing commands"""
    # open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you Sir.')
    elif 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    # open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you Sir.')
        else:
            pass
    # greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')
    elif 'help me' in command:
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Current weather in {city_name} : Tells you the current condition and temperature
        5. Hello
        6. play me a video : Plays song in your VLC media player
        7. change wallpaper : Change desktop wallpaper
        8. news for today : reads top news of today
        9. time : Current system time
        10. top stories from google news (RSS feeds)
        11. tell me about xyz : tells you about xyz
        """)
    # joke
    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')
    # top stories from google new s
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = (Client.read())
            Client.close()
            soup_page = soup(xml_page, 'xml')
            news_list = soup_page.findAll('item')
            for news in news_list[:15]:
                sofiaResponse(news.title.text)
        except Exception as e:
            print(e)
    # current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('68ed9e03e54976e590884493c5a63b51')
            mgr = owm.weather_manager()
            obs = mgr.weather_at_place(city)
            w = obs.weather
            b = w.humidity
            q = w.status
            x = w.temperature
            sofiaResponse('Current weather in %s is %s and the temperature is %s.' % (city, q, x, b))
        # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    # To know the clock
    elif 'main time' in command:
        from time import ctime
        sofiaResponse(ctime())
    # sending mail
    elif 'email' in command:
        sofiaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'Enyinnaya' in recipient:
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            sofiaResponse('Email has been sent successfully. You can check your inbox.')
        else:
            sofiaResponse('I do not know what you mean!')
            # launch any application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            app = reg_ex.group()
            app1 = app+'.exe'
            subprocess.Popen(["open", "-n", "/Applications"], stdout=subprocess.PIPE)
            sofiaResponse('I have launched the desired application')
    # play youtube song
    elif 'play me a song' in command:
        path = '/Users/REX/Desktop/Rex/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        sofiaResponse('What song shall I play for you?')
        song = myCommand()
        if song:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + song.replace(' ', '+')
            response = urllib.request.urlopen(url)
            html = response.read()
            soup1 = soup(html, "lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
            url = url_list[0]
            ydl_opts = {}
            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)
            if flag == 0:
                sofiaResponse('I have not found anything in Youtube ')
        # change wallpaper
    elif 'change wallpaper' in command:
        folder = '/Windows/Web/Wallpaper'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
        # pic from unsplash.com
        f = urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.request.urlretrieve(photo, "/Windows/Web/Wallpaper")
        # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        sofiaResponse('wallpaper changed successfully')
        # ask me anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500])
        except Exception as e:
            print(e)
            sofiaResponse(e)

    elif 'play music' in command:
        sofiaResponse('Enjoy the coldplay of your music')
        music_dir = 'C:\\Users\\REX\\Desktop\\Rex\\Music\\Gospel\\Gospel'
        songs = os.listdir(music_dir)
        sofiaResponse('which song should i play')
        random = os.startfile(os.path.join(music_dir,songs))


sofiaResponse(
    'Hi Rex, I am Sofia and I am your personal voice assistant, '
    'Please give a command or say "help me" and I will tell you what all I can do for you.')
# loop to continue executing multiple commands


while True:
    assistant(myCommand())
