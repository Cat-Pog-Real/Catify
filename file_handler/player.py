import pygame
import time
import math
import threading

from scripts import screen_setup

from file_handler import grabber

thumbnail_path = ''
song_path = ''
song_index = 0

song_name = ''
song_length = 0

song_time_elapsed = 0
song_time_elapsed_in_seconds = math.floor(song_time_elapsed)

is_playing = False
is_paused = False
is_repeating = False
is_shuffle = False

pick_new_song = False

def set_paths(path1,path2):
    global thumbnail_path, song_path
    thumbnail_path = path1
    song_path = path2

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)

def play_song():
    global is_playing, is_paused, song_time_elapsed
    is_playing = True
    is_paused = False
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)
    song_time_elapsed = 0

def change_time(time):
    global is_repeating
    if is_repeating == False:
        pygame.mixer.music.play(loops=0, start=time)
    else:
        pygame.mixer.music.play(loops=-1, start=time)

def pause_song():
    global is_paused
    is_paused = True
    pygame.mixer.music.pause()

def unpause_song():
    global is_paused
    is_paused = False
    pygame.mixer.music.unpause()

def stop_song():
    global is_playing
    is_playing = False
    pygame.mixer.music.stop()

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

small_text_font = pygame.font.SysFont("Arial",15)
text_color = (246,250,240)

def draw_text(text,font,text_color,pos):
    img = font.render(text,True,text_color)
    screen_setup.screen.blit(img,pos)

def main():
    global song_time_elapsed, song_time_elapsed_in_seconds, pick_new_song
    if thumbnail_path != '':
        img = pygame.image.load(thumbnail_path)
        img = pygame.transform.scale(img,(80,60))
        screen_setup.screen.blit(img,(5,screen_setup.screen_height-5-(65)))
        if len(song_name) < 39:
            draw_text(song_name,small_text_font,text_color,(90,screen_setup.screen_height-5-(45)))
        else:
            new_txt = song_name[:39] + '...'
            draw_text(new_txt,small_text_font,text_color,(90,screen_setup.screen_height-5-(45)))
    song_time_elapsed_in_seconds = math.floor(song_time_elapsed)
    if song_time_elapsed_in_seconds >= song_length and song_path != '':
        if is_shuffle == False:
            if is_repeating:
                play_song()
            else:
                stop_song()
                song_time_elapsed = 0
        else:
            pick_new_song = True
    if grabber.show_text == True:
        draw_text("DOWNLOADING SONG",small_text_font,text_color,(350,11))

running = True

def counter():
    global song_time_elapsed, is_playing, is_paused, running
    while running:

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        except:
            running = False

        if is_playing == True and is_paused == False:
            time.sleep(0.1)
            song_time_elapsed += 0.1
        else:
            time.sleep(0.1)

thread1 = threading.Thread(target=counter)
thread1.start()

def player_tick():
    main()