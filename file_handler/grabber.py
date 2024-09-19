import os
import urllib.request
import pytubefix
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from moviepy.editor import *

import pygame

from scripts import hud
from scripts import screen_setup
from scripts import input

import sys

output = open("default_files/output.txt", "wt")
sys.stdout = output
sys.stderr = output

def downloadThumbnail(youtube_link):
    try:
        video = pytubefix.YouTube(youtube_link)
        thumbnail_url = video.thumbnail_url
        pathname = 'songs/'+video.title+'/'+video.title+".jpg"
        urllib.request.urlretrieve(thumbnail_url, pathname)
        print("Thumbnail Downloaded")
    except KeyError:
        print("Thumbnail Falied")

def downloadMP3(youtube_link,output_path='songs/'):
    try:
        # Download the highest quality video stream
        yt = YouTube(youtube_link)
        output_path='songs/'+yt.title
        video_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = video_stream.download(output_path=output_path)
        # Convert the video file to MP3
        mp4_file = downloaded_file
        mp3_file = mp4_file.replace(".mp4", ".mp3")
        # Using moviepy to convert to MP3
        audio_clip = AudioFileClip(mp4_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        # Remove the original MP4 file to save space
        os.remove(mp4_file)
        # downloads thumbnail
        downloadThumbnail(youtube_link)
        
        print("MP3 Downloaded")

        open('default_files/output.txt', 'w').close()
                
    except Exception as e:
        print(f"An error occurred: {e}")

url = ""
last_url = url

preview_name = ""

def is_real_video(txt,arg):
        global url, last_url
        url = txt
        if arg == 0:
            if url != last_url:
                try:
                    video = YouTube(url)
                except RegexMatchError:
                    return False
                else:
                    return True
            else:
                return "SAME TEXT"
        elif arg == 1:
            try:
                video = YouTube(url)
            except RegexMatchError:
                return False
            else:
                return True

update_songbox = True
show_text = False

def attempt_download(url):
    global update_songbox, show_text
    show_text = True
    update_songbox = False
    result = is_real_video(url,1)
    if result == True:
        downloadMP3(url)
        print("Succesful Download")
    else:
        print("you blow")
    input.max_scroll_value = -1
    update_songbox = True
    show_text = False

def grabber_tick():
    text_Input = hud.textInput_list[0]
    global url, last_url, preview_name
    if hud.curScene == 1:
        last_url = url
        url = text_Input.text

        result = is_real_video(url,0)
        if result != "SAME TEXT":
            if os.path.exists('preview_thumbnail/preview.jpg'):
                os.remove('preview_thumbnail/preview.jpg')
                preview_name = ""
            if result == True:
                video = YouTube(url)
                preview_name = video.title
                thumbnail_url = video.thumbnail_url
                pathname = 'preview_thumbnail/'+"preview"+".jpg"
                urllib.request.urlretrieve(thumbnail_url, pathname)
                print("Preview Downloaded")

        result = is_real_video(url,1)
        if result == True:
            img = pygame.image.load('preview_thumbnail/preview.jpg')
            img = pygame.transform.scale(img,(481,360))
            screen_setup.screen.blit(img,(screen_setup.center_x-(481/2),screen_setup.center_y-300))
            hud.draw_text(preview_name,hud.medium_text_font,hud.text_color,[screen_setup.center_x-(len(preview_name)*7.6),screen_setup.center_y+65])
        elif result == False:
            img = pygame.image.load('preview_thumbnail/default.jpg')
            img = pygame.transform.scale(img,(481,360))
            screen_setup.screen.blit(img,(screen_setup.center_x-(481/2),screen_setup.center_y-300))
            blank = "No Video"
            hud.draw_text(blank,hud.medium_text_font,hud.text_color,[screen_setup.center_x-(len(blank)*7.6),screen_setup.center_y+65])
