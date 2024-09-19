import pygame

from scripts import hud
from scripts import input

command_list = []

command_ID = 0

class command:
    def __init__(self,command: str,value,id):
        self.c = command
        self.v = value
        self.id = id
        self.v_default = value
        self.v_type = type(value)

def add_command(c,v):
    global command_ID
    id = command_ID
    command_list.append(command(c,v,id))
    command_ID += 1

add_command('button_color',(0,0,0))
add_command('set_max_volume',0.0)
add_command('set_scroll_speed',0)
add_command('save','no_value')
add_command('reset','no_value')
add_command('quit','no_value')

try:
    data = open('default_files/settings.txt', 'r').read()
    data = str(data)
    data = data.split('|')
except:
    data = 'fail'

if data != 'fail':
    if data[0] == '':
        pass
        #print('no data to load')
    else:
        try:
            command_list[0].v = eval(data[0])
            command_list[1].v = eval(data[1])
            command_list[2].v = eval(data[2])
            #print('data loaded')
        except:
            #print('shit')
            pass

def command_tick():
    for i in range(len(command_list)):
        cur_command = command_list[i]
        if cur_command.v_default != 'no_value':
            if cur_command.v != cur_command.v_default:
                if cur_command.id == 0:
                    temp = True
                    for i in range(len(cur_command.v)):
                        if cur_command.v[i] > 255 or cur_command.v[i] < 0:
                            temp = False
                    if len(cur_command.v) == 3:
                        if temp == True:
                            hud.button_hovered = cur_command.v
                    else:
                        cur_command.v = cur_command.v_default
                        if len(hud.textInput_list) > 0:
                            cur_textInput = hud.textInput_list[0]
                            cur_textInput.text = "invalid color"
                elif cur_command.id == 1:
                    if cur_command.v > 0.01 and cur_command.v <= 1:
                        hud.slider_list[0].max_value = cur_command.v
                    else:
                        cur_command.v = cur_command.v_default
                        if len(hud.textInput_list) > 0:
                            cur_textInput = hud.textInput_list[0]
                            cur_textInput.text = "invalid max volume"
                elif cur_command.id == 2:
                    if cur_command.v >= 0:
                        input.mouse_scroll_sens = cur_command.v
                    else:
                        cur_command.v = cur_command.v_default
                        if len(hud.textInput_list) > 0:
                            cur_textInput = hud.textInput_list[0]
                            cur_textInput.text = "invalid mouse scroll speed"
        else:
            if cur_command.v == 'run':
                cur_command.v = cur_command.v_default
                if cur_command.id == 3:
                    t = open('default_files/settings.txt', 'w')
                    t.write(str(command_list[0].v)+'|'+str(command_list[1].v)+'|'+str(command_list[2].v))
                    if len(hud.textInput_list) > 0:
                        cur_textInput = hud.textInput_list[0]
                        cur_textInput.text = "done"
                elif cur_command.id == 4:
                    open('default_files/settings.txt', 'w').close()
                    if len(hud.textInput_list) > 0:
                        cur_textInput = hud.textInput_list[0]
                        cur_textInput.text = "default restored"
                elif cur_command.id == 5:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

def custom_commands():
    command_tick()
    if len(hud.textInput_list) > 0:
        cur_textInput = hud.textInput_list[0]
        text = str(cur_textInput.text)
        for i in range(len(command_list)):
            cur_command = command_list[i]
            if cur_command.v_default != 'no_value':
                if cur_command.c in text:
                   if ' ' in text and ' .' in text:
                        x = text.split()
                        if len(x) > 1:
                            if type(eval(x[1])) == cur_command.v_type:
                                cur_command.v = eval(x[1])
                                cur_textInput.text = ''
            else:
                if cur_command.c in text:
                    cur_command.v = 'run'