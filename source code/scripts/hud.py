import pygame
from math import floor, sqrt
from random import randrange
import threading
from os import remove
from pathlib import Path
from sys import exit

from scripts import input
from scripts import screen_setup

from file_handler import grabber
from file_handler import player

#pygame.init()

# Hud Variables
curScene = 1
volume = 0
recalculate = False

new_shuffle_list = []

# Buttons
button_list = []

# Button Colors
button_idle = (30,30,30)
button_hovered = (101,163,191)
button_clicked = (217,242,255)

button_ID = 0

class Button:
    def __init__(self,pos,pos2,idle,hovered,clicked,font,text,text_buffer,scene_visible,id):
        self.pos = pos
        self.pos2 = pos2
        self.idle = idle
        self.color = self.idle
        self.hovered = hovered
        self.clicked = clicked
        self.font = font
        self.text = text
        self.text_buffer = text_buffer
        self.scene_visible = scene_visible
        self.id = id

def add_button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible):
    global button_ID
    id = button_ID
    button_list.append(Button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible,id))
    button_ID += 1

def buttoncollsion(i):
    global recalculate, create_playlist
    cur_button = button_list[i]
    if input.mouse_position[0] < cur_button.pos[0]+cur_button.pos2[0] and input.mouse_position[0] > cur_button.pos[0] and input.mouse_position[1] < cur_button.pos[1]+cur_button.pos2[1] and input.mouse_position[1] > cur_button.pos[1]:
        cur_button.color = cur_button.hovered
        if input.find_mouse_button("left_click").just_pressed == 1:
            global curScene
            cur_button.color = cur_button.clicked
            if cur_button.id == 0:
                textInput = textInput_list[0]
                url = textInput.text
                thread = threading.Thread(target=grabber.attempt_download,args=(url,))
                thread.start()
                #grabber.attempt_download(url)
            elif cur_button.id == 1:
                curScene = 1
            elif cur_button.id == 2:
                curScene = 2
                input.mouse_scroll_value = 0
                recalculate = True
            elif cur_button.id == 3:
                curScene = 3
                input.mouse_scroll_value = 0
                recalculate = True
            elif cur_button.id == 4:
                create_playlist = True
    else:
        cur_button.color = cur_button.idle

def button_tick():
    for i in range(len(button_list)):
        cur_button = button_list[i]
        if cur_button.scene_visible == 0 or cur_button.scene_visible == curScene:
            if cur_button.id == 0:
                if player.song_name != '':
                    cur_button.pos[0] = screen_setup.screen_width-160
                else:
                    cur_button.pos[0] = screen_setup.center_x-75
                player.max_width = cur_button.pos[0]-110
            #button logic
            buttoncollsion(i)
            #draw button
            cur_button.hovered = button_hovered
            pygame.draw.rect(screen_setup.screen,cur_button.color,(cur_button.pos,cur_button.pos2),0)
            #draw text
            draw_text(cur_button.text,cur_button.font,text_color,(cur_button.pos[0]+cur_button.text_buffer[0],cur_button.pos[1]+cur_button.text_buffer[1]))

# Buttons
texture_button_list = []

texture_button_ID = 0

texture_button_reset = False

last_press = 0

class texture_Button:
    def __init__(self,pos,pos2,idle,hovered,clicked,font,text,text_buffer,scene_visible,id,img,img_buffer,rounded):
        self.pos = pos
        self.orginal_pos = [pos[0],pos[1]]
        self.pos2 = pos2
        self.orginal_pos2 = [pos2[0],pos2[1]]
        self.idle = idle
        self.color = self.idle
        self.hovered = hovered
        self.clicked = clicked
        self.font = font
        self.text = text
        self.text_buffer = text_buffer
        self.scene_visible = scene_visible
        self.id = id
        self.img = img
        self.img_buffer = img_buffer
        self.orginal_buffer = [img_buffer[0],img_buffer[1]]
        self.rounded = rounded

def add_texture_button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible,img,img_buffer,rounded):
    global texture_button_ID
    id = texture_button_ID
    texture_button_list.append(texture_Button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible,id,img,img_buffer,rounded))
    texture_button_ID += 1

def shuffle_song(dir):
    global texture_button_reset, song_selected, song_selected_list, song_selected_length, texture_button_reset, last_press, new_shuffle_list
    if player.is_shuffle == True:
        if player.is_playing == True:
            player.stop_song()
        if len(songbox_list) != 1:
            if player.shuffle_version == 'default':
                rand = randrange(0,len(songbox_list))
                if rand == player.song_index:
                    rand = randrange(0,len(songbox_list))
                if rand == player.song_index:
                    rand = randrange(0,len(songbox_list))
                cur_songbox = songbox_list[rand]
            else:
                rand = 0
                if len(new_shuffle_list) > 1:
                    rand_temp = randrange(0,len(new_shuffle_list))
                    rand = new_shuffle_list[rand_temp]
                    new_shuffle_list.pop(rand_temp)
                elif len(new_shuffle_list) == 1:
                    rand = new_shuffle_list[0]
                    new_shuffle_list.pop(0)
                    for t in range(len(songbox_list)):
                        new_shuffle_list.append(t)
                else:
                    new_shuffle_list = []
                    for t in range(len(songbox_list)):
                        new_shuffle_list.append(t)
                cur_songbox = songbox_list[rand]
        else:
            rand = 0
            cur_songbox = songbox_list[rand]
        if player.song_name != cur_songbox.song_name  or len(songbox_list) == 1:
            player.song_name = cur_songbox.song_name
            player.song_length = floor(cur_songbox.length_in_seconds)
            player.song_index = rand
            player.song_time_elapsed = 0.0
            player.set_paths(cur_songbox.img_path,cur_songbox.song)
            player.play_song()
            player.pick_new_song = False
            remove_songbox_selected()
            song_selected = rand
            texture_button_reset = True
    elif player.is_shuffle == False:
        if player.is_playing == True:
            player.stop_song()
        temp = song_selected + dir
        if temp >= len(songbox_list):
            temp = 0
        if temp < 0:
            temp = len(songbox_list)-1
        song_selected = temp
        cur_songbox = songbox_list[temp]
        player.song_name = cur_songbox.song_name
        player.song_length = floor(cur_songbox.length_in_seconds)
        player.song_index = temp
        player.song_time_elapsed = 0.0
        player.set_paths(cur_songbox.img_path,cur_songbox.song)
        player.play_song()
        texture_button_reset = True

