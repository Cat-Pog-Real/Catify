from os import path, listdir, makedirs
from glob import glob, escape
import pygame

from scripts import hud
from scripts import screen_setup

from file_handler import grabber

PLAYLIST_PATH = 'user_data/playlists/'

def grab_playlists(folder_path):
    folder_names = []
    
    if path.isdir(folder_path):
        for item in listdir(folder_path):
            item_path = path.join(folder_path, item)
            if path.isdir(item_path):
                folder_names.append(item)

    folder_count = len(folder_names)
    
    return folder_count, folder_names

playlist_num, playlist_names = grab_playlists(PLAYLIST_PATH)

def create_playlist(playlist_name):
    if playlist_name not in playlist_names and playlist_name != '':
        playlist_dir = PLAYLIST_PATH+playlist_name
        makedirs(playlist_dir)
        text_file = open(playlist_dir+'/playlist_data.txt','w')
        text_file.close()
    else:
        print('playlist already exists')

x = 0
y = 0

def update_playlistbox_hud():
    global x, y, playlist_num, playlist_names
    if grabber.update_playlistbox:
        x = 0
        y = 0

        playlist_num, playlist_names = grab_playlists(PLAYLIST_PATH)

        hud.playlistbox_list = []

        for i in range(playlist_num):
            playlist_name = playlist_names[i]
            folder_path = PLAYLIST_PATH+playlist_name

            file = glob(escape('user_data/playlists/'+playlist_name+'//')+'**.txt')
            try:
                open('user_data/default_files/output.txt', 'w').close()
            except:
                print("ERROR WITH PLAYLIST NAME!!!")
                pygame.display.quit()
                pygame.quit()
                exit()
            playlist_path = file[0]

            small_width = 751

            if screen_setup.screen_width < small_width:
                width = screen_setup.screen_width
            else:
                width = screen_setup.screen_width/2

            hud.add_playlistbox([(((screen_setup.screen_width/2)-10+5)*x) + 5,40+5+(40*y)],[width-10,35],hud.button_idle,(40,40,40),playlist_name,[9,9],3,playlist_path,folder_path)

            x += 1
            if screen_setup.screen_width < small_width:
                if x > 0:
                    x = 0
                    y += 1
            else:
                 if x > 1:
                    x = 0
                    y += 1
    grabber.update_playlistbox = False