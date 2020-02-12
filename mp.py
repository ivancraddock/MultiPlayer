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
    command = ["vlc", f'--video-title=multiplayer_{name}', f'{path}/{name}', "-I", "dummy"] 
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    wmctrl_output = "."
    while(f"multiplayer_{name}" not in wmctrl_output):
        print(f"multiplayer_{name}",wmctrl_output)
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
        pattern_list += [".avi$",".mov$",".mp4$"]
    pattern = "|".join(pattern_list)
    final_list = [x for i,x in enumerate(file_list) if ((re.search(pattern, x)) and (n.lower() in x.lower()))]
    print(final_list)
    choice_file = choice(final_list)
    return choice_file


def test_window(name,s):
    pass

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
    else:
        print('Unrecognized Command: Enter -h as an arg to see help text' )
        exit()

choice_file = test_select(path_arg,audio_arg,video_arg,name_arg)
test_launch(path_arg, choice_file)

print(555*"*")

if screen_arg >= 0:
    test_window(choice_file,screen_arg)
exit(1)