import os
import sys
import time
import subprocess


def test():
	print('[x] Installing screen')
	os.system('apt install screen')
	time.sleep(5)
	print('[x] downloading bot.py')
	os.system('curl https://pastebin.com/raw/JmzDQGvs -o bot.py')
	time.sleep(3)
	print('[x] Downloading requirements ')
	os.system('curl https://pastebin.com/raw/bNWEAw6w -o requirements.txt')
	print('[x] Installing pip')
	os.system('pip install -r requirements.txt')
	p = subprocess.Popen("screen -R kontol", stdin=subprocess.PIPE, shell=True)
	p.communicate(input='\n'.encode()) 
	os.system('python3 bot.py')

test()
