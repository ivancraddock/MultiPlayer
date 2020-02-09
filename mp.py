import os
from pathlib import Path
from random import choice
import shutil
import subprocess
import re
import sys

path_arg, audio_arg, video_arg, name_arg = None,None,None,None

def test_teardown(path):
    shutil.rmtree(path+"/deleteme/")

def test_setup(path):

    os.mkdir(path + "/deleteme")

    for i in range(2,30):
        Path(path+"/deleteme/temp"+str(i)).touch()
    for i in range(2,7):
        Path(path+"/deleteme/temp"+str(i)+".mov").touch()
    for i in range(2,7):
        Path(path+"/deleteme/temp"+str(i)+".avi").touch()

def test_launch(path,name):
    command = ["vlc", f'--video-title=multijack_{name}', f'{path}/{name}', "-I dummy"] 
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()


def test_select(path,a,v):
    #file_list = os.listdir(path + "/deleteme")
    file_list = os.listdir(path)
    pattern = '.avi$|.mov$|.mp3$'
    final_list = [x for i,x in enumerate(file_list) if re.search(pattern, x)]
    print(final_list)
    rando = choice(final_list)
    test_launch(path,rando)

if len(sys.argv) < 2:    
    path = (os.path.dirname(os.path.realpath(__file__)))
else:
    for i in sys.argv[1:]:
        if "-p=" in i[:3]:
            path_arg = i[3:]
        elif "-a" in i[:2]:
            audio_arg = True
        elif "-v" in i[:2]:
            video_arg = True
        elif "-n=" in i[:3]:
            name_arg = i[3:]
        elif "-h" in i[:2]:
            print("help text")
            exit()
        else:
            print("Unrecognized Command")
            exit()




#test_setup(path)
test_select(path)
#test_teardown(path)