def skip_foward():
    global texture_button_reset, song_selected, song_selected_list, song_selected_length, song_selected_pos, texture_button_reset, last_press
    if len(songbox_list) > 0:
        if (song_selected_pos < len(song_selected_list)-1) != True or player.is_shuffle == False:
            shuffle_song(1)
        if player.is_shuffle == True:
            if song_selected_pos < len(song_selected_list)-1:
                song_selected_pos = clamp(song_selected_pos+1,0,song_selected_length-1)
                if player.is_playing == True:
                    player.stop_song()
                temp = song_selected_list[song_selected_pos]
                song_selected = temp
                cur_songbox = songbox_list[temp]
                player.song_name = cur_songbox.song_name
                player.song_length = floor(cur_songbox.length_in_seconds)
                player.song_index = temp
                player.song_time_elapsed = 0.0
                player.set_paths(cur_songbox.img_path,cur_songbox.song)
                player.play_song()
                texture_button_reset = True
            else:
                if (song_selected_pos + 1) > len(song_selected_list):
                    song_selected_list.insert(len(song_selected_list),song_selected)
                    if len(song_selected_list) > song_selected_length:
                        song_selected_list.pop(0)
                else:
                    song_selected_pos = clamp(song_selected_pos+1,0,song_selected_length-1)
                    song_selected_list.insert(len(song_selected_list),song_selected)
                    if len(song_selected_list) > song_selected_length:
                        song_selected_list.pop(0)
        last_press = 1

def skip_backwards():
    global texture_button_reset, song_selected, song_selected_list, song_selected_length, song_selected_pos, texture_button_reset, last_press
    if len(songbox_list) > 0:
        if song_selected_pos == 0 or player.is_shuffle == False:
            shuffle_song(-1)
        if player.is_shuffle == True:
            if song_selected_pos > 0:
                song_selected_pos = clamp(song_selected_pos-1,0,song_selected_length-1)
                if player.is_playing == True:
                    player.stop_song()
                temp = song_selected_list[song_selected_pos]
                song_selected = temp
                cur_songbox = songbox_list[temp]
                player.song_name = cur_songbox.song_name
                player.song_length = floor(cur_songbox.length_in_seconds)
                player.song_index = temp
                player.song_time_elapsed = 0.0
                player.set_paths(cur_songbox.img_path,cur_songbox.song)
                player.play_song()
                texture_button_reset = True
            else:
                if (song_selected_pos - 1) < len(song_selected_list):
                    song_selected_list.insert(0,song_selected)
                    if len(song_selected_list) > song_selected_length:
                        song_selected_list.pop(len(song_selected_list)-1)
                else:
                    song_selected_pos = clamp(song_selected_pos-1,0,song_selected_length-1)
                    song_selected_list.insert(0,song_selected)
                    if len(song_selected_list) > song_selected_length:
                        song_selected_list.pop(len(song_selected_list)-1)
        last_press = -1

def texture_buttoncollsion(i):
    global texture_button_reset, song_selected, song_selected_list, song_selected_length, texture_button_reset, last_press
    cur_button = texture_button_list[i]
    cur_button.pos[1] = cur_button.orginal_pos[1]
    cur_button.pos[0] = cur_button.orginal_pos[0]
    cur_button.pos2[1] = cur_button.orginal_pos2[1]
    cur_button.pos2[0] = cur_button.orginal_pos2[0]
    cur_button.img_buffer[1] = cur_button.orginal_buffer[1]
    cur_button.img_buffer[0] = cur_button.orginal_buffer[0]
    if input.mouse_position[0] < cur_button.pos[0]+cur_button.pos2[0] and input.mouse_position[0] > cur_button.pos[0] and input.mouse_position[1] < cur_button.pos[1]+cur_button.pos2[1] and input.mouse_position[1] > cur_button.pos[1]:
        cur_button.color = cur_button.hovered
        cur_button.pos[0] -= 2
        cur_button.pos[1] -= 2
        cur_button.pos2[0] += 4
        cur_button.pos2[1] += 4
        cur_button.img_buffer[0] += 2
        cur_button.img_buffer[1] += 2
        if input.find_mouse_button("left_click").just_pressed == 1:
            global curScene
            cur_button.color = cur_button.clicked
            if cur_button.id == 0:
                if len(songbox_list) > 0:
                    cur_songbox = songbox_list[song_selected]
                    if player.is_playing == False and player.song_time_elapsed_in_seconds == 0:
                        if player.song_path != '':
                            player.song_name = cur_songbox.song_name
                            player.song_length = floor(cur_songbox.length_in_seconds)
                            player.song_index = song_selected
                            player.song_time_elapsed = 0.0
                            player.set_paths(cur_songbox.img_path,cur_songbox.song)
                            player.play_song()
                            texture_button_reset = True
                        else:
                            if player.is_playing == True:
                                player.stop_song()
                            if len(songbox_list) != 1:
                                if player.shuffle_version == 'default':
                                    rand = randrange(0,len(songbox_list))
                                    if rand == player.song_index:
                                        rand = randrange(0,len(songbox_list))
                                    if rand == player.song_index:
                                        rand = randrange(0,len(songbox_list))
                                    cur_songbox = songbox_list[rand]
                                else:
                                    rand = 0
                                    if len(new_shuffle_list) > 1:
                                        rand_temp = randrange(0,len(new_shuffle_list))
                                        rand = new_shuffle_list[rand_temp]
                                        new_shuffle_list.pop(rand_temp)
                                    elif len(new_shuffle_list) == 1:
                                        rand = new_shuffle_list[0]
                                        new_shuffle_list.pop(0)
                                        for t in range(len(songbox_list)):
                                            new_shuffle_list.append(t)
                                    else:
                                        for t in range(len(songbox_list)):
                                            new_shuffle_list.append(t)
                                    cur_songbox = songbox_list[rand]
                            else:
                                rand = 0
                                cur_songbox = songbox_list[rand]
                            cur_songbox = songbox_list[rand]
                            if player.song_name != cur_songbox.song_name:
                                player.song_name = cur_songbox.song_name
                                player.song_length = floor(cur_songbox.length_in_seconds)
                                player.song_index = rand
                                player.song_time_elapsed = 0.0
                                player.set_paths(cur_songbox.img_path,cur_songbox.song)
                                player.play_song()
                                player.pick_new_song = False
                                remove_songbox_selected()
                                song_selected = rand
                                texture_button_reset = True
                    elif player.is_playing == True:
                        if player.is_paused == False:
                            player.pause_song()
                            cur_button.text = 'Unpause'
                            cur_button.img = pygame.image.load('user_data/default_files/play.png').convert_alpha()
                            cur_button.img_buffer = [0,1]
                        elif player.is_paused == True:
                            player.unpause_song()
                            cur_button.text = 'Pause'
                            cur_button.img = pygame.image.load('user_data/default_files/pause.png').convert_alpha()
                            cur_button.img_buffer = [-0.5,1]
            elif cur_button.id == 1:
                skip_foward()
            elif cur_button.id == 2:
                skip_backwards()
    else:
        cur_button.color = cur_button.idle

