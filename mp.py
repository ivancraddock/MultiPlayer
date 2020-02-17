import os
from pathlib import Path
from random import choice
import shutil
import subprocess
import re
import sys
import time


def dependancy_check():

    vlc_check = shutil.which("vlc")
    if vlc_check == None:
        print("VLC NOT INSTALLED. Please visit videolan.org for the latest download")
        exit(0)
    wmctrl_check = shutil.which("wmctrl")
    if wmctrl_check == None:
        print("WMCTRL NOT INSTALLED. Please install using your packet manager")
        exit(0)

def test_select(p=None,n=""):
    if path_arg == None:
        p = (os.path.dirname(os.path.realpath(__file__)))
    file_list = os.listdir(p)
    pattern = ".avi$|.mov$|.mp4$|.flv$|.wmv$"

    final_list = [x for i,x in enumerate(file_list) if ((re.search(pattern, x)) and (n.lower() in x.lower()))]
    choice_file = choice(final_list)
    return choice_file

def test_launch(p,n):
    window_name = n
    if screen_arg >= 0:
        window_name = str(screen_arg) + "_" + n
    command = ["vlc", f'--video-title=multiplayer_{window_name}', f'{p}/{n}', "-I", "dummy"] 
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    wmctrl_output = ""
    while(f"multiplayer_{window_name}" not in wmctrl_output):
        print(f"multiplayer_{window_name}",wmctrl_output)
        time.sleep(1)
        wmctrl_output = str(subprocess.check_output(["wmctrl","-l"]))

def test_window(s):
    command_1 = ['xrandr']
    command_2 = ['grep', '*']
    p = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(command_2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0]
    width, height = str(resolution).strip("b'").split('x')

    command_3 = ["wmctrl","-r","multiplayer_" + str(s), "-e"]
    #Offset values (added/subtracted from each _window and _pos variable) may need to be manually tweaked
    x_window, x_pos = (int(width) // 2 ) - 1, (int(width) // 2) + 11
    y_window, y_pos = (int(height) //2 ) - 35 , (int(height) // 2) - 5
    if s == 0:
        command_3 += [f"0,0,0,{(x_window) * 2},{(y_window) * 2}"]
    elif s == 1:
        command_3 += [f"0,0,0,{(x_window) * 2},{y_window}"]
    elif s == 2:
        command_3 += [f"0,0,{y_pos},{(x_window) * 2},{y_window}"]
    elif s == 3:
        command_3 += [f"0,0,0,{(x_window)},{y_window * 2}"]
    elif s == 4:
        command_3 += [f"0,{x_pos},0,{(x_window)},{y_window * 2}"]
    elif s == 5:
        command_3 += [f"0,0,0,{x_window},{y_window}"]
    elif s == 6:
        command_3 += [f"0,{x_pos},0,{x_window},{y_window}"]
    elif s == 7:
        command_3 += [f"0,0,{y_pos},{x_window},{y_window}"]
    elif s == 8:
        command_3 += [f"0,{x_pos},{y_pos},{x_window},{y_window}"]

    process_3 = subprocess.Popen(command_3, stdout=subprocess.PIPE)
        
if __name__ == "__main__":

    dependancy_check()

    path_arg,name_arg,screen_arg=None,"",-1

    for i in sys.argv[1:]:
        if "-p=" in i[:3]:
            path_arg = i[3:]
        elif "-a" in i[:2]:
            audio_arg = True
        elif "-v" in i[:2]:
            video_arg = True
        elif "-n=" in i[:3]:
            name_arg = i[3:]
        elif ("-h" in i[:2]):
            f = open('help.txt', 'r')
            file_contents = f.read()
            print (file_contents)
            f.close()
            exit(1)
        elif ("-s=" in i[:3]):
            print(i[3])
            if i[3].isdigit():
                screen_arg = int(i[3])
            else:
                print("Unrecognized argument for screen position")
                exit(0)
        else:
            print('Unrecognized Command: Enter -h as an arg to see help text' )
            exit(0)

    choice_file = test_select(path_arg,name_arg)
    test_launch(path_arg, choice_file)

    if screen_arg >= 0:
        test_window(screen_arg)
    exit(1)