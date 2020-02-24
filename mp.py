import os
from pathlib import Path
from random import choice
import shutil
import subprocess
import re
import sys
import time

path_arg,name_arg,screen_arg=None,"",-1


def instance_writer(screen,name):
    with open(f'.cache/MULTIPLAYER_{screen}', 'w') as f:
        f.write(name)


def instance_terminator(screen):
    instance = ""
    if os.path.isdir(".cache"):
        if os.path.isfile(f'.cache/MULTIPLAYER_{screen}'):
            with open(f'.cache/MULTIPLAYER_{screen}', 'r') as f:
                instance = f.read()
            print(f"File read {screen}")
        else:
            return
    else:
        os.mkdir(".cache")
        print("Dir created")
        return
    command_1 = ["pkill", "-f", f"'{instance}'"]

    p = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    print(" ".join(command_1))



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

def test_resize(n,s):
    screen_wait,resolution_string = True,""

    command_1 = ['xrandr']
    command_2 = ['grep', '*']
    try: 
        p = subprocess.Popen(command_1, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(command_2, stdin=p.stdout, stdout=subprocess.PIPE)
        p.stdout.close()
        resolution_string, junk = p2.communicate()
    except:
        pass
    finally:
        p.terminate()
        p2.terminate()
    resolution = resolution_string.split()[0]
    width, height = str(resolution).strip("b'").split('x')
    print("RESIZE METHOD")
    print(n)
    command_3 = []
    #Offset values (added/subtracted from each _window and _pos variable) may need to be manually tweaked
    x_window, x_pos = (int(width) // 2 ) - 1, (int(width) // 2) + 11
    y_window, y_pos = (int(height) //2 ) - 35 , (int(height) // 2) - 5
    if s == 0:
        command_3 = [f"0,0,0,{(x_window) * 2},{(y_window) * 2}"]
    elif s == 1:
        command_3 = [f"0,0,0,{(x_window) * 2},{y_window}"]
    elif s == 2:
        command_3 = [f"0,0,{y_pos},{(x_window) * 2},{y_window}"]
    elif s == 3:
        command_3 = [f"0,0,0,{(x_window)},{y_window * 2}"]
    elif s == 4:
        command_3 = [f"0,{x_pos},0,{(x_window)},{y_window * 2}"]
    elif s == 5:
        command_3 = [f"0,0,0,{x_window},{y_window}"]
    elif s == 6:
        command_3 = [f"0,{x_pos},0,{x_window},{y_window}"]
    elif s == 7:
        command_3 = [f"0,0,{y_pos},{x_window},{y_window}"]
    elif s == 8:
        command_3 = [f"0,{x_pos},{y_pos},{x_window},{y_window}"]

    wmctrl_output = ""
    while(screen_wait):
        wmctrl_output = str(subprocess.check_output(["wmctrl","-l"]))[2:-1]
        if n in wmctrl_output:
            screen_wait = False
        time.sleep(0.5)

    window_id = ""
    for i in wmctrl_output.split('\\n'):
        if n in i:
            window_id = i[:10]
            break
    
    command_3 = ["wmctrl","-i","-r",window_id, "-e"] + command_3


    try:
        process_3 = subprocess.Popen(command_3, stdout=subprocess.PIPE)
    except:
        pass
    finally:
        print("PROCESS 3 finished")

def test_launch(p,n,s):
    kill_string = None
    if f'MULTIPLAYER_{s}' in os.environ.keys():
        pass
    print(n)
    command = ["vlc", f'{p}{n}', '--play-and-exit', '--no-fullscreen'] 
    n = str(n.encode("utf-8"))[2:-1]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        os.environ[f'MULTIPLAYER_{s}'] = n
        if s != None:
            test_resize(n,s)
        while(True):
            time.sleep(20)

    except:
        pass
    finally:
        process.terminate()

if __name__ == "__main__":


    dependancy_check()

    path_arg,name_arg,screen_arg=None,"",-1

    for i in sys.argv[1:]:
        if "-p=" in i[:3]:
            path_arg = i[3:]
        elif "-n=" in i[:3]:
            name_arg = i[3:]
        elif ("-h" in i[:2]):
            with open('help.txt', 'r') as f:
                file_contents = f.read()
                print (file_contents)
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

    instance_terminator(screen_arg)
    choice_file = test_select(path_arg,name_arg)
    instance_writer(screen_arg,choice_file)
    test_launch(path_arg, choice_file, screen_arg)

    exit(1)