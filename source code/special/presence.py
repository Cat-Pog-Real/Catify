from pypresence import Presence, ActivityType

import time
import threading

connected = False

client_id = 'fuck you'
RPC = Presence(client_id)
try:
    RPC.connect()
    connected = True
except:
    connected = False

if connected:
    RPC.update(
        activity_type=ActivityType.LISTENING,
        state="!! nothing dumbass !!",
        details="Listening to: "
    )

update = False

song_name = "NULL"
song_length = 0
song_paused = False
seconds_passed = 0

def update_presence():
    global update, song_name, song_length, seconds_passed, song_paused, connected
    while True:
        if update and connected:
            update = False
            if song_paused:
                RPC.update(
                    activity_type=ActivityType.LISTENING,
                    state=song_name + " | PAUSED",
                    details="Listening to: ",
                    #start=0
                    #end=time.time()+song_length-seconds_passed
                )
            else:
                RPC.update(
                    activity_type=ActivityType.LISTENING,
                    state=song_name,
                    details="Listening to: ",
                    start=time.time(),
                    end=time.time()+song_length-seconds_passed
                )
        time.sleep(1)

thread = threading.Thread(target=update_presence, daemon=True)

def start_discord():
    global connected, thread
    if connected:
        thread.start()

def update_discord(name, length, time, paused):
    global update, song_name, song_length, seconds_passed, song_paused
    update = True
    song_name = name
    song_length = length
    seconds_passed = time
    song_paused = paused