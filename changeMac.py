import subprocess
import random
import re
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', help= "Define your interface")
parser.add_argument('-r', help= "Choose to reset your Mac Address to its original value", action="store_true")
parser.add_argument('-c', help= "Choose to change your Mac Address to a random one", action="store_true")
args = parser.parse_args()

inter = args.i
c = args.c
r = args.r

# Actual Script
if c  and not r:
	def rand_mac():
	    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
	        (random.randint(0, 255)),
	        random.randint(0, 255),
	        random.randint(0, 255),
	        random.randint(0, 255),
	        random.randint(0, 255),
	        random.randint(0, 255)
	        )

	randomac = rand_mac()
	print(randomac)
	ether = subprocess.check_output(['ifconfig' , inter])

	down = subprocess.Popen(['ifconfig',inter ,'down'],
	                        stdout=subprocess.PIPE,
	                        )
	change = subprocess.Popen(['ifconfig', inter, 'hw', 'ether', randomac],
							stdin=down.stdout,
							stdout=subprocess.PIPE,
							)
	up = subprocess.Popen(['ifconfig', inter, 'up'],
							stdin=change.stdout,
							stdout=subprocess.PIPE,
							)
	try:
		up.communicate()
		oMac = ether.decode('utf-8')
		p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
		oldMac = re.findall(p, oMac)
		print("Mac Address has changed from {} to {}".format(oldMac[1], randomac))
	except:
		print("Unnassignable Mac Address")

elif r and not c:
	a = subprocess.check_output('dmesg')
	aD = a.decode('utf-8')
	b = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", aD)
	burntMac = b.group(0)

	down = subprocess.Popen(['ifconfig', inter ,'down'],
                        stdout=subprocess.PIPE,
                        )
	change = subprocess.Popen(['ifconfig', inter, 'hw', 'ether', burntMac],
							stdin=down.stdout,
							stdout=subprocess.PIPE,
							)
	up = subprocess.Popen(['ifconfig', inter , 'up'],
							stdin=change.stdout,
							stdout=subprocess.PIPE,
							)
	try:
		up.communicate()
		print("Reset to ", burntMac)
	except:
		print("Error")
else:
	print("Error. Try again.")
	exit()

