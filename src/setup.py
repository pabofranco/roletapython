import cx_Freeze
import sys
import random
import winsound
import time
import PIL
import tkinter
import pymysql

base = None

if sys.platform == 'win32':
	base = "Win32GUI"

executables = [cx_Freeze.Executable("Roleta_Russa.py", base=base, icon="icone.ico")]

cx_Freeze.setup(
	name = "Roleta Russa",
	options = {"build_exe": {"packages":["tkinter", "PIL", "time", "winsound", "random", "pymysql"], "include_files":["icone.ico", "bullet.wav", "load.wav", "mybeep.wav", "nobullet.wav", "spin.wav", "mute.png", "unmute.png", "seta.png", "titulo.png", "tambor_a.png", "tambor_b.png", "tambor_c.png", "tambor_d.png"]}}, 
	version = "1.2",
	description = "Roleta Russa - Single Player",
	executables = executables
	)