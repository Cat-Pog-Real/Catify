import pygame
import win32gui
import keyboard
from sys import exit

from scripts import input
from scripts import hud
from scripts import screen_setup

from file_handler import player
from file_handler import grabber
from file_handler import song_preview

from special import command

pygame.init()

# global variables
background_color = (20,20,20)
transparent_color = (255, 0, 128)
active_fps = 60
inactve_fps = 8
target_fps = active_fps
delta = 0
fps = 0

# Add Hud Elements
hud.add_block([0,0],[screen_setup.screen_width,40],(10,10,10),0)
hud.add_block([0,screen_setup.screen_height-80],[screen_setup.screen_width,80],(10,10,10),0)

text_width = 600
text_height = 150
hud.add_textInput([screen_setup.center_x-(text_width/2),screen_setup.center_y-(text_height/2)+185],[text_width,text_height],(210,210,210),"Put Youtube Link Here:",(100,100,100),hud.small_text_font,(30,30,30),"",[10,10],1)

hud.add_button([screen_setup.center_x-75,screen_setup.screen_height-60],[150,40],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.medium_text_font,"Download",[7,4],1)

hud.add_slider([screen_setup.center_x+260,17],[120,10],9,(200,200,200),(40,40,40),(240,240,240),0.18,0.01,hud.small_text_font,'Volume:',[-68,-4],2)
hud.add_slider([screen_setup.center_x+335,screen_setup.screen_height-40],[140,10],9,(200,200,200),(40,40,40),(240,240,240),0.18,0,hud.small_text_font,'0:00',[51,-22],2)

hud.add_button([5,5],[120,30],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.small_text_font,"Download page",[9,6],0)
hud.add_button([130,5],[120,30],hud.button_idle,hud.button_hovered,hud.button_clicked,hud.small_text_font,"Song list",[30,6],0)

hud.add_texture_button([screen_setup.center_x+75,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Pause",[0,-20],2,pygame.image.load('default_files/pause.png'),[-0.5,1],8)
hud.add_texture_button([screen_setup.center_x+120,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Skip +1",[0,-20],2,pygame.image.load('default_files/skip_song.png'),[-2,1],8)
hud.add_texture_button([screen_setup.center_x+30,screen_setup.screen_height-60],[40,40],hud.button_hovered,(50,50,50),hud.button_clicked,hud.small_text_font,"Skip -1",[0,-20],2,pygame.transform.flip(pygame.image.load('default_files/skip_song.png'),True,False),[2,1],8)

hud.add_checkbox([screen_setup.center_x+265,screen_setup.screen_height-50],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Repeat',[-8,-20],2)
hud.add_checkbox([screen_setup.center_x+205,screen_setup.screen_height-50],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Shuffle',[-8,-20],2)

hud.add_checkbox([screen_setup.center_x+140,5],[30,30],hud.button_idle,(50,50,50),hud.button_hovered,hud.small_text_font,'Mute:',[-42,8],2)

while True:
    # Handling Background Position and Color
    if screen_setup.screen_no_window == False:
        screen_setup.screen.fill(background_color)
    else:
        win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 5, 0, 0, 1)
        screen_setup.screen.fill(transparent_color)

    # Update Inputs
    input.update_inputs()

    # Draw Game
    grabber.grabber_tick()
    song_preview.update_songbox_preview()

    # Draw Hud/Gui DRAW LAST
    hud.hud_tick()
    hud.draw_text("Catify",hud.medium_text_font,hud.text_color,[screen_setup.screen_width-90,3])

    # Read Custom Commands
    command.custom_commands()

    # draw ontop of hud
    player.player_tick()

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

    # Update Display and locks the framerate to the target fps also calculates delta also gets current fps
    screen_setup.screen_tick()

    pygame.display.update()
    if target_fps != 0 and target_fps < 1001:
        screen_setup.clock.tick(target_fps)
    else:
        screen_setup.clock.tick()
        pygame.event.wait(1)

    fps = screen_setup.clock.get_fps()
    delta = screen_setup.clock.tick(fps)/1000