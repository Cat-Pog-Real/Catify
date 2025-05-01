import pygame
from math import floor

from scripts import screen_setup

from file_handler import grabber

from special import presence

max_width = (screen_setup.screen_width/2)-120

thumbnail_path = ''
song_path = ''
song_index = 0

song_name = ''
song_length = 0

song_time_elapsed = 0
song_time_elapsed_in_seconds = floor(song_time_elapsed)

is_playing = False
is_paused = False
is_repeating = False
is_shuffle = False

shuffle_version = 'new'

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
    presence.update_discord(song_name, song_length, 0, is_paused)

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
    presence.update_discord(song_name, song_length, song_time_elapsed_in_seconds, is_paused)

def unpause_song():
    global is_paused
    is_paused = False
    pygame.mixer.music.unpause()
    presence.update_discord(song_name, song_length, song_time_elapsed_in_seconds, is_paused)

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

def get_text_width(text,font,text_color):
    img = font.render(text,True,text_color)
    return img.get_width()

def get_text_height(text,font,text_color):
    img = font.render(text,True,text_color)
    return img.get_height()

def get_letter_width(text,font,text_color):
    img = font.render(text,True,text_color)
    width = img.get_width()
    average_letter_width = width/len(text)
    return average_letter_width

song_img = ''
old_path = ''

def main():
    global song_time_elapsed, song_time_elapsed_in_seconds, pick_new_song, max_width, song_img, old_path
    if thumbnail_path != '':
        if old_path != thumbnail_path:
            song_img = ''
        if song_img == '':
            song_img = pygame.image.load(thumbnail_path)
            song_img = pygame.transform.scale(song_img,(80,60))
            old_path = thumbnail_path
        else:
            screen_setup.screen.blit(song_img,(5,screen_setup.screen_height-5-(65)))

        song_name_width = get_text_width(song_name,small_text_font,text_color)
        #max_width = (screen_setup.screen_width/2)-120
        if song_name_width > max_width:
            average_letter_width = get_letter_width(song_name,small_text_font,text_color)
            new_name = song_name[:floor(max_width/average_letter_width)-floor(average_letter_width*0.5)]+'...'
            draw_text(new_name,small_text_font,text_color,(90,screen_setup.screen_height-5-(45)))
        else:
            draw_text(song_name,small_text_font,text_color,(90,screen_setup.screen_height-5-(45)))

    song_time_elapsed_in_seconds = floor(song_time_elapsed)
    if song_time_elapsed_in_seconds >= song_length and song_path != '':
        if is_shuffle == False:
            if is_repeating:
                play_song()
            else:
                stop_song()
                song_time_elapsed = 0
                play_song()
                pause_song()
                print(is_playing)
        else:
            pick_new_song = True
    if grabber.show_text == True:
        text_width = get_text_width("DOWNLOADING SONG",small_text_font,text_color)
        text_height = get_text_height("DOWNLOADING SONG",small_text_font,text_color)
        temp_x = screen_setup.center_x-(text_width/2)
        pygame.draw.rect(screen_setup.screen,(50,50,50),(temp_x,9,text_width+10,text_height+6),0,2)
        draw_text("DOWNLOADING SONG",small_text_font,text_color,(temp_x+5,12))

def player_tick(delta_time):
    global song_time_elapsed, is_playing, is_paused
    if is_playing == True and is_paused == False:
        song_time_elapsed += delta_time
    main()