def texture_button_tick():
    global texture_button_reset
    for i in range(len(texture_button_list)):
        cur_button = texture_button_list[i]
        if cur_button.scene_visible == 0 or cur_button.scene_visible == curScene:
            #button logic
            cur_button.idle = button_hovered
            texture_buttoncollsion(i)
            if cur_button.id == 0:
                #check 1
                if player.is_playing == False and player.song_time_elapsed_in_seconds == 0:
                    cur_button.text = 'Play'
                    cur_button.img = pygame.image.load('user_data/default_files/play.png').convert_alpha()
                    cur_button.img_buffer = [0,1]
                    cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                    cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
                #check 2
                if texture_button_reset == True:
                    cur_button.text = 'Pause'
                    cur_button.img = pygame.image.load('user_data/default_files/pause.png').convert_alpha()
                    cur_button.img_buffer = [-0.5,1]
                    cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                    cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
                    texture_button_reset = False
                #check 3
                if player.is_playing and player.is_paused and player.song_time_elapsed_in_seconds == 0:
                    cur_button.text = 'Play'
                    cur_button.img = pygame.image.load('user_data/default_files/play.png').convert_alpha()
                    cur_button.img_buffer = [0,1]
                    cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                    cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
                #check 4
                if input.texture_update:
                    input.texture_update = False
                    if player.is_playing:
                        if player.is_paused == False:
                            cur_button.text = 'Pause'
                            cur_button.img = pygame.image.load('user_data/default_files/pause.png').convert_alpha()
                            cur_button.img_buffer = [-0.5,1]
                            cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                            cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
                        else:
                            cur_button.text = 'Play'
                            cur_button.img = pygame.image.load('user_data/default_files/play.png').convert_alpha()
                            cur_button.img_buffer = [0,1]
                            cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                            cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
                    else:
                        cur_button.text = 'Pause'
                        cur_button.img = pygame.image.load('user_data/default_files/pause.png').convert_alpha()
                        cur_button.img_buffer = [-0.5,1]
                        cur_button.orginal_buffer[1] = cur_button.img_buffer[1]
                        cur_button.orginal_buffer[0] = cur_button.img_buffer[0]
            elif cur_button.id == 2:
                player.max_width = cur_button.pos[0]-110
            #draw button
            pygame.draw.rect(screen_setup.screen,cur_button.color,(cur_button.pos,cur_button.pos2),0,cur_button.rounded)
            screen_setup.screen.blit(cur_button.img,(cur_button.pos[0]+cur_button.img_buffer[0],cur_button.pos[1]+cur_button.img_buffer[1]))
            #draw text
            if input.mouse_position[0] < cur_button.pos[0]+cur_button.pos2[0] and input.mouse_position[0] > cur_button.pos[0] and input.mouse_position[1] < cur_button.pos[1]+cur_button.pos2[1] and input.mouse_position[1] > cur_button.pos[1]:
                draw_text(cur_button.text,cur_button.font,text_color,(cur_button.pos[0]+cur_button.text_buffer[0],cur_button.pos[1]+cur_button.text_buffer[1]))

# Text Variables
small_text_font = pygame.font.Font('user_data/default_files/ARIAL.TTF',15)
title_text_font = pygame.font.Font('user_data/default_files/ARIAL.TTF',22)
medium_text_font = pygame.font.Font('user_data/default_files/ARIAL.TTF',30)
large_text_font = pygame.font.Font('user_data/default_files/ARIAL.TTF',45)
text_color = (246,250,240)

def draw_text(text,font,text_color,pos):
    img = font.render(text,True,text_color)
    #img = pygame.transform.rotate(img, 90)
    screen_setup.screen.blit(img,pos)

# Visual blocks to seperate elements
block_list = []

class Block:
    def __init__(self,pos,pos2,color,scene_visible):
        self.pos = pos
        self.pos2 = pos2
        self.color = color
        self.scene_visible = scene_visible

def add_block(pos,pos2,color,scene_visible):
    block_list.append(Block(pos,pos2,color,scene_visible))

def block_tick():
    for i in range(len(block_list)):
        cur_block = block_list[i]
        if curScene == cur_block.scene_visible or cur_block.scene_visible == 0:
            pygame.draw.rect(screen_setup.screen,cur_block.color,(cur_block.pos,cur_block.pos2),0)

# Slider
slider_list = []

slider_ID = 0

slider_unpause = False
paused = False

class Slider:
    def __init__(self,pos,pos2,rad,box_color,circle_color,circle_selected,max_value,min_value,id,font,label,label_pos,scene_visible):
        self.pos = pos
        self.pos2 = pos2
        self.rad = rad
        self.box_color = box_color
        self.circle_pos = [pos[0],pos[1]+(pos2[1]/2)]
        self.value = 0
        self.circle_color = circle_color
        self.circle_selected = circle_selected
        self.max_value = max_value
        self.min_value = min_value
        self.id = id
        self.font = font
        self.label = label
        self.label_pos = label_pos
        self.scene_visible = scene_visible

def add_slider(pos,pos2,rad,box_color,circle_color,circle_selected,max_value,min_value,font,label,label_pos,scene_visible):
    global slider_ID
    id = slider_ID
    slider_list.append(Slider(pos,pos2,rad,box_color,circle_color,circle_selected,max_value,min_value,id,font,label,label_pos,scene_visible))
    slider_ID += 1

