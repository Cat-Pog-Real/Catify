import pygame
import math
import random
import threading
import win32clipboard
import os
import pathlib
from sys import exit

from scripts import input
from scripts import screen_setup

from file_handler import grabber
from file_handler import player

pygame.init()

# Hud Variables // Classes
curScene = 1
volume = 0

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
            elif cur_button.id == 3:
                pass
            elif cur_button.id == 4:
                pass
    else:
        cur_button.color = cur_button.idle

def button_tick():
    for i in range(len(button_list)):
        cur_button = button_list[i]
        if cur_button.scene_visible == 0 or cur_button.scene_visible == curScene:
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
        self.img = img
        self.img_buffer = img_buffer
        self.rounded = rounded

def add_texture_button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible,img,img_buffer,rounded):
    global texture_button_ID
    id = texture_button_ID
    texture_button_list.append(texture_Button(pos,pos2,color,hovered,clicked,font,text,text_buffer,scene_visible,id,img,img_buffer,rounded))
    texture_button_ID += 1

def texture_buttoncollsion(i):
    global texture_button_reset, song_selected, song_selected_list, song_selected_length, texture_button_reset, last_press
    cur_button = texture_button_list[i]
    if input.mouse_position[0] < cur_button.pos[0]+cur_button.pos2[0] and input.mouse_position[0] > cur_button.pos[0] and input.mouse_position[1] < cur_button.pos[1]+cur_button.pos2[1] and input.mouse_position[1] > cur_button.pos[1]:
        cur_button.color = cur_button.hovered
        if input.find_mouse_button("left_click").just_pressed == 1:
            global curScene
            cur_button.color = cur_button.clicked
            if cur_button.id == 0:
                cur_songbox = songbox_list[song_selected]
                if player.is_playing == False and player.song_time_elapsed_in_seconds == 0:
                    if player.song_path != '':
                        player.song_name = cur_songbox.song_name
                        player.song_length = math.floor(cur_songbox.length_in_seconds)
                        player.song_index = song_selected
                        player.song_time_elapsed = 0.0
                        player.set_paths(cur_songbox.img_path,cur_songbox.song)
                        player.play_song()
                        texture_button_reset = True
                    else:
                        if player.is_playing == True:
                            player.stop_song()
                        rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        cur_songbox = songbox_list[rand]
                        if player.song_name != cur_songbox.song_name:
                            player.song_name = cur_songbox.song_name
                            player.song_length = math.floor(cur_songbox.length_in_seconds)
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
                        cur_button.img = pygame.image.load('default_files/play.png')
                        cur_button.img_buffer = [0,1]
                    elif player.is_paused == True:
                        player.unpause_song()
                        cur_button.text = 'Pause'
                        cur_button.img = pygame.image.load('default_files/pause.png')
                        cur_button.img_buffer = [-0.5,1]
            elif cur_button.id == 1:
                if (len(song_selected_list) > 1 and last_press == -1) != True:
                    if player.is_shuffle == True:
                        if player.is_playing == True:
                            player.stop_song()
                        rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        cur_songbox = songbox_list[rand]
                        if player.song_name != cur_songbox.song_name:
                            player.song_name = cur_songbox.song_name
                            player.song_length = math.floor(cur_songbox.length_in_seconds)
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
                        temp = song_selected + 1
                        if temp >= len(songbox_list):
                            temp = 0
                        song_selected = temp
                        cur_songbox = songbox_list[temp]
                        player.song_name = cur_songbox.song_name
                        player.song_length = math.floor(cur_songbox.length_in_seconds)
                        player.song_index = temp
                        player.song_time_elapsed = 0.0
                        player.set_paths(cur_songbox.img_path,cur_songbox.song)
                        player.play_song()
                        texture_button_reset = True
                else:
                    if player.is_playing == True:
                        player.stop_song()
                    temp = song_selected_list[1]
                    song_selected_list.pop(1)
                    song_selected = temp
                    cur_songbox = songbox_list[temp]
                    player.song_name = cur_songbox.song_name
                    player.song_length = math.floor(cur_songbox.length_in_seconds)
                    player.song_index = temp
                    player.song_time_elapsed = 0.0
                    player.set_paths(cur_songbox.img_path,cur_songbox.song)
                    player.play_song()
                    texture_button_reset = True
                if player.is_shuffle == True:
                    if len(song_selected_list) < song_selected_length:
                            if len(song_selected_list) > 0:
                                song_selected_list.insert(len(song_selected_list),song_selected)
                            else:
                                song_selected_list.insert(0,song_selected)
                    else:
                        song_selected_list.pop(0)
                        if len(song_selected_list) > 0:
                            song_selected_list.insert(len(song_selected_list),song_selected)
                        else:
                            song_selected_list.insert(0,song_selected)
                last_press = 1
            elif cur_button.id == 2:
                if (len(song_selected_list) > 1 and last_press == 1) != True:
                    if player.is_shuffle == True:
                        if player.is_playing == True:
                            player.stop_song()
                        rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        if rand == player.song_index:
                            rand = random.randrange(0,len(songbox_list))
                        cur_songbox = songbox_list[rand]
                        if player.song_name != cur_songbox.song_name:
                            player.song_name = cur_songbox.song_name
                            player.song_length = math.floor(cur_songbox.length_in_seconds)
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
                        temp = song_selected - 1
                        if temp < 0:
                            temp = len(songbox_list)-1
                        song_selected = temp
                        cur_songbox = songbox_list[temp]
                        player.song_name = cur_songbox.song_name
                        player.song_length = math.floor(cur_songbox.length_in_seconds)
                        player.song_index = temp
                        player.song_time_elapsed = 0.0
                        player.set_paths(cur_songbox.img_path,cur_songbox.song)
                        player.play_song()
                        texture_button_reset = True
                else:
                    if player.is_playing == True:
                        player.stop_song()
                    temp = song_selected_list[len(song_selected_list)-2]
                    song_selected_list.pop(len(song_selected_list)-2)
                    song_selected = temp
                    cur_songbox = songbox_list[temp]
                    player.song_name = cur_songbox.song_name
                    player.song_length = math.floor(cur_songbox.length_in_seconds)
                    player.song_index = temp
                    player.song_time_elapsed = 0.0
                    player.set_paths(cur_songbox.img_path,cur_songbox.song)
                    player.play_song()
                    texture_button_reset = True
                if player.is_shuffle == True:
                    if len(song_selected_list) < song_selected_length:
                                song_selected_list.insert(0,song_selected)
                    else:
                        song_selected_list.pop(len(song_selected_list)-1)
                        song_selected_list.insert(0,song_selected)
                last_press = -1
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
                    cur_button.img = pygame.image.load('default_files/play.png')
                    cur_button.img_buffer = [0,1]
                #check 2
                if texture_button_reset == True:
                    cur_button.text = 'Pause'
                    cur_button.img = pygame.image.load('default_files/pause.png')
                    cur_button.img_buffer = [-0.5,1]
                    texture_button_reset = False
                #check 3
                if input.texture_update:
                    input.texture_update = False
                    if player.is_playing:
                        if player.is_paused == False:
                            cur_button.text = 'Pause'
                            cur_button.img = pygame.image.load('default_files/pause.png')
                            cur_button.img_buffer = [-0.5,1]
                        else:
                            cur_button.text = 'Play'
                            cur_button.img = pygame.image.load('default_files/play.png')
                            cur_button.img_buffer = [0,1]
                    else:
                        cur_button.text = 'Pause'
                        cur_button.img = pygame.image.load('default_files/pause.png')
                        cur_button.img_buffer = [-0.5,1]
            #draw button
            pygame.draw.rect(screen_setup.screen,cur_button.color,(cur_button.pos,cur_button.pos2),0,cur_button.rounded)
            screen_setup.screen.blit(cur_button.img,(cur_button.pos[0]+cur_button.img_buffer[0],cur_button.pos[1]+cur_button.img_buffer[1]))
            #draw text
            if input.mouse_position[0] < cur_button.pos[0]+cur_button.pos2[0] and input.mouse_position[0] > cur_button.pos[0] and input.mouse_position[1] < cur_button.pos[1]+cur_button.pos2[1] and input.mouse_position[1] > cur_button.pos[1]:
                draw_text(cur_button.text,cur_button.font,text_color,(cur_button.pos[0]+cur_button.text_buffer[0],cur_button.pos[1]+cur_button.text_buffer[1]))

