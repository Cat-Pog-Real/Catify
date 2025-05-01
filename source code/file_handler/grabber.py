from os import path, remove
from urllib.request import urlretrieve
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from moviepy import AudioFileClip
from math import floor

import pygame

from scripts import hud
from scripts import screen_setup
from scripts import input

import sys

ILLEGAL_CHARACTERS = [':', '<', '>', '/', '\\', '"', '|', '?', '*']

output = open("user_data/default_files/output.txt", "wt")
sys.stdout = output
sys.stderr = output

POTOKEN = "MnSt6qtVlvkDGq3SjLvVSmB3rjFizvv6KUlb3o8k6_labN4RNq_u4ZcgN7IoSCTvaDTbyYwen8njHusP9KQVtcbtqUATrF8jRmya3_Ebi1Ht5y0qkCoOLHcDtNLm8boqX7iwNOTG8vlPpJvy1msvZCdujr_vKQ=="
VISITOR_DATA = "Cgs1T2szczB2RU9sWSjsxsC8BjIKCgJVUxIEGgAgHg%3D%3D"

def token_verifier(vistor_data=VISITOR_DATA, po_token=POTOKEN):
    return vistor_data, po_token

def grab_video(youtube_link):
    #video = YouTube(youtube_link, use_po_token=True, po_token_verifier=token_verifier())
    #video = YouTube(youtube_link, client='WEB', use_po_token=True, po_token_verifier=token_verifier())
    #video = YouTube(youtube_link, client='WEB')
    video = YouTube(youtube_link)
    return video

def downloadThumbnail(video):
    try:
        #video = grab_video(youtube_link)
        thumbnail_url = video.thumbnail_url
        title = str(video.title)
        for char in ILLEGAL_CHARACTERS:
            if char in video.title:
                title = title.replace(char, '')
        pathname = 'user_data/songs/'+title+'/'+title+".jpg"
        urlretrieve(thumbnail_url, pathname)
        print("Thumbnail Downloaded")
    except KeyError:
        print("Thumbnail Falied")