def slider_tick():
    global volume, slider_unpause, paused

    for i in range(len(slider_list)):
        cur_slider = slider_list[i]
        if cur_slider.scene_visible == curScene or cur_slider.scene_visible == 0:
            
            pygame.draw.rect(screen_setup.screen,cur_slider.box_color,(cur_slider.pos,cur_slider.pos2),0,10)
    
            dist = sqrt(((cur_slider.circle_pos[0]-input.mouse_position[0])**2)+((cur_slider.circle_pos[1]-input.mouse_position[1])**2))
    
            draw_text(cur_slider.label,cur_slider.font,text_color,[cur_slider.pos[0]+cur_slider.label_pos[0],cur_slider.pos[1]+cur_slider.label_pos[1]])
    
            if input.mouse_position[0] > cur_slider.pos[0] and input.mouse_position[0] < cur_slider.pos[0] + cur_slider.pos2[0] and input.mouse_position[1] > cur_slider.pos[1] and input.mouse_position[1] < cur_slider.pos[1] + cur_slider.pos2[1] and input.find_mouse_button("left_click").pressed == True:
                cur_slider.circle_pos[0] = input.mouse_position[0]
    
            if dist < cur_slider.rad * 1.25:
                cur_color = cur_slider.circle_selected
                if input.find_mouse_button("left_click").just_pressed == True:
                    cur_slider.circle_pos[0] = input.mouse_position[0]
                if cur_slider.circle_pos[0] < cur_slider.pos[0]:
                    cur_slider.circle_pos[0] = cur_slider.pos[0]
                elif cur_slider.circle_pos[0] > cur_slider.pos[0] + cur_slider.pos2[0]:
                    cur_slider.circle_pos[0] = cur_slider.pos[0] + cur_slider.pos2[0]
            else:
                cur_color = cur_slider.circle_color

            pygame.draw.circle(screen_setup.screen,cur_color,cur_slider.circle_pos,cur_slider.rad)

            max_val = abs(cur_slider.max_value) + abs(cur_slider.min_value)
            steps = max_val / cur_slider.pos2[0]
            cur_slider.value = cur_slider.min_value
            cur_slider.value = cur_slider.value + ((cur_slider.circle_pos[0]-cur_slider.pos[0])*steps)
            #cur_slider.value = floor(cur_slider.value)
            if cur_slider.id == 0:
                volume = cur_slider.value
                if mute == False:
                    player.set_volume(volume)
                else:
                    player.set_volume(0)
            elif cur_slider.id == 1:
                if player.song_path != '' and input.find_mouse_button("left_click").pressed == False:
                    cur_slider.max_value = player.song_length
                    cur_slider.min_value = 0
                    steps = max_val / cur_slider.pos2[0]
                    cur_slider.circle_pos[0] = cur_slider.pos[0] + (player.song_time_elapsed_in_seconds / steps)
                elif input.mouse_position[0] > cur_slider.pos[0] and input.mouse_position[0] < cur_slider.pos[0] + cur_slider.pos2[0] and input.mouse_position[1] > cur_slider.pos[1] and input.mouse_position[1] < cur_slider.pos[1] + cur_slider.pos2[1] and input.find_mouse_button("left_click").pressed == True:
                    if player.song_path != '':
                        cur_slider.circle_pos[0] = input.mouse_position[0]
                        if cur_slider.circle_pos[0] < cur_slider.pos[0]:
                            cur_slider.circle_pos[0] = cur_slider.pos[0]
                        elif cur_slider.circle_pos[0] > cur_slider.pos[0] + cur_slider.pos2[0]:
                            cur_slider.circle_pos[0] = cur_slider.pos[0] + cur_slider.pos2[0]
                        max_val = abs(cur_slider.max_value) + abs(cur_slider.min_value)
                        steps = max_val / cur_slider.pos2[0]
                        cur_slider.value = cur_slider.min_value
                        cur_slider.value = cur_slider.value + ((cur_slider.circle_pos[0]-cur_slider.pos[0])*steps)
                        cur_slider.value = floor(cur_slider.value)
                        player.song_time_elapsed = cur_slider.value
                        if slider_unpause == False:
                            if player.is_paused == True:
                                paused = True
                            elif player.is_paused == False:
                                paused = False
                            player.change_time(cur_slider.value)
                        player.pause_song()
                        slider_unpause = True
                if player.song_path != '':
                    length = player.song_length - player.song_time_elapsed_in_seconds
                    minutes = int(length // 60)
                    seconds = int(length % 60)
                    if seconds > 9:
                        cur_slider.label = str(minutes) + ':' + str(seconds)
                    else:
                        cur_slider.label = str(minutes) + ':0' + str(seconds)
                else:
                    cur_slider.label = '0:00'
            elif cur_slider.id == 2:
                pass
    
    if slider_unpause == True and input.find_mouse_button('left_click').pressed == False:
        for i in range(len(slider_list)):
            cur_slider = slider_list[i]
            if cur_slider.id == 1:
                player.unpause_song()
                player.change_time(cur_slider.value)
                if paused:
                    player.pause_song()
                slider_unpause = False
                paused = False

# Checkbox
checkbox_list = []

checkbox_ID = 0

mute = False
edit_playlists = False

class Checkbox:
    def __init__(self,pos,pos2,idle,hovered,selected,font,label,label_pos,id,scene_visible):
        self.pos = pos
        self.pos2 = pos2
        self.idle = idle
        self.hovered = hovered
        self.selected = selected
        self.font = font
        self.label = label
        self.label_pos = label_pos
        self.scene_visible = scene_visible
        self.id = id
        self.checked = 0
        self.h = False

def add_checkbox(pos,pos2,idle,hovered,selected,font,label,label_pos,scene_visible):
    global checkbox_ID
    id = checkbox_ID
    checkbox_list.append(Checkbox(pos,pos2,idle,hovered,selected,font,label,label_pos,id,scene_visible))
    checkbox_ID += 1

def load_playlist_checked():
    global playlist_path
    if playlist_path != '':
        song_file = open(playlist_path+'/playlist_data.txt','r')
        song_string = song_file.read()
        song_list = str(song_string).split(',')
        if song_list[0] == '':
            song_list.pop(0)
        for i in range(len(songbox_list)):
            cur_songbox = songbox_list[i]
            if cur_songbox.song_name in song_list:
                cur_songbox.playlist_clicked = True

def load_playlist():
    global playlist_path, playlist_songs
    playlist_songs = []
    if playlist_path != '':
        song_file = open(playlist_path+'/playlist_data.txt','r')
        song_string = song_file.read()
        song_list = str(song_string).split(',')
        if song_list[0] == '':
            song_list.pop(0)
        playlist_songs = song_list
        song_file.close()
        for song in playlist_songs:
            found_song = False
            for songbox in songbox_list:
                if songbox.song_name == song:
                    found_song = True
            if found_song == False:
                playlist_songs.remove(song)
                file_data = open(playlist_path+'/playlist_data.txt','w')
                temp_string = ''
                for song_name in playlist_songs:
                    temp_string = temp_string+','+str(song_name)
                file_data.write(temp_string)
                file_data.close()

def checkbox_tick():
    global mute, song_selected_list, song_selected_pos, edit_playlists, playlist_changed
    for i in range(len(checkbox_list)):
        cur_checkbox = checkbox_list[i]
        if cur_checkbox.scene_visible == curScene or cur_checkbox.scene_visible == 0:
            cur_checkbox.h = False
            if input.mouse_position[0] > cur_checkbox.pos[0] and input.mouse_position[0] < cur_checkbox.pos[0] + cur_checkbox.pos2[0] and input.mouse_position[1] > cur_checkbox.pos[1] and input.mouse_position[1] < cur_checkbox.pos[1] + cur_checkbox.pos2[1]:
                cur_checkbox.h = True
                if input.find_mouse_button('left_click').just_pressed == True:
                    if cur_checkbox.checked == 0:
                        cur_checkbox.checked = 1
                    else:
                        cur_checkbox.checked = 0
                    if cur_checkbox.id == 1:
                        song_selected_list = []
                        song_selected_pos = 0
                    if cur_checkbox.id == 3:
                        song_selected_list = []
                        song_selected_pos = 0
                        playlist_changed = True

            if cur_checkbox.checked == 0:
                if cur_checkbox.h == False:
                    cur_color = cur_checkbox.idle
                else:
                    cur_color = cur_checkbox.hovered
            else:
                cur_color = cur_checkbox.selected

            draw_text(cur_checkbox.label,cur_checkbox.font,text_color,(cur_checkbox.pos[0]+cur_checkbox.label_pos[0],cur_checkbox.pos[1]+cur_checkbox.label_pos[1]))

            cur_checkbox.selected = button_hovered
            pygame.draw.rect(screen_setup.screen,cur_color,(cur_checkbox.pos[0],cur_checkbox.pos[1],cur_checkbox.pos2[0],cur_checkbox.pos2[1]))

            if cur_checkbox.id == 0:
                if cur_checkbox.checked == 0:
                    player.is_repeating = False
                elif cur_checkbox.checked == 1:
                    player.is_repeating = True
                    player.is_shuffle = False
                    checkbox_list[1].checked = 0
            elif cur_checkbox.id == 1:
                if cur_checkbox.checked == 0:
                    player.is_shuffle = False
                elif cur_checkbox.checked == 1:
                    player.is_shuffle = True
                    player.is_repeating = False
                    checkbox_list[0].checked = 0
            elif cur_checkbox.id == 2:
                if cur_checkbox.checked == 0:
                    mute = False
                elif cur_checkbox.checked == 1:
                    mute = True
            elif cur_checkbox.id == 3:
                if cur_checkbox.checked == 0:
                    edit_playlists = False
                elif cur_checkbox.checked == 1:
                    if playlist_selected != -1:
                        edit_playlists = True
                    else:
                        cur_checkbox.checked = 0
                    
# Text Input
textInput_list = []

searching = False

class TextInput:
    def __init__(self,pos,pos2,color,text_empty,text_empty_color,text_font,text_color,text,text_buffer,scene_visible):
        self.pos = pos
        self.pos2 = pos2
        self.color = color
        self.text_empty = text_empty
        self.text_empty_color = text_empty_color
        self.text_font = text_font
        self.text_color = text_color
        self.text = text
        self.text_buffer = text_buffer
        self.active = 0
        self.scene_visible = scene_visible
        self.backspace_wait = 0
        self.blinker_wait = 0
        self.is_typing = False

def add_textInput(pos,pos2,color,text_empty,text_empty_color,text_font,text_color,text,text_buffer,scene_visible):
    textInput_list.append(TextInput(pos,pos2,color,text_empty,text_empty_color,text_font,text_color,text,text_buffer,scene_visible))

def textInputCollision(i):
    cur_textInput = textInput_list[i]
    if input.mouse_position[0] < cur_textInput.pos[0]+cur_textInput.pos2[0] and input.mouse_position[0] > cur_textInput.pos[0] and input.mouse_position[1] < cur_textInput.pos[1]+cur_textInput.pos2[1] and input.mouse_position[1] > cur_textInput.pos[1]:
        if input.find_mouse_button("left_click").just_pressed == 1:
            cur_textInput.active = 1
    else:
        if input.find_mouse_button("left_click").just_pressed == 1:
            cur_textInput.active = 0

def get_text_segments(text,font,text_color,textbox_width,text_buffer):
    textbox_width -= text_buffer[0]*2
    is_bar = False
    if '|' in text:
        if text == '|':
            return ['|']
        else:
            text = str(text).replace('|','')
            is_bar = True
    if text != '':
        img = font.render(text,True,text_color)
        img_width = img.get_width()
        number_of_letters = len(str(text))
        average_letter_width = img_width/number_of_letters
        text_list = []
        temp_text = str(text)
        max_letters = floor(textbox_width/average_letter_width)
        for i in range(100):
            if (len(temp_text)*average_letter_width) > (textbox_width):
                temp_string = temp_text[:max_letters]
                no_spaces = False
                for t in range(len(temp_string)+1):
                    if temp_string != '':
                        temp_letter = temp_string[-1]
                    else:
                        temp_string = temp_text[:max_letters]
                        no_spaces = True
                        break
                    if temp_letter != ' ':
                        temp_string = temp_string[:-1]
                    else:
                        break
                text_list.append(temp_string)
                if no_spaces:
                    temp_text = temp_text[t:]
                else:
                    temp_text = temp_text.replace(temp_string,"")
            else:
                if temp_text != '':
                    text_list.append(temp_text)
                if is_bar:
                    text_list[len(text_list)-1] = text_list[len(text_list)-1]+'|'
                return text_list  

def textInput_tick():
    global searching, song_selected_list, song_selected_pos
    for i in range(len(textInput_list)):
        cur_textInput = textInput_list[i]
        #print(cur_textInput.active)
        if cur_textInput.scene_visible == curScene:
            #textbox logic
            textInputCollision(i)
            #draw textbox
            if i == 2:
                player.max_width = cur_textInput.pos[0]-110
            if i == 0:
                pygame.draw.rect(screen_setup.screen,cur_textInput.color,(cur_textInput.pos,cur_textInput.pos2),0,10)
            else:
                pygame.draw.rect(screen_setup.screen,cur_textInput.color,(cur_textInput.pos,cur_textInput.pos2),0,2)
            if cur_textInput.active == 0:

                cur_textInput.is_typing = False

                if '|' in cur_textInput.text:
                    cur_textInput.text = str(cur_textInput.text).replace('|','')

                if cur_textInput.text == "":
                    draw_text(cur_textInput.text_empty,cur_textInput.text_font,cur_textInput.text_empty_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]))
                else:
                    text_list = get_text_segments(cur_textInput.text,cur_textInput.text_font,cur_textInput.text_empty_color,cur_textInput.pos2[0],cur_textInput.text_buffer)
                    y = 0
                    try:
                        for text in text_list:
                            draw_text(text,cur_textInput.text_font,cur_textInput.text_empty_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]+y))
                            y += 20
                    except:
                        pass
            else:
                
                cur_textInput.is_typing = True

                if cur_textInput.blinker_wait <= 0:
                    cur_textInput.blinker_wait = 35
                    if '|' in cur_textInput.text:
                        cur_textInput.text = str(cur_textInput.text).replace('|','')
                    else:
                        cur_textInput.text += '|'
                
                if cur_textInput.blinker_wait > 0:
                    cur_textInput.blinker_wait -= 1

                if input.find_key("backspace").just_pressed == True:
                    if '|' in cur_textInput.text:
                            cur_textInput.text = str(cur_textInput.text).replace('|','')
                            cur_textInput.text = cur_textInput.text[:-1]
                            cur_textInput.text += '|'
                    else:
                        cur_textInput.text = cur_textInput.text[:-1]
                    cur_textInput.backspace_wait = -25

                if input.find_key("backspace").pressed == True and cur_textInput.backspace_wait == 0:
                    if '|' in cur_textInput.text:
                            cur_textInput.text = str(cur_textInput.text).replace('|','')
                            cur_textInput.text = cur_textInput.text[:-1]
                            cur_textInput.text += '|'
                    else:
                        cur_textInput.text = cur_textInput.text[:-1]
                    cur_textInput.backspace_wait = 1
                
                if cur_textInput.backspace_wait < 0:
                    cur_textInput.backspace_wait += 1

                if cur_textInput.backspace_wait > 0:
                    cur_textInput.backspace_wait += 1

                if cur_textInput.backspace_wait > 1:
                    cur_textInput.backspace_wait = 0

                if input.find_key("delete").just_pressed == True:
                    cur_textInput.text = ""
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    if keys[pygame.K_v]:
                        cur_textInput.text = ""
                        try:
                            cur_textInput.text = pygame.scrap.get_text()
                        except:
                            cur_textInput.text = 'NOT VALID COPY'
                if input.find_key('enter').just_pressed and i == 1 and searching == False:
                    searching = True
                    song_selected_list = []
                    song_selected_pos = 0

                text_list = get_text_segments(cur_textInput.text,cur_textInput.text_font,cur_textInput.text_color,cur_textInput.pos2[0],cur_textInput.text_buffer)
                y = 0
                no_clipping_text = ''
                try:
                    for text in text_list:
                        draw_text(text,cur_textInput.text_font,cur_textInput.text_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]+y))
                        y += 20
                        if (cur_textInput.pos[1] + cur_textInput.text_buffer[1] + y) > ((cur_textInput.pos[1] + cur_textInput.pos2[1])):# - cur_textInput.text_buffer[1]):
                            no_clipping_text = no_clipping_text+str(text)
                    if no_clipping_text != '':
                        cur_textInput.text = str(cur_textInput.text)[:-len(no_clipping_text)]
                except:
                    pass
                #print(new_text)