# Text Variables
small_text_font = pygame.font.Font('default_files/ARIAL.TTF',15)
medium_text_font = pygame.font.Font('default_files/ARIAL.TTF',30)
large_text_font = pygame.font.Font('default_files/ARIAL.TTF',45)
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
    global volume, slider_unpause

    for i in range(len(slider_list)):
        cur_slider = slider_list[i]
        if cur_slider.scene_visible == curScene or cur_slider.scene_visible == 0:
            
            pygame.draw.rect(screen_setup.screen,cur_slider.box_color,(cur_slider.pos,cur_slider.pos2),0,10)
    
            dist = math.sqrt(math.pow(cur_slider.circle_pos[0]-input.mouse_position[0],2)+math.pow(cur_slider.circle_pos[1]-input.mouse_position[1],2))
    
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
            #cur_slider.value = math.floor(cur_slider.value)
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
                        cur_slider.value = math.floor(cur_slider.value)
                        #print(cur_slider.value)
                        player.song_time_elapsed = cur_slider.value
                        if slider_unpause == False:
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
                slider_unpause = False

# Checkbox
checkbox_list = []

checkbox_ID = 0

mute = False

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

def checkbox_tick():
    global mute, song_selected_list
    for i in range(len(checkbox_list)):
        cur_checkbox = checkbox_list[i]
        if cur_checkbox.scene_visible == curScene or cur_checkbox.scene_visible == 0:
            cur_checkbox.h = False
            if input.mouse_position[0] > cur_checkbox.pos[0] and input.mouse_position[0] < cur_checkbox.pos[0] + cur_checkbox.pos2[0] and input.mouse_position[1] > cur_checkbox.pos[1] and input.mouse_position[1] < cur_checkbox.pos[1] + cur_checkbox.pos2[1]:
                cur_checkbox.h = True
                if input.find_mouse_button('left_click').just_pressed == True:
                    song_selected_list = []
                    if cur_checkbox.checked == 0:
                        cur_checkbox.checked = 1
                    else:
                        cur_checkbox.checked = 0

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
            elif cur_checkbox.id == 1:
                if cur_checkbox.checked == 0:
                    player.is_shuffle = False
                elif cur_checkbox.checked == 1:
                    player.is_shuffle = True
            elif cur_checkbox.id == 2:
                if cur_checkbox.checked == 0:
                    mute = False
                elif cur_checkbox.checked == 1:
                    mute = True
                    

