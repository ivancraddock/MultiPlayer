import os
from pathlib import Path
from random import choice
import shutil
import subprocess
import re
import sys
import time


path_arg,audio_arg,video_arg,name_arg,screen_arg=None,None,None,"",-1

def test_launch(path,name):
    s_name = name
    if screen_arg >= 0:
        s_name = str(screen_arg) + "_" + name

    command = ["vlc", f'--video-title=multiplayer_{s_name}', f'{path}/{name}', "-I", "dummy"] 
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    wmctrl_output = ""
    while(f"multiplayer_{s_name}" not in wmctrl_output):
        print(f"multiplayer_{s_name}",wmctrl_output)
        time.sleep(1)
        wmctrl_output = str(subprocess.check_output(["wmctrl","-l"]))

def test_select(path,a,v,n):
    if path_arg == None:
        path = (os.path.dirname(os.path.realpath(__file__)))
    file_list = os.listdir(path)
    pattern_list = []
    if (a == None) and (v == None):
        a = v = True
    if a == True:
        pattern_list += [".mp3"]
    if v == True:
        pattern_list += [".avi$",".mov$",".mp4$",".flv$",".wmv$"]
    pattern = "|".join(pattern_list)
    final_list = [x for i,x in enumerate(file_list) if ((re.search(pattern, x)) and (n.lower() in x.lower()))]
    print(final_list)
    choice_file = choice(final_list)
    return choice_file


def test_window(name,s):
    command_1 = ['xrandr']
    command_2 = ['grep', '*']
    p = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(command_2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0]
    width, height = str(resolution).strip("b'").split('x')
    x_window, x_offset = (int(width) // 2 ) - 1, (int(width) // 2) + 11
    y_window, y_offset = (int(height) //2 ) - 35 , (int(height) // 2) + 64
    command_3 = ["wmctrl","-r","multiplayer_" + str(s), "-e"]
    if s == 4:
        command_3 += [f"0,0,0,{x_window},{y_window}"]
    elif s == 5:
        command_3 += [f"0,{x_offset},0,{x_window},{y_window}"]
    elif s == 6:
        command_3 += [f"0,0,{y_offset},{x_window},{y_window}"]
    elif s == 7:
        command_3 += [f"0,{x_offset},{y_offset},{x_window},{y_window}"]

    process_3 = subprocess.Popen(command_3, stdout=subprocess.PIPE)
        

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
        exit()
    elif ("-s=" in i[:3]):
        print(i[3])
        if i[3].isdigit():
            screen_arg = int(i[3])
        else:
            print("Unrecognized argument for screen position")
            exit(1)
    else:
        print('Unrecognized Command: Enter -h as an arg to see help text' )
        exit()

choice_file = test_select(path_arg,audio_arg,video_arg,name_arg)
test_launch(path_arg, choice_file)

if screen_arg >= 0:
    test_window(choice_file,screen_arg)
exit(1)