def hud_event(event):
    for i in range(len(textInput_list)):
        cur_textInput = textInput_list[i]
        if cur_textInput.is_typing:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()

            if event.type == pygame.TEXTINPUT:
                if event.text != '|':
                    cur_textInput.text += event.text
                    if '|' in cur_textInput.text:
                        cur_textInput.text = str(cur_textInput.text).replace('|','')
                        cur_textInput.text += '|'


# song box stuff
songbox_list = []

song_selected = -1
song_selected_name = ''
old_song_selected = -1
old_song_name = ''
temp_name = ''

song_selected_list = []
song_selected_length = 5
song_selected_pos = 0

max_string_length = 39

garbage_img = ''

class songbox:
    def __init__(self,pos,pos2,color,hovered_color,img_path,img,img_buffer,song_name,name_surface,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path):
        self.pos = pos
        self.real_pos = [0,0]
        self.pos2 = pos2
        self.color = color
        self.hovered_color = hovered_color
        self.img_path = img_path
        self.img = img
        self.img_buffer = img_buffer
        self.name_surface = name_surface
        self.song_name = song_name
        self.song_length = song_length
        self.name_buffer = name_buffer
        self.length_buffer = length_buffer
        self.scene_visible = scene_visible
        self.song = song
        self.length_in_seconds = length_in_seconds
        self.folder_path = folder_path
        self.selected = False
        self.hovered = False
        self.delete = False
        self.playlist_clicked = False