# Text Input
textInput_list = []

is_typing = False

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

def textInput_tick():
    global is_typing
    for i in range(len(textInput_list)):
        cur_textInput = textInput_list[i]
        #print(cur_textInput.active)
        if cur_textInput.scene_visible == curScene:
            #textbox logic
            textInputCollision(i)
            #draw textbox
            pygame.draw.rect(screen_setup.screen,cur_textInput.color,(cur_textInput.pos,cur_textInput.pos2),0,10)
            if cur_textInput.active == 0:

                is_typing = False

                if '|' in cur_textInput.text:
                    cur_textInput.text = str(cur_textInput.text).replace('|','')

                if cur_textInput.text == "":
                    draw_text(cur_textInput.text_empty,cur_textInput.text_font,cur_textInput.text_empty_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]))
                else:
                    draw_text(cur_textInput.text,cur_textInput.text_font,cur_textInput.text_empty_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]))
            else:
                
                is_typing = True

                if cur_textInput.blinker_wait <= 0:
                    cur_textInput.blinker_wait = 12
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
                    cur_textInput.backspace_wait = -12

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
                        win32clipboard.OpenClipboard()
                        try:
                            cur_textInput.text = win32clipboard.GetClipboardData()
                        except:
                            cur_textInput.text = 'NOT VALID COPY'
                        win32clipboard.CloseClipboard()
                
                draw_text(cur_textInput.text,cur_textInput.text_font,cur_textInput.text_color,(cur_textInput.pos[0]+cur_textInput.text_buffer[0],cur_textInput.pos[1]+cur_textInput.text_buffer[1]))

def hud_event(event):
    global is_typing
    if is_typing:
        for i in range(len(textInput_list)):
            cur_textInput = textInput_list[i]
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

song_selected_list = []
song_selected_length = 2

max_string_length = 39

class songbox:
    def __init__(self,pos,pos2,color,hovered_color,img_path,img,img_buffer,song_name,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path):
        self.pos = pos
        self.real_pos = [0,0]
        self.pos2 = pos2
        self.color = color
        self.hovered_color = hovered_color
        self.img_path = img_path
        self.img = img
        self.img_buffer = img_buffer
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

def add_songbox(pos,pos2,color,hovered,img_path,img,img_buffer,song_name,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path):
    songbox_list.append(songbox(pos,pos2,color,hovered,img_path,img,img_buffer,song_name,song_length,name_buffer,length_buffer,scene_visible,song,length_in_seconds,folder_path))

def remove_songbox_selected():
    global song_selected
    song_selected = -1

def songbox_collision(index):
    global song_selected, texture_button_reset
    cur_songbox = songbox_list[index]
    cur_songbox.delete = False
    pos = [(cur_songbox.pos[0]+cur_songbox.pos2[0])-32.5,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-32.5]
    pos2 = [30,30]
    if input.mouse_position[0] < pos[0]+pos2[0] and input.mouse_position[0] > pos[0] and input.mouse_position[1] < pos[1]+pos2[1] and input.mouse_position[1] > pos[1]:
        cur_songbox.hovered = True
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
                        player.song_length = math.floor(cur_songbox.length_in_seconds)
                        player.song_index = song_selected
                        player.song_time_elapsed = 0.0
                        player.set_paths(cur_songbox.img_path,cur_songbox.song)
                        player.play_song()
                        texture_button_reset = True
                else:
                    remove_songbox_selected()
            elif player.song_path != cur_songbox.song:
                os.remove(cur_songbox.img_path)
                os.remove(cur_songbox.song)
                pathlib.Path.rmdir(cur_songbox.folder_path)
                grabber.update_songbox = True
    else:
        cur_songbox.hovered = False

