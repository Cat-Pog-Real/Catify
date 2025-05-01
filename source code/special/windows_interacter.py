from ctypes import windll

registered = False

# Constants for media keys
MOD_NOREPEAT = 0x4000  # Prevent repeated key presses
WM_HOTKEY = 0x0312

# Virtual key codes for media keys
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2

# Function to handle media key events
def handle_media_key(vk_code):
    if vk_code == VK_MEDIA_PLAY_PAUSE:
        print("Play/Pause key pressed")
        # Add logic to play/pause the song
    elif vk_code == VK_MEDIA_NEXT_TRACK:
        print("Next Track key pressed")
        # Add logic to skip to the next track
    elif vk_code == VK_MEDIA_PREV_TRACK:
        print("Previous Track key pressed")
        # Add logic to go to the previous track
    elif vk_code == VK_MEDIA_STOP:
        print("Stop key pressed")
        # Add logic to stop playback

# Function to register media keys as global hotkeys
def register_media_keys():
    global registered
    if registered == False:
        registered = True
        user32 = windll.user32
        if not user32.RegisterHotKey(None, 1, MOD_NOREPEAT, VK_MEDIA_PLAY_PAUSE):
            print("Failed to register Play/Pause key")
        if not user32.RegisterHotKey(None, 2, MOD_NOREPEAT, VK_MEDIA_NEXT_TRACK):
            print("Failed to register Next Track key")
        if not user32.RegisterHotKey(None, 3, MOD_NOREPEAT, VK_MEDIA_PREV_TRACK):
            print("Failed to register Previous Track key")
        if not user32.RegisterHotKey(None, 4, MOD_NOREPEAT, VK_MEDIA_STOP):
            print("Failed to register Stop key")

# Function to unregister media keys
def unregister_media_keys():
    global registered
    if registered:
        registered = False
        user32 = windll.user32
        user32.UnregisterHotKey(None, 1)
        user32.UnregisterHotKey(None, 2)
        user32.UnregisterHotKey(None, 3)
        user32.UnregisterHotKey(None, 4)