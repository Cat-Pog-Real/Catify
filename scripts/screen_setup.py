import pygame
import win32api
import win32con
import win32gui

from scripts import input
from scripts import hud

project_name = "Catify"

fuchsia = (255, 0, 128)

changed_res = False

screen_width = 1000
screen_height = 700

center_x = screen_width / 2
center_y = screen_height / 2

check_screen_width = screen_width
check_screen_height = screen_height

old_screen_width = screen_width
old_screen_height = screen_height
screen_resizeable = False
screen_fullscreen = False
screen_no_window = False
show_fps = False

if screen_resizeable == True:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption(project_name)
icon = pygame.image.load('default_files/icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

def screen_tick():
    global screen_width, screen_height, old_screen_width, old_screen_height, screen_resizeable, screen_fullscreen, screen, screen_no_window, show_fps, center_x, center_y, check_screen_width, check_screen_height, changed_res, update_counter

    check_screen_width = screen_width
    check_screen_height = screen_height

    if screen_fullscreen == True and screen_width != 1920:
        old_screen_width = screen_width
        old_screen_height = screen_height
    if screen_resizeable == True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

    center_x = screen_width / 2
    center_y = screen_height / 2

    if check_screen_width != screen_width or check_screen_height != screen_height:
        changed_res = True
    else:
        changed_res = False
    
    #if input.find_key("f10").just_pressed == True:
    #    if show_fps == False:
    #        show_fps = True
    #    else:
    #        show_fps = False
    #
    #if input.find_key("f11").just_pressed == True:
    #    if screen_fullscreen == False:
    #        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    #        screen_fullscreen = True
    #    elif screen_fullscreen == True:
    #        screen_width = old_screen_width
    #        screen_height = old_screen_height
    #        if screen_resizeable == True:
    #            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    #        else:
    #            screen = pygame.display.set_mode((screen_width, screen_height))
    #        screen_fullscreen = False
    #
    #if input.find_key("f12").just_pressed == True:
    #    if screen_no_window == False:
    #        screen_no_window = True
    #        updateScreen()
    #    else:
    #        screen_no_window = False
    #        updateScreen()
    
    # Show FPS
    if screen_no_window == False and show_fps == True:
        fps = clock.get_fps()
        hud.draw_text(str(round(fps)),hud.medium_text_font,hud.text_color,[0,0])
    
    # oh fuck quit button
    #if input.find_key("delete").just_pressed == True:
    #    pygame.display.quit()
    #    pygame.quit()
    #    exit()

    temp = list(pygame.display.get_caption())
    if temp[0] == 'MoviePy':
        pygame.display.set_caption(project_name)


def updateScreen():
    # Clear Background
    if screen_no_window == False:
        if screen_resizeable == True:
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        else:
            screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        # Create layered window
        if screen_fullscreen == False:
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        else:
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.FULLSCREEN)
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        screen.fill(fuchsia)