def songbox_tick():
    global curScene, max_string_length, song_selected
    for i in range(len(songbox_list)):
        cur_songbox = songbox_list[i]
        if curScene == cur_songbox.scene_visible or cur_songbox.scene_visible == 0:
            cur_songbox.real_pos[0] = cur_songbox.pos[0]
            cur_songbox.real_pos[1] = cur_songbox.pos[1] - input.mouse_scroll_value

            if cur_songbox.real_pos[1] + cur_songbox.pos2[1] >= 40 and cur_songbox.real_pos[1] <= screen_setup.screen_height-80:

                pygame.draw.rect(screen_setup.screen,cur_songbox.color,(cur_songbox.pos[0],cur_songbox.real_pos[1],cur_songbox.pos2[0],cur_songbox.pos2[1]))
                if i == len(songbox_list)-1:
                    if cur_songbox.real_pos[1] < 580 and cur_songbox.pos[1] > 580:
                        difference = input.mouse_scroll_value + (cur_songbox.real_pos[1]-580)
                        input.mouse_scroll_value = difference
                        input.max_scroll_value = difference
                    elif cur_songbox.pos[1] < 580:
                        input.max_scroll_value = 0
                
                cur_songbox.img = pygame.transform.scale(cur_songbox.img, (40, 30))
                screen_setup.screen.blit(cur_songbox.img,(cur_songbox.pos[0]+cur_songbox.img_buffer[0],cur_songbox.real_pos[1]+cur_songbox.img_buffer[1]))
                if len(cur_songbox.song_name) <= max_string_length:
                    draw_text(cur_songbox.song_name,small_text_font,text_color,[cur_songbox.pos[0]+cur_songbox.name_buffer[0],cur_songbox.real_pos[1]+cur_songbox.name_buffer[1]])
                else:
                    new_txt = cur_songbox.song_name[:max_string_length] + '...'
                    draw_text(new_txt,small_text_font,text_color,[cur_songbox.pos[0]+cur_songbox.name_buffer[0],cur_songbox.real_pos[1]+cur_songbox.name_buffer[1]])
                draw_text(cur_songbox.song_length,small_text_font,text_color,[cur_songbox.pos[0]+cur_songbox.length_buffer[0],cur_songbox.real_pos[1]+cur_songbox.length_buffer[1]])

                songbox_collision(i)

                pygame.draw.rect(screen_setup.screen,(20,20,20),((cur_songbox.pos[0]+cur_songbox.pos2[0])-32.5,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-32.5,30,30))
                if song_selected == i:
                    pygame.draw.rect(screen_setup.screen,button_hovered,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                elif cur_songbox.hovered == True:
                    if cur_songbox.delete == False:
                        pygame.draw.rect(screen_setup.screen,cur_songbox.hovered_color,((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                    else:
                        pygame.draw.rect(screen_setup.screen,(225,40,40),((cur_songbox.pos[0]+cur_songbox.pos2[0])-30,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-30,24,24))
                        img = pygame.image.load('default_files/open_trash.png')
                        img = pygame.transform.scale(img,(30,30))
                        screen_setup.screen.blit(img,((cur_songbox.pos[0]+cur_songbox.pos2[0])-33,(cur_songbox.real_pos[1]+cur_songbox.pos2[1])-33))
                    

def hud_tick():
    global song_selected, texture_button_reset

    songbox_tick()
    block_tick()
    button_tick()
    texture_button_tick()
    textInput_tick()
    slider_tick()
    checkbox_tick()

    if player.pick_new_song == True:
        rand = random.randrange(0,len(songbox_list))
        if rand == player.song_index:
            rand = random.randrange(0,len(songbox_list))
        if rand == player.song_index:
            rand = random.randrange(0,len(songbox_list))
        cur_songbox = songbox_list[rand]
        if player.song_name != cur_songbox.song_name:
            player.song_name = cur_songbox.song_name
            player.song_length = math.floor(cur_songbox.length_in_seconds)
            player.song_index = rand
            player.song_time_elapsed = 0.0
            player.set_paths(cur_songbox.img_path,cur_songbox.song)
            player.play_song()
            player.pick_new_song = False
            remove_songbox_selected()
            song_selected = rand
            texture_button_reset = True