def add_songbox(pos,pos2,color,hovered_color,img_path,img,img_buffer,song_name,name_surface,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path):
    songbox_list.append(songbox(pos,pos2,color,hovered_color,img_path,img,img_buffer,song_name,name_surface,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path))

def remove_songbox_selected():
    global song_selected
    song_selected = -1

def songbox_collision(index):
    global song_selected, texture_button_reset, playlist_songs, playlist_path, playlist_changed
    cur_songbox = songbox_list[index]
    cur_songbox.delete = False
    pos = [(cur_songbox.pos[0]+cur_songbox.pos2[0])-32.5,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-32.5]
    pos2 = [30,30]
    if input.mouse_position[0] < pos[0]+pos2[0] and input.mouse_position[0] > pos[0] and input.mouse_position[1] < pos[1]+pos2[1] and input.mouse_position[1] > pos[1] and input.mouse_position[1] < screen_setup.screen_height-80 and input.mouse_position[1] > 40:
        cur_songbox.hovered = True
        if edit_playlists == False:
            if input.find_key("shift").pressed:
                cur_songbox.delete = True
            if input.find_mouse_button("left_click").just_pressed:
                if cur_songbox.delete == False:
                    cur_songbox.selected = True
                    if song_selected != index:
                        remove_songbox_selected()
                        song_selected = index
                        if player.song_name != cur_songbox.song_name:
                            player.song_name = cur_songbox.song_name
                            player.song_length = floor(cur_songbox.length_in_seconds)
                            player.song_index = song_selected
                            player.song_time_elapsed = 0.0
                            player.set_paths(cur_songbox.img_path,cur_songbox.song)
                            player.play_song()
                            texture_button_reset = True
                    else:
                        remove_songbox_selected()
                elif player.song_path != cur_songbox.song:
                    remove(cur_songbox.img_path)
                    remove(cur_songbox.song)
                    Path.rmdir(cur_songbox.folder_path)
                    grabber.update_songbox = True
                    if playlist_path != '':
                        playlist_changed = True
                        load_playlist()
                        load_playlist_checked()
        elif input.find_mouse_button("left_click").just_pressed:
            if cur_songbox.playlist_clicked:
                cur_songbox.playlist_clicked = False
                if cur_songbox.song_name in playlist_songs:
                    playlist_songs.remove(cur_songbox.song_name)
            else:
                cur_songbox.playlist_clicked = True
                if cur_songbox.song_name not in playlist_songs:
                    playlist_songs.append(cur_songbox.song_name)
            file_data = open(playlist_path+'/playlist_data.txt','w')
            temp_string = ''
            for song_name in playlist_songs:
                temp_string = temp_string+','+str(song_name)
            file_data.write(temp_string)
    else:
        cur_songbox.hovered = False

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

