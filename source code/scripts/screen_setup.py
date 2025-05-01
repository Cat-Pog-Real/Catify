import pygame

from scripts import hud

project_name = "Catify"

fuchsia = (255, 0, 128)

changed_res = False

screen_width = 1000
screen_height = 700

min_width = 750
min_height = (min_width/10)*7

center_x = screen_width / 2
center_y = screen_height / 2

check_screen_width = screen_width
check_screen_height = screen_height

old_screen_width = screen_width
old_screen_height = screen_height
screen_resizeable = True
screen_fullscreen = False
screen_no_window = False
show_fps = False

if screen_resizeable == True:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption(project_name)
icon = pygame.image.load('user_data/default_files/icon.png')
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

    if check_screen_width != screen_width or check_screen_height != screen_height:
        changed_res = True
        if 10/7 != screen_width/screen_height:
            if check_screen_width != screen_width and check_screen_height != screen_height:
                if abs(screen_width-check_screen_width) > abs(screen_height-check_screen_height):
                    new_width = screen_width-(screen_width%10)
                    if new_width < min_width:
                        new_width = min_width
                    width_mult = (new_width-1000)/10
                    new_height = 700+(7*width_mult)
                else:
                    new_height = screen_height-(screen_height%7)
                    if new_height < min_height:
                        new_height = min_height
                    height_mult = (new_height-700)/7
                    new_width = 1000+(10*height_mult)
                screen_width = new_width
                screen_height = new_height
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            elif check_screen_width != screen_width:
                new_width = screen_width-(screen_width%10)
                if new_width < min_width:
                    new_width = min_width
                width_mult = (new_width-1000)/10
                new_height = 700+(7*width_mult)
                screen_width = new_width
                screen_height = new_height
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            elif check_screen_height != screen_height:
                new_height = screen_height-(screen_height%7)
                if new_height < min_height:
                    new_height = min_height
                height_mult = (new_height-700)/7
                new_width = 1000+(10*height_mult)
                screen_width = new_width
                screen_height = new_height
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    else:
        changed_res = False
    
    center_x = screen_width / 2
    center_y = screen_height / 2
    
    # Show FPS
    if screen_no_window == False and show_fps == True:
        fps = clock.get_fps()
        hud.draw_text(str(round(fps)),hud.medium_text_font,hud.text_color,[0,0])

    temp = list(pygame.display.get_caption())
    if temp[0] == 'MoviePy':
        pygame.display.set_caption(project_name)