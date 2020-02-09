import os
from pathlib import Path
from random import choice
import shutil
import subprocess

def test_teardown():
    temp_path = (os.path.dirname(os.path.realpath(__file__)))
    shutil.rmtree(temp_path+"/deleteme/")

def test_setup():
    os.mkdir("deleteme")
    print(os.listdir())

    temp_path = (os.path.dirname(os.path.realpath(__file__)))
    for i in range(2,30):
        Path(temp_path+"/deleteme/temp"+str(i)).touch()

def test_select():
    temp_path = (os.path.dirname(os.path.realpath(__file__)))
    file_list = os.listdir("deleteme")
    rando = choice(file_list)
    command = f'vlc --video-title="multijack_{rando}" "${temp_path}/deleteme/${rando}" -I dummy &' ## Creates a VLC video with a video title that corresponds to the argument passed to MultiJack
    print(command)
    ##process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    ##output, error = process.communicate()

test_setup()
test_select()
test_teardown()

