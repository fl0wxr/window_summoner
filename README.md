## window\_summoner - A method to mark a window and instantly move it to any active workspace in XFCE

The following idea demonstrates a convenient way where the user can move a marked window from any workspace to the active one in an XFCE environment.

1. Click on the window you would like to be marked as, say `MOVABLE_WINDOW_IDX` . Where `MOVABLE_WINDOW_IDX` can be any integer ranging from `0` to `9` .
2. Press `Super+Shift+Key_MOVABLE_WINDOW_IDX` to mark that active window, and to assign its corresponding movable window ID as `MOVABLE_WINDOW_IDX` .
3. Whenever you leave that workspace, move that window to the currently active workspace by pressing `Super+Key_MOVABLE_WINDOW_IDX` . `Key_MOVABLE_WINDOW_IDX` purely depends on the user’s keyboard-key preference.

### Installation

One way to implement this concept is through the following instructions. It is worth noting that this method depend on the apt packages `xdotool` and `wmctrl` .

1. Under the user’s home folder create a directory named as `.window_summoner` .
2. Then navigate inside that directory and create 4 files. The first one shall be named as `get_window_id.py` and will contain the following content

```python
import subprocess
import sys
import re
import os


rm_newline = lambda str_: re.sub('\n', '', str_)

current_dpath, _ = os.path.split(sys.argv[0]); del _
MOVABLE_WINDOW_IDX = int(sys.argv[1])
with open(current_dpath+'/'+'movable_window_id_list.txt', 'r') as file:
    MOVABLE_WINDOWS_ID = rm_newline(file.read()).split(' ')

MOVABLE_WINDOWS_ID[MOVABLE_WINDOW_IDX] = rm_newline(subprocess.check_output(['xdotool', 'getactivewindow']).decode(sys.stdout.encoding))

with open(current_dpath+'/'+'movable_window_id_list.txt', 'w') as file:
    MOVABLE_WINDOWS_ID = file.write(' '.join(MOVABLE_WINDOWS_ID))
```

The other file will be `summon_window.py` with its content being  

```python
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
```

To break down

`wmctrl -ir $MOVABLE_WINDOW_ID -t $(wmctrl -d | grep "*" | cut -d' ' -f1)`:

- `wmctrl`: a command-line utility that can interact with and manipulate X Window System windows.

- `-ir $MOVABLE_WINDOW_ID`: the `-ir` flag tells `wmctrl` to "interact with the window with the given numeric ID". `$MOVABLE_WINDOW_ID` is a Bash variable that contains the numeric ID of the window we want to move.

- `-t $(wmctrl -d | grep "*" | cut -d' ' -f1)`: the `-t` flag tells `wmctrl` to "move the window to the desktop with the given index". `$(wmctrl -d | grep "*" | cut -d' ' -f1)` is a command substitution that gets the index of the currently active desktop/workspace. Here's what's happening in that command substitution:
  
  - `wmctrl -d`: lists all available desktops/workspaces.
  - `grep "*"`: filters for the currently active desktop/workspace, which is indicated by an asterisk (`*`) in the output of `wmctrl -d`.
  - `cut -d' ' -f1`: extracts the first field (which is the index of the desktop/workspace) from the output of `grep "*"`.

The other two `movable_window_id_list.txt` , `initial_movable_window_id_list.txt` both should contain

```
0 0 0 0 0 0 0 0 0 0
```

where the latter should be read-only and should serve as a backup for the other.

3. Now depending on the maximum number of windows you intend to have marked at the same time (assuming it doesn’t surpass 10), create the following shortcuts in XFCE’s keyboard settings panel.

Do the following for every keyboard integer `MOVABLE_WINDOW_IDX` you wish to be active.
Shortcut: `Super+Shift+Key_MOVABLE_WINDOW_IDX` → Command: `python3 /home/$USER/.window_summoner/get_window_id.py MOVABLE_WINDOW_IDX` 

Shortcut: `Super+Key_MOVABLE_WINDOW_IDX` → Command: `python3 ~/.window_summoner/summon_window.sh MOVABLE_WINDOW_IDX` 

where obviously you replace `Key_MOVABLE_WINDOW_IDX` with your key of choice.

An example is the following

Shortcut: `Super+Shift+1` → Command: `source ~/.window_summoner/get_window_id.sh 1` 

And this sets up the mentioned method that allows the user to move any marked window to their active workspace.