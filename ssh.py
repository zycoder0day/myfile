import os
import sys
import time
import subprocess


def test():
	print('[x] Installing screen')
	os.system('apt install screen')
	time.sleep(5)
	print('[x] downloading bot.py')
	os.system('curl https://pastebin.com/raw/iga3EnDW -o bot.py')
	time.sleep(3)
	print('[x] Downloading requirements ')
	os.system('curl https://pastebin.com/raw/Z77cKGcy -o requirements.txt')
	print('[x] Installing pips')
	os.system('pip install -r requirements.txt')
	time.sleep(5)	

test()
