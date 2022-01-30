#!/usr/bin/python3

import os
import subprocess
from time import sleep

P_HEIGHT = 36   # panel height (when visible, of course)
TIMEOUT = 3     # after this amount of seconds, the panel will be hidden
PROCESS_NAME = 'PopupPanel_xXXx' # make sure to set a unique name no other process will ever have in your machine, or those one will be killed; also make sure to use a string not longer than 15 char

def set_procname(Newname):
	newname = bytes(Newname, 'utf-8')
	from ctypes import cdll, byref, create_string_buffer
	libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
	buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
	buff.value = newname                 #Null terminated string as it should be
	libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.

def bash(cmd, read=False):
	if read:
		try:
			x = subprocess.check_output(cmd, shell=True).decode("utf-8")
		except:
			x = False
		return x
	else:
		os.system(cmd)
		return 

def minimize():
    bash(f'qdbus org.kde.plasmashell /PlasmaShell evaluateScript "p = panelById(panelIds[1]); p.height = {- P_HEIGHT};"')
    print('minimized')

def maximize():
    bash(f'qdbus org.kde.plasmashell /PlasmaShell evaluateScript "p = panelById(panelIds[1]); p.height = {P_HEIGHT};"')
    print('maximized')

def toggle():
    bash('qdbus org.kde.plasmashell /PlasmaShell evaluateScript "p = panelById(panelIds[1]); p.height = {P_HEIGHT} - p.height;"')
    print('toggled')

def killOtherProcesses():
    IDs = bash(f'ps -A | pgrep {PROCESS_NAME}', read=True).strip().split('\n')
    ownID = os.getpid()
    print(ownID, IDs)
    for ID in IDs:
        if str(ID) != str(ownID):
            print(f'{ID} != {ownID}')
            bash(f'kill {ID}')
        else:
            print(f'{ID} == {ownID}')
    print('killed')

def main():
    set_procname(PROCESS_NAME)
    killOtherProcesses()
    maximize()
    sleep(TIMEOUT)
    minimize()


if __name__ == '__main__':
    main()
    print('finished completely')