def downloadMP3(video,output_path='user_data/songs/'):
    try:
        # Download the highest quality video stream
        #yt = grab_video(youtube_link)
        #output_path='user_data/songs/'+yt.title
        #video_stream = yt.streams.filter().first()
        title = str(video.title)
        for char in ILLEGAL_CHARACTERS:
            if char in video.title:
                title = title.replace(char, '')
        print(title)
        output_path='user_data/songs/'+title
        video_stream = video.streams.filter().first()
        downloaded_file = video_stream.download(output_path=output_path)
        # Convert the video file to MP3
        mp4_file = downloaded_file
        mp3_file = mp4_file.replace(".mp4", ".mp3")
        # Using moviepy to convert to MP3
        audio_clip = AudioFileClip(mp4_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        # Remove the original MP4 file to save space
        remove(mp4_file)
        # downloads thumbnail
        #downloadThumbnail(youtube_link)
        downloadThumbnail(video)
        
        print("MP3 Downloaded")

        open('user_data/default_files/output.txt', 'w').close()
                
    except Exception as error:
        print(f"An error occurred: {error}")

url = ""
last_url = url

preview_name = ""

def is_real_video(txt,arg):
        global url, last_url
        url = txt
        if arg == 0:
            if url != last_url:
                try:
                    video = grab_video(url)
                except RegexMatchError:
                    return False, 'FALSE'
                else:
                    return True, video
            else:
                return "SAME TEXT", 'FALSE'
        elif arg == 1:
            try:
                video = grab_video(url)
            except RegexMatchError:
                return False, 'FALSE'
            else:
                return True, video

update_songbox = True
just_downloaded = False
update_playlistbox = True
show_text = False

default_img = ''
preview_img = ''

def attempt_download(url):
    global update_songbox, show_text, just_downloaded
    show_text = True
    update_songbox = False
    result, video = is_real_video(url,1)
    if result == True:
        downloadMP3(video)
        print("Succesful Download")
    else:
        print("you blow")
    input.max_scroll_value = -1
    update_songbox = True
    just_downloaded = True
    show_text = False

def clamp(input, min, max):
    if input < min:
        return min
    elif input > max:
        return max
    else:
        return input

def grabber_tick():
    text_Input = hud.textInput_list[0]
    global url, last_url, preview_name, default_img, preview_img
    
    if hud.curScene == 1:
        if '|' in url:
            url = str(url).replace('|','')
        last_url = url
        url = text_Input.text
        if '|' in url:
            url = str(url).replace('|','')
    
        result, video = is_real_video(url,0)
        preview_changed = False
        if result != "SAME TEXT":
            if path.exists('user_data/preview_thumbnail/preview.jpg'):
                remove('user_data/preview_thumbnail/preview.jpg')
                preview_name = ""
                #preview_img = pygame.image.load('user_data/preview_thumbnail/default.jpg').convert()
                preview_changed = True
            if result == True:
                title = str(video.title)
                for char in ILLEGAL_CHARACTERS:
                    if char in video.title:
                        title = title.replace(char, '')
                preview_name = title
                thumbnail_url = video.thumbnail_url
                pathname = 'user_data/preview_thumbnail/'+"preview"+".jpg"
                urlretrieve(thumbnail_url, pathname)
                preview_img = pygame.image.load('user_data/preview_thumbnail/preview.jpg').convert()
                preview_changed = False
                print("Preview Downloaded")

        if preview_changed:
            preview_img = default_img

        result, video = is_real_video(url,1)
        if result == True:
            img = pygame.transform.scale(preview_img,(480*(screen_setup.screen_width/1000),360*(screen_setup.screen_height/700)))
            screen_setup.screen.blit(img,(screen_setup.center_x-(img.get_width()/2),40+(10*((screen_setup.screen_height/700)**2))))
            font = hud.medium_text_font
            if screen_setup.screen_width > 751:
                font = hud.medium_text_font
            elif screen_setup.screen_width > 500:
                font = hud.title_text_font
            else:
                font = hud.small_text_font
            text_width = hud.get_text_width(preview_name,font,hud.text_color)
            if text_width > screen_setup.screen_width:
                max_width = screen_setup.screen_width-60
                average_letter_width = hud.get_letter_width(preview_name,font,hud.text_color)
                new_name = preview_name[:floor(max_width/average_letter_width)-floor(average_letter_width*0.5)]+'...'
                text_width = hud.get_text_width(new_name,font,hud.text_color)
                hud.draw_text(new_name,font,hud.text_color,[screen_setup.center_x-(text_width/2),img.get_height()+40+(10*((screen_setup.screen_height/700)**2))+clamp(9*((screen_setup.screen_height/700)**2),0,9)])
            else:
                hud.draw_text(preview_name,font,hud.text_color,[screen_setup.center_x-(text_width/2),img.get_height()+40+(10*((screen_setup.screen_height/700)**2))+clamp(9*((screen_setup.screen_height/700)**2),0,9)])
        elif result == False:
            img = pygame.transform.scale(default_img,(480*(screen_setup.screen_width/1000),360*(screen_setup.screen_height/700)))
            screen_setup.screen.blit(img,(screen_setup.center_x-(img.get_width()/2),40+(10*((screen_setup.screen_height/700)**2))))
            blank = "No Video"
            font = hud.medium_text_font
            if screen_setup.screen_width > 751:
                font = hud.medium_text_font
            elif screen_setup.screen_width > 500:
                font = hud.title_text_font
            else:
                font = hud.small_text_font
            text_width = hud.get_text_width(blank,font,hud.text_color)
            hud.draw_text(blank,font,hud.text_color,[screen_setup.center_x-(text_width/2),img.get_height()+40+(10*((screen_setup.screen_height/700)**2))+clamp(9*((screen_setup.screen_height/700)**2),0,9)])
