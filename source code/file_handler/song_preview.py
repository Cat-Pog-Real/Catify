from os import path, listdir
from glob import glob, escape
from math import floor
import pygame

from scripts import hud
from scripts import screen_setup

from file_handler import grabber

def grab_songs(folder_path):
    folder_names = []
    
    # Check if the provided path is a directory
    if path.isdir(folder_path):
        # Iterate over items in the folder
        for item in listdir(folder_path):
            item_path = path.join(folder_path, item)
            # If the item is a directory, add it to the list
            if path.isdir(item_path):
                folder_names.append(item)
    
    # Count the number of folders
    folder_count = len(folder_names)
    
    return folder_count, folder_names

from mutagen.mp3 import MP3

def get_audio_length(file_path):
    # Load the MP3 file
    audio = MP3(file_path)
    # Get the length of the audio in seconds
    length_in_seconds = audio.info.length
    return length_in_seconds

# Example usage:
#folder_path = 'user_data/songs/'
#folder_count, folder_names = grab_songs(folder_path)

def draw_text(text,font,text_color,width):
    new_name = text
    song_name_width = font.render(text,True,text_color).get_width()
    max_width = width-140
    if song_name_width > max_width:
        average_letter_width = song_name_width/len(text)
        new_name = text[:floor(max_width/average_letter_width)-floor(average_letter_width*0.5)]+'...'
    img = font.render(new_name,True,text_color)
    return img

x = 0
y = 0

def update_songbox_preview(arg=[]):
    if grabber.update_songbox == True:
        global x, y

        x = 0
        y = 0

        folder_path = 'user_data/songs/'
        folder_count, folder_names = grab_songs(folder_path)
        if arg == []:
            pass
        else:
            folder_names = arg
            folder_count = len(folder_names)


        hud.songbox_list = []

        for i in range(folder_count):
            song_name = folder_names[i]

            temp_folder_path = folder_path + folder_names[i]

            file = glob(escape('user_data/songs/'+song_name+'//')+'**.mp3')
            try:
                #print(file[0])
                open('user_data/default_files/output.txt', 'w').close()
            except:
                print("ERROR WITH SONG NAME!!!")
                pygame.display.quit()
                pygame.quit()
                exit()
            song_path = file[0]

            if path.exists(song_path):
                song_length_in_seconds = get_audio_length(song_path)
                minutes = int(song_length_in_seconds // 60)
                seconds = int(song_length_in_seconds % 60)
                if seconds > 9:
                    song_length = str(minutes) + ':' + str(seconds)
                else:
                    song_length = str(minutes) + ':0' + str(seconds)
            else:
                #print(song_path)
                song_length = 'N/A'

            small_width = 751

            if screen_setup.screen_width < small_width:
                width = screen_setup.screen_width
            else:
                width = screen_setup.screen_width/2

            hud.add_songbox([(((screen_setup.screen_width/2)-10+5)*x) + 5,40+5+(40*y)],[width-10,35],hud.button_idle,(40,40,40),'user_data/songs/' + song_name + '/' + song_name + '.jpg',pygame.transform.scale(pygame.image.load('user_data/songs/' + song_name + '/' + song_name + '.jpg'), (40, 30)).convert(),[2,2],song_name,draw_text(song_name,hud.small_text_font,hud.text_color,width-10),song_length,[50,9],[415,9],2,song_path,song_length_in_seconds,temp_folder_path)

            x += 1
            if screen_setup.screen_width < small_width:
                if x > 0:
                    x = 0
                    y += 1
            else:
                 if x > 1:
                    x = 0
                    y += 1
        grabber.update_songbox = False
        hud.new_shuffle_list = []
        for i in range(len(hud.songbox_list)):
            hud.new_shuffle_list.append(i)
        hud.songbox_tick(1)
        if hud.edit_playlists:
            hud.load_playlist()
            hud.load_playlist_checked()

def clamp(input, min, max):
    if input < min:
        return min
    elif input > max:
        return max
    else:
        return input

def search_songs(search_string,arg=[]):
    search_string = str(search_string).lower()
    folder_path = 'user_data/songs/'
    if arg == []:
        folder_count, folder_names = grab_songs(folder_path)
    else:
        folder_names = arg
        folder_count = len(arg)
    song_names = []
    for i in range(folder_count):
        song_name = folder_names[i]
        song_names.append(song_name)
    search_letters = []
    no_duplicate_string = ''
    for char in search_string:
        if char not in no_duplicate_string:
            no_duplicate_string = no_duplicate_string+char
    no_duplicate_string = no_duplicate_string.replace(' ','')
    for letter in no_duplicate_string:
        search_letters.append(letter)
    matching_string = []
    for name in song_names:
        if search_string in str(name).lower():
            matching_string.append(name)
    matching_letters = []
    passing_grade = clamp(len(search_letters)-1,1,9999)
    for name in song_names:
        letter_pass = 0
        for letter in search_letters:
            if letter in str(name).lower():
                letter_pass += 1
        if letter_pass >= passing_grade:
            matching_letters.append(name)
    if search_string == '':
        update_songbox_preview(arg)
    elif matching_string != []:
        if len(matching_string) > 3 and len(matching_string) < 7:
            temp = list(dict.fromkeys(matching_string+matching_letters))
            update_songbox_preview(temp)
        else:
            update_songbox_preview(matching_string)
    elif matching_letters != []:
        update_songbox_preview(matching_letters)
    else:
        update_songbox_preview(arg)
        print('none are matching')