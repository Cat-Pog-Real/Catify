import pygame

pygame.init()

from time import time
from sys import exit
from os.path import basename

from scripts import input
from scripts import hud
from scripts import screen_setup
hud.garbage_img = pygame.transform.scale(pygame.image.load('user_data/default_files/open_trash.png'),(30,30)).convert_alpha()

from file_handler import player
from file_handler import grabber
from file_handler import song_preview
from file_handler import playlist_handler

grabber.default_img = pygame.image.load('user_data/preview_thumbnail/default.jpg').convert()

from special import command, presence, windows_interacter, hwnd_to_exe_string

#pygame.init()

# global variables
background_color = (20,20,20)
transparent_color = (255, 0, 128)
active_fps = 60
inactve_fps = 8
target_fps = active_fps

delta_time = 0
previous_frame_time = time()
fps = 0

# Add Hud Elements

def clamp(input, min, max):
    if input < min:
        return min
    elif input > max:
        return max
    else:
        return input

def init_hud(arg=0):

    if arg == 1:
        volume_pos = hud.slider_list[0].circle_pos[0] - hud.slider_list[0].pos[0]
        repeat_checked = hud.checkbox_list[0].checked
        shuffle_checked = hud.checkbox_list[1].checked
        mute_checked = hud.checkbox_list[2].checked
        edit_checked = hud.checkbox_list[3].checked
        download_text = hud.textInput_list[0].text

    hud.block_list = []
    hud.textInput_list = []
    hud.button_list = []
    hud.button_ID = 0
    hud.slider_list = []
    hud.slider_ID = 0
    hud.texture_button_list = []
    hud.texture_button_ID = 0
    hud.checkbox_list = []
    hud.checkbox_ID = 0

    hud.add_block([0,0],[screen_setup.screen_width,40],(10,10,10),0)
    hud.add_block([0,screen_setup.screen_height-80],[screen_setup.screen_width,80],(10,10,10),0)

    text_width = 600
    if text_width > screen_setup.screen_width:
        text_width = screen_setup.screen_width-20
    text_height = clamp(150*((screen_setup.screen_height/700)**2),35,250)
    hud.add_textInput([screen_setup.center_x-(text_width/2),screen_setup.screen_height-text_height-87],[text_width,text_height],(210,210,210),"Put Youtube Link Here:",(100,100,100),hud.small_text_font,(30,30,30),"",[10,10],1)
    hud.add_textInput([290,5],[120,30],(210,210,210),"Search:",(100,100,100),hud.small_text_font,(30,30,30),"",[3,5],2)
    hud.add_textInput([screen_setup.screen_width-473,screen_setup.screen_height-59],[245,40],(210,210,210),"Playlist Name:",(100,100,100),hud.small_text_font,(30,30,30),"",[2,0],3)

    hud.add_button([screen_setup.center_x-75+105,screen_setup.screen_height-60],[150,40],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.medium_text_font,"Download",[7,4],1)

    hud.add_slider([screen_setup.screen_width-190,17],[120,10],9,(200,200,200),(40,40,40),(240,240,240),0.18,0.01,hud.small_text_font,'Volume:',[-64,-4],2)
    hud.add_slider([screen_setup.screen_width-150,screen_setup.screen_height-40],[140,10],9,(200,200,200),(40,40,40),(240,240,240),0.18,0,hud.small_text_font,'0:00',[51,-22],2)

    hud.add_button([5,5],[90,30],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.small_text_font,"Download",[12,6],0)
    hud.add_button([100,5],[90,30],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.small_text_font,"Song list",[16,6],0)
    hud.add_button([195,5],[90,30],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.small_text_font,"Playlists",[17,6],0)

    hud.add_button([screen_setup.screen_width-220,screen_setup.screen_height-60],[210,40],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.medium_text_font,"Create Playlist",[7,4],3)

    hud.add_texture_button([screen_setup.screen_width-363,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Pause",[-1,-20],2,pygame.image.load('user_data/default_files/pause.png').convert_alpha(),[-0.5,1],8)
    hud.add_texture_button([screen_setup.screen_width-318,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Skip +1",[-3,-20],2,pygame.image.load('user_data/default_files/skip_song.png').convert_alpha(),[-2,1],8)
    hud.add_texture_button([screen_setup.screen_width-408,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Skip -1",[-3,-20],2,pygame.transform.flip(pygame.image.load('user_data/default_files/skip_song.png').convert_alpha(),True,False),[2,1],8)

    hud.add_checkbox([screen_setup.screen_width-205,screen_setup.screen_height-50],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Repeat',[-8,-20],2)
    hud.add_checkbox([screen_setup.screen_width-257,screen_setup.screen_height-50],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Shuffle',[-8,-20],2)

    hud.add_checkbox([screen_setup.screen_width-292,5],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Mute:',[-42,7],2)
    hud.add_checkbox([screen_setup.screen_width-105,5],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Edit Playlists:',[-95,7],3)

    if arg == 1:
        hud.slider_list[0].circle_pos[0] = volume_pos+hud.slider_list[0].pos[0]
        hud.checkbox_list[0].checked = repeat_checked
        hud.checkbox_list[1].checked = shuffle_checked
        hud.checkbox_list[2].checked = mute_checked
        hud.checkbox_list[3].checked = edit_checked
        hud.textInput_list[0].text = download_text
        input.texture_update = True

init_hud()
presence.start_discord()
windows_interacter.register_media_keys()

MEDIA_APPS = ['spotify.exe', 'vlc.exe', 'mpc-hc64.exe', 'chrome.exe', 'firefox.exe', 'opera.exe', 'operagx.exe']
UPDATE_RATE = 0.25 # seconds
counter = 0

while True:
    # Handling Background Position and Color
    #if screen_setup.screen_no_window == False:
    screen_setup.screen.fill(background_color)
    #else:
    #    win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 5, 0, 0, 1)
    #    screen_setup.screen.fill(transparent_color)

    # Check if the window is in focus and lock meadia keys
    counter += delta_time
    if counter >= UPDATE_RATE:
        counter = 0
        last_part = basename(str(hwnd_to_exe_string.window_focused()))
        #print(last_part)
        if last_part.lower() in MEDIA_APPS:
            windows_interacter.unregister_media_keys()
        elif last_part.lower() == 'python.exe' or last_part.lower() == 'catify.exe':
            windows_interacter.register_media_keys()

    # Update Inputs
    input.update_inputs()

    # Draw Game
    grabber.grabber_tick()
    song_preview.update_songbox_preview()
    if grabber.just_downloaded and hud.playlist_path != '':
        hud.load_playlist()
        hud.load_playlist_checked()
        grabber.update_songbox = True
        song_preview.update_songbox_preview(hud.playlist_songs)
        grabber.just_downloaded = False
    if hud.searching:
        grabber.update_songbox = True
        text = hud.textInput_list[1].text
        if '|' in text:
            text = str(text).replace('|','')
        if hud.playlist_songs == []:
            song_preview.search_songs(text)
        elif hud.edit_playlists == False:
            song_preview.search_songs(text,hud.playlist_songs)
        else:
            song_preview.search_songs(text)
        hud.textInput_list[1].text = ''
        hud.songbox_tick(1)
        if hud.edit_playlists:
            hud.load_playlist_checked()
        hud.searching = False
        grabber.update_songbox = False
    if hud.playlist_changed:
        grabber.update_songbox = True
        hud.load_playlist()
        if hud.edit_playlists:
            song_preview.update_songbox_preview()
        else:
            song_preview.update_songbox_preview(hud.playlist_songs)
        hud.songbox_tick(1)
        hud.load_playlist_checked()
        hud.playlist_changed = False
        grabber.update_songbox = False
    playlist_handler.update_playlistbox_hud()
    if hud.create_playlist:
        grabber.update_playlistbox = True
        text = hud.textInput_list[2].text
        if '|' in text:
            text = str(text).replace('|','')
        playlist_handler.create_playlist(text)
        playlist_handler.update_playlistbox_hud()
        hud.textInput_list[2].text = ''
        hud.playlistbox_tick()
        hud.create_playlist = False
        grabber.update_playlistbox = False

    if screen_setup.changed_res:
        grabber.update_songbox = True
        grabber.update_playlistbox = True
        song_preview.update_songbox_preview()
        playlist_handler.update_playlistbox_hud()
        init_hud(1)

    # Draw Hud/Gui DRAW LAST
    hud.hud_tick()
    hud.draw_text(screen_setup.project_name,hud.title_text_font,hud.text_color,[screen_setup.screen_width-62,8]) # DRAWING CATIFY

    # Read Custom Commands
    command.custom_commands()

    # draw ontop of hud
    player.player_tick(delta_time)

    # Exit Game
    for event in pygame.event.get():
        input.mouse_scroll(event)
        hud.hud_event(event)
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()

    if pygame.display.get_active():
        target_fps = active_fps
    else:
        target_fps = inactve_fps

    # Update Display and locks the framerate to the target fps also calculates delta_time also gets current fps
    screen_setup.screen_tick()

    pygame.display.update()
    if target_fps != 0 and target_fps < 1001:
        screen_setup.clock.tick(target_fps)
    else:
        screen_setup.clock.tick()
        #pygame.event.wait(1)

    fps = screen_setup.clock.get_fps()
    current_frame_time = time()
    delta_time = current_frame_time - previous_frame_time
    previous_frame_time = current_frame_time