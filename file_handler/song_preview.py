import os
import pygame
import glob

from scripts import hud
from scripts import screen_setup

from file_handler import grabber

def grab_songs(folder_path):
    folder_names = []
    
    # Check if the provided path is a directory
    if os.path.isdir(folder_path):
        # Iterate over items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            # If the item is a directory, add it to the list
            if os.path.isdir(item_path):
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
#folder_path = 'songs/'
#folder_count, folder_names = grab_songs(folder_path)

x = 0
y = 0

def update_songbox_preview():
    if grabber.update_songbox == True:
        global x, y

        x = 0
        y = 0

        folder_path = 'songs/'
        folder_count, folder_names = grab_songs(folder_path)

        hud.songbox_list = []

        for i in range(folder_count):
            song_name = folder_names[i]

            temp_folder_path = folder_path + folder_names[i]

            file = glob.glob(glob.escape('songs/'+song_name+'//')+'**.mp3')
            try:
                #print(file[0])
                open('default_files/output.txt', 'w').close()
            except:
                print("ERORR WITH SONG NAME!!!")
                print("ERORR WITH SONG NAME!!!")
                print("ERORR WITH SONG NAME!!!")
                pygame.display.quit()
                pygame.quit()
                exit()
            song_path = file[0]

            if os.path.exists(song_path):
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

            hud.add_songbox([(((screen_setup.screen_width/2)-10+5)*x) + 5,40+5+(40*y)],[(screen_setup.screen_width/2)-10,35],hud.button_idle,(40,40,40),'songs/' + song_name + '/' + song_name + '.jpg',pygame.image.load('songs/' + song_name + '/' + song_name + '.jpg'),[2,2],song_name,song_length,[50,9],[415,9],2,song_path,song_length_in_seconds,temp_folder_path)

            x += 1
            if x > 1:
                x = 0
                y += 1
        grabber.update_songbox = False
