import subprocess
import sys
import re
import os


rm_newline = lambda str_: re.sub('\n', '', str_)

current_dpath, _ = os.path.split(sys.argv[0]); del _
MOVABLE_WINDOW_IDX = int(sys.argv[1])
with open(current_dpath+'/'+'movable_window_id_list.txt', 'r') as file:
    MOVABLE_WINDOWS_ID = rm_newline(file.read()).split(' ')

os.system("""wmctrl -ir %s -t $(wmctrl -d | grep "*" | cut -d' ' -f1)"""%(MOVABLE_WINDOWS_ID[MOVABLE_WINDOW_IDX]))
os.system('xdotool windowactivate %s'%(MOVABLE_WINDOWS_ID[MOVABLE_WINDOW_IDX]))