def clamp(input, min, max):
    if input < min:
        return min
    elif input > max:
        return max
    else:
        return input

file_read = []

def songbox_tick(arg=0):
    global curScene, max_string_length, song_selected, temp_name, searching, recalculate, garbage_img
    for i in range(len(songbox_list)):
        cur_songbox = songbox_list[i]

        if arg == 1:
            changed = False
            if player.song_name != '':
                for t in range(len(songbox_list)):
                    c_s = songbox_list[t]
                    if player.song_name == c_s.song_name:
                        song_selected = t
                        changed = True
            if changed == False:
                song_selected = -1

        if i == len(songbox_list) - 1:
            max_view_height = screen_setup.screen_height-120
            if (input.max_scroll_value != cur_songbox.pos[1]-max_view_height and input.max_scroll_value != 0 and curScene == 2) or searching or (recalculate and curScene == 2):
                difference = cur_songbox.pos[1]-max_view_height
                input.max_scroll_value = difference
                temp = floor(difference/40)
                input.mouse_scroll_sens = clamp(temp,20,60)
                recalculate = False
            elif cur_songbox.pos[1] < max_view_height and curScene == 2:
                input.max_scroll_value = 0

        if curScene == cur_songbox.scene_visible or cur_songbox.scene_visible == 0:
            cur_songbox.real_pos[0] = cur_songbox.pos[0]
            cur_songbox.real_pos[1] = cur_songbox.pos[1] - input.mouse_scroll_value
            
            if cur_songbox.real_pos[1] + cur_songbox.pos2[1] >= 40 and cur_songbox.real_pos[1] <= screen_setup.screen_height-80:

                pygame.draw.rect(screen_setup.screen,cur_songbox.color,(cur_songbox.pos[0],cur_songbox.real_pos[1],cur_songbox.pos2[0],cur_songbox.pos2[1]))
                
                screen_setup.screen.blit(cur_songbox.img,(cur_songbox.pos[0]+cur_songbox.img_buffer[0],cur_songbox.real_pos[1]+cur_songbox.img_buffer[1]))
                screen_setup.screen.blit(cur_songbox.name_surface,[cur_songbox.pos[0]+cur_songbox.name_buffer[0],cur_songbox.real_pos[1]+cur_songbox.name_buffer[1]])

                song_length_width = get_text_width(cur_songbox.song_length,small_text_font,text_color)
                draw_text(cur_songbox.song_length,small_text_font,text_color,[cur_songbox.pos[0]+cur_songbox.pos2[0]-song_length_width-40,cur_songbox.real_pos[1]+cur_songbox.length_buffer[1]])

                songbox_collision(i)

                if edit_playlists == False:
                    pygame.draw.rect(screen_setup.screen,(20,20,20),((cur_songbox.pos[0]+cur_songbox.pos2[0])-32.5,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-32.5,30,30))
                    if song_selected == i:
                        pygame.draw.rect(screen_setup.screen,button_hovered,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                    elif cur_songbox.hovered == True:
                        if cur_songbox.delete == False:
                            pygame.draw.rect(screen_setup.screen,cur_songbox.hovered_color,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                        else:
                            pygame.draw.rect(screen_setup.screen,(225,40,40),((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                            screen_setup.screen.blit(garbage_img,((cur_songbox.pos[0]+cur_songbox.pos2[0])-33,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-33))
                else:

                    pygame.draw.rect(screen_setup.screen,(20,20,20),((cur_songbox.pos[0]+cur_songbox.pos2[0])-32.5,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-32.5,30,30))
                    if cur_songbox.playlist_clicked:
                        pygame.draw.rect(screen_setup.screen,button_hovered,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                    elif cur_songbox.hovered == True:
                        if cur_songbox.delete == False:
                            pygame.draw.rect(screen_setup.screen,cur_songbox.hovered_color,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                        else:
                            pygame.draw.rect(screen_setup.screen,(225,40,40),((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                            screen_setup.screen.blit(garbage_img,((cur_songbox.pos[0]+cur_songbox.pos2[0])-33,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-33))


# playlist box stuff
playlistbox_list = []
playlist_path = ''
playlist_selected = -1
delete = False

loaded_playlist_id = -1
playlist_content = []
create_playlist = False
playlist_changed = False

playlist_songs = []

class playlistbox:
    def __init__(self,pos,pos2,color,hovered_color,playlist_name,name_buffer,scene_visible,txt_path,folder_path):
        self.pos = pos
        self.real_pos = [0,0]
        self.pos2 = pos2
        self.color = color
        self.hovered_color = hovered_color
        self.playlist_name = playlist_name
        self.name_buffer = name_buffer
        self.scene_visible = scene_visible
        self.txt_path = txt_path
        self.folder_path = folder_path
        self.selected = False
        self.hovered = False
        self.delete = False

def add_playlistbox(pos,pos2,color,hovered_color,playlist_name,name_buffer,scene_visible,txt_path,folder_path):
    playlistbox_list.append(playlistbox(pos,pos2,color,hovered_color,playlist_name,name_buffer,scene_visible,txt_path,folder_path))

def remove_playlistbox_selected():
    global playlist_selected, playlist_path
    playlist_selected = -1
    playlist_path = ''

def playlistbox_collision(index):
    global delete, playlist_selected, playlist_path, playlist_changed
    cur_playlistbox = playlistbox_list[index]
    pos = [(cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-32.5,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-32.5]
    pos2 = [30,30]
    delete = False
    if input.mouse_position[0] < pos[0]+pos2[0] and input.mouse_position[0] > pos[0] and input.mouse_position[1] < pos[1]+pos2[1] and input.mouse_position[1] > pos[1]:
        cur_playlistbox.hovered = True
        if input.find_key("shift").pressed:
            delete = True
        if input.find_mouse_button("left_click").just_pressed:
            if delete:
                if playlist_path != cur_playlistbox.folder_path:
                    remove(cur_playlistbox.txt_path)
                    Path.rmdir(cur_playlistbox.folder_path)
                    grabber.update_playlistbox = True
            else:
                cur_playlistbox.selected = True
                if playlist_selected != index:
                    remove_playlistbox_selected()
                    playlist_selected = index
                    playlist_path = cur_playlistbox.folder_path
                    playlist_changed = True
                else:
                    remove_playlistbox_selected()
                    playlist_changed = True
    else:
        cur_playlistbox.hovered = False

def playlistbox_tick():
    global curScene, searching, recalculate, delete, playlist_songs, garbage_img
    for i in range(len(playlistbox_list)):
        cur_playlistbox = playlistbox_list[i]

        if i == len(playlistbox_list) - 1:
            max_view_height = screen_setup.screen_height-120
            if (input.max_scroll_value != cur_playlistbox.pos[1] - max_view_height and input.max_scroll_value != 0 and curScene == 3) or searching or (recalculate and curScene == 3):
                difference = cur_playlistbox.pos[1] - max_view_height
                input.max_scroll_value = difference
                temp = floor(difference/40)
                input.mouse_scroll_sens = clamp(temp,20,60)
                recalculate = False
            elif cur_playlistbox.pos[1] < max_view_height and curScene == 3:
                input.max_scroll_value = 0

        if curScene == cur_playlistbox.scene_visible or cur_playlistbox.scene_visible == 0:
            cur_playlistbox.real_pos[0] = cur_playlistbox.pos[0]
            cur_playlistbox.real_pos[1] = cur_playlistbox.pos[1] - input.mouse_scroll_value

            pygame.draw.rect(screen_setup.screen,cur_playlistbox.color,(cur_playlistbox.pos[0],cur_playlistbox.real_pos[1],cur_playlistbox.pos2[0],cur_playlistbox.pos2[1]))
            
            playlist_name_width = get_text_width(cur_playlistbox.playlist_name,small_text_font,text_color)
            if playlist_name_width > 350:
                average_letter_width = get_letter_width(cur_playlistbox.playlist_name,small_text_font,text_color)
                new_name = cur_playlistbox.playlist_name[:floor(350/average_letter_width)-floor(average_letter_width*0.45)]+'...'
                draw_text(new_name,small_text_font,text_color,[cur_playlistbox.pos[0]+cur_playlistbox.name_buffer[0],cur_playlistbox.real_pos[1]+cur_playlistbox.name_buffer[1]])
            else:
                draw_text(cur_playlistbox.playlist_name,small_text_font,text_color,[cur_playlistbox.pos[0]+cur_playlistbox.name_buffer[0],cur_playlistbox.real_pos[1]+cur_playlistbox.name_buffer[1]])
            
            playlistbox_collision(i)
            
            pygame.draw.rect(screen_setup.screen,(20,20,20),((cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-32.5,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-32.5,30,30))
            if playlist_selected == i:
                pygame.draw.rect(screen_setup.screen,button_hovered,((cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-30,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-30,24,24))
            elif cur_playlistbox.hovered == True:
                if delete == False:
                    pygame.draw.rect(screen_setup.screen,cur_playlistbox.hovered_color,((cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-30,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-30,24,24))
                else:
                    pygame.draw.rect(screen_setup.screen,(225,40,40),((cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-30,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-30,24,24))
                    screen_setup.screen.blit(garbage_img,((cur_playlistbox.pos[0]+cur_playlistbox.pos2[0])-33,(cur_playlistbox.real_pos[1]+cur_playlistbox.pos2[1])-33))

def hud_tick():
    global song_selected, texture_button_reset, song_selected_list, song_selected_length, song_selected_pos

    playlistbox_tick()
    songbox_tick()
    block_tick()
    button_tick()
    texture_button_tick()
    textInput_tick()
    slider_tick()
    checkbox_tick()

    if input.next_track:
        skip_foward()
        input.next_track = False
    elif input.previous_track:
        skip_backwards()
        input.previous_track = False

    if player.pick_new_song == True:
        skip_foward()
        player.pick_new_song = False
