import pygame
import keyboard
import threading
from sys import exit

from file_handler import player

# New Key Input System
key_list = []

Any_Button_Pressed = False

class Key:
    def __init__(self,name,input):
        self.name = name
        self.input = input
        self.just_pressed = False
        self.pressed = False
        self.wait = 0
        self.any_button_pressed = False

def add_key(name,input):
    key_list.append(Key(name,input))

def key_tick():
    global Any_Button_Pressed
    for i in range(len(key_list)):
        cur_key = key_list[i]
        if cur_key.name != "null":
            cur_key.pressed = False
            keys = pygame.key.get_pressed()
            cur_key.any_button_pressed = False
            for t in range(len(cur_key.input)):
                if keys[cur_key.input[t]]:
                    cur_key.any_button_pressed = True
                    Any_Button_Pressed = True
            if cur_key.any_button_pressed == True:
                cur_key.pressed = True
            elif cur_key.pressed != True:
                cur_key.pressed = False
                cur_key.wait = 0
            if cur_key.pressed == True:
                if cur_key.wait == 0:
                    cur_key.wait = 1
                    cur_key.just_pressed = True
                if cur_key.wait > 1:
                    cur_key.just_pressed = False
                if cur_key.wait > 0:
                    cur_key.wait += 1
            if cur_key.just_pressed == True and cur_key.wait == 0:
                cur_key.just_pressed = False
        else:
            cur_key.pressed = "no key found"
            cur_key.just_pressed = "no key found"

def find_key(name):
    for i in range(len(key_list)):
        cur_key = key_list[i]
        if cur_key.name == name:
            return cur_key
    for i in range(len(key_list)):
        cur_key = key_list[i]
        if cur_key.name == "null":
            print("")
            print(f"KEY: '{name}' NOT FOUND")
            print("")
            return cur_key
    

# Add keys needed for inputs
add_key("null",[pygame.K_DOLLAR])
add_key("up",[pygame.K_w,pygame.K_UP])
add_key("down",[pygame.K_s,pygame.K_DOWN])
add_key("left",[pygame.K_a,pygame.K_LEFT])
add_key("right",[pygame.K_d,pygame.K_RIGHT])
add_key("space",[pygame.K_SPACE])
#add_key("player",[pygame.K_MENU])
add_key("shift",[pygame.K_LSHIFT,pygame.K_RSHIFT])
add_key("escape",[pygame.K_ESCAPE])
add_key("delete",[pygame.K_DELETE])
add_key("backspace",[pygame.K_BACKSPACE])
add_key("f10",[pygame.K_F10])
add_key("f11",[pygame.K_F11])
add_key("f12",[pygame.K_F12])

# New Mouse Button Input System
mouse_button_list = []

class MouseButton:
    def __init__(self,name,input):
        self.name = name
        self.input = input
        self.just_pressed = False
        self.pressed = False
        self.wait = 0

def add_mouse_button(name,input):
    mouse_button_list.append(MouseButton(name,input))

def mouse_button_tick():
    global Any_Button_Pressed
    for i in range(len(mouse_button_list)):
        cur_mouse_button = mouse_button_list[i]
        if cur_mouse_button.name != "null":
            if cur_mouse_button.pressed == False:
                cur_mouse_button.wait = 0
            if cur_mouse_button.pressed == True:
                Any_Button_Pressed = True
                if cur_mouse_button.wait == 0:
                    cur_mouse_button.wait = 1
                    cur_mouse_button.just_pressed = True
                if cur_mouse_button.wait > 1:
                    cur_mouse_button.just_pressed = False
                if cur_mouse_button.wait > 0:
                    cur_mouse_button.wait += 1
            if cur_mouse_button.just_pressed == True and cur_mouse_button.wait == 0:
                cur_mouse_button.just_pressed = False
        else:
            cur_mouse_button.pressed = "no mouse button found"
            cur_mouse_button.just_pressed = "no mouse button found"

def find_mouse_button(name):
    for i in range(len(mouse_button_list)):
        cur_mouse_button = mouse_button_list[i]
        if cur_mouse_button.name == name:
            return cur_mouse_button
    for i in range(len(mouse_button_list)):
        cur_mouse_button = mouse_button_list[i]
        if cur_mouse_button.name == "null":
            print("")
            print(f"MOUSE BUTTON: '{name}' NOT FOUND")
            print("")
            return cur_mouse_button

def update_mouse_buttons():
    for i in range(len(mouse_button_list)):
        cur_mouse_button = mouse_button_list[i]
        mouse_list = pygame.mouse.get_pressed(num_buttons=5)
        cur_mouse_button.pressed = mouse_list[cur_mouse_button.input]
    
# Add all mouse buttons needed
add_mouse_button("null",0)
add_mouse_button("left_click",0)
add_mouse_button("middle_click",1)
add_mouse_button("right_click",2)
add_mouse_button("m4_click",3)
add_mouse_button("m5_click",4)

mouse_position = pygame.mouse.get_pos()
mouse_scroll_value = 0
mouse_scroll_velocity = 0
mouse_scroll_drag = -0.4
mouse_scroll_sens = 20
max_scroll_value = -1

def mouse_scroll(event):
    global mouse_scroll_value, mouse_scroll_sens, max_scroll_value, mouse_scroll_velocity, mouse_scroll_drag
    if event.type == pygame.QUIT:
        pygame.display.quit()
        pygame.quit()
        exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            if mouse_scroll_velocity > 0:
                mouse_scroll_velocity = 0
            else:
                mouse_scroll_velocity -= mouse_scroll_sens
        elif event.button == 5:
            if mouse_scroll_velocity < 0:
                mouse_scroll_velocity = 0
            else:
                mouse_scroll_velocity += mouse_scroll_sens

texture_update = False
running = True

def read_input():
    global texture_update, running
    counter = 0
    while running:
        if keyboard.read_key() == 'play/pause media':
                counter += 1
        if counter == 1:
            if player.is_playing:
                texture_update = True
                if player.is_paused:
                    player.unpause_song()
                else:
                    player.pause_song()
            else:
                if player.song_path != '':
                    texture_update = True
                    player.play_song()
        elif counter == 2:
            counter = 0

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        except:
            running = False

thread = threading.Thread(target=read_input, daemon = True)
thread.start()

def update_inputs():
    global mouse_position, Any_Button_Pressed, mouse_scroll_value, mouse_scroll_velocity, mouse_scroll_drag
    Any_Button_Pressed = False
    mouse_position = pygame.mouse.get_pos()

    mouse_scroll_velocity += mouse_scroll_velocity * mouse_scroll_drag
    mouse_scroll_value += mouse_scroll_velocity

    if mouse_scroll_value < 0:
        mouse_scroll_value = 0
        mouse_scroll_velocity = 0
    if max_scroll_value != -1:
        if mouse_scroll_value > max_scroll_value:
            mouse_scroll_value = max_scroll_value
            mouse_scroll_velocity = 0

    update_mouse_buttons()
    mouse_button_tick()
